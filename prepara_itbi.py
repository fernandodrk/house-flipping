"""Pré-processa a base de ITBI da Prefeitura de São Paulo para o simulador.

Lê os arquivos anuais em ITBI\\*.xlsx (converte .ods que ainda não tenham xlsx) e grava,
em ITBI\\dados\\, um arquivo compacto por ano (<ano>.gz.txt: JSON em gzip, em base64) mais um index.json. O
simulador carrega esses arquivos sozinho ao abrir, em poucos segundos, em vez de
abrir os xlsx de dezenas de MB no navegador.

Uso:
    python prepara_itbi.py            # processa tudo em ITBI\\
    python prepara_itbi.py ITBI\\2026.xlsx   # só um arquivo

Só usa a biblioteca padrão e o openpyxl. Rode de novo sempre que baixar um ano novo
ou atualizado da Fazenda (https://prefeitura.sp.gov.br/web/fazenda/w/acesso_a_informacao/31501).
"""
import sys, os, re, json, gzip, glob, base64, datetime, unicodedata
from openpyxl import load_workbook

PASTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ITBI")
SAIDA = os.path.join(PASTA, "dados")

# mesmas regras de reconhecimento de coluna do simulador
COLS = {
    "sql": r"cadastro|^sql", "log": r"logradouro", "num": r"^numero$|^n[º°]\.?$|^num\.?$|^numero do imovel$",
    "compl": r"complemento", "bairro": r"bairro", "refer": r"^referencia$", "nat": r"natureza",
    "valor": r"valor de transa", "data": r"data de transa", "vvr": r"^valor venal de referencia$",
    "base": r"base de calculo", "prop": r"proporcao", "matricula": r"matricula", "cartorio": r"cartorio",
    "areaC": r"area construida", "uso": r"descricao do uso", "padrao": r"descricao do padrao", "fin": r"tipo de financ",
}
DICTS = ["log", "bairro", "refer", "nat", "fin", "cartorio", "uso", "padrao"]
MESES = {"jan": 0, "fev": 1, "mar": 2, "abr": 3, "mai": 4, "jun": 5, "jul": 6, "ago": 7, "set": 8, "out": 9, "nov": 10, "dez": 11}


def norm(s):
    s = "" if s is None else str(s)
    return unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower().strip()


def sheet_month(nome, arquivo):
    m = re.search(r"(?:^|[^a-z])(jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez)[a-z]*[\s\-_/.]*(\d{4}|\d{2})?", norm(nome))
    if not m:
        return None
    y = int(m.group(2)) if m.group(2) else None
    if y is not None and y < 100:
        y += 2000
    if y is None:
        f = re.search(r"20\d\d", os.path.basename(arquivo))
        y = int(f.group(0)) if f else None
    return None if y is None else y * 12 + MESES[m.group(1)]


def num(v):
    if isinstance(v, (int, float)):
        return float(v)
    if v is None:
        return None
    s = re.sub(r"[R$\s]", "", str(v)).replace(".", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def data(v):
    if isinstance(v, datetime.datetime):
        return v.date()
    if isinstance(v, datetime.date):
        return v
    if isinstance(v, (int, float)):
        return (datetime.date(1899, 12, 30) + datetime.timedelta(days=int(v)))
    m = re.search(r"(\d{1,2})[/\-](\d{1,2})[/\-](\d{4})", str(v or ""))
    if m:
        return datetime.date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", str(v or ""))
    if m:
        return datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    return None


EPOCH = datetime.date(1970, 1, 1)


class Colunas:
    def __init__(self):
        self.n = 0
        self.c = {k: [] for k in ["valor", "vvr", "base", "prop", "areaC", "num", "dataD", "reg", "regSheet"] + DICTS}
        self.s = {"sql": [], "compl": [], "matricula": []}
        self.d = {k: {} for k in DICTS}

    def did(self, k, v):
        d = self.d[k]
        if v not in d:
            d[v] = len(d)
        return d[v]

    def add(self, r, m, reg_sheet):
        g = lambda k: r[m[k]] if k in m and m[k] < len(r) else None
        valor = num(g("valor"))
        if not valor or valor <= 0:
            return False
        d = data(g("data")) if "data" in m else None
        reg = reg_sheet if reg_sheet is not None else (d.year * 12 + d.month - 1 if d else None)
        areaC = num(g("areaC"))
        c = self.c
        c["valor"].append(valor); c["vvr"].append(num(g("vvr"))); c["base"].append(num(g("base"))); c["prop"].append(num(g("prop")))
        c["areaC"].append(areaC); c["num"].append(num(g("num")))
        c["dataD"].append((d - EPOCH).days if d else -1); c["reg"].append(-1 if reg is None else reg); c["regSheet"].append(1 if reg_sheet is not None else 0)
        for k in DICTS:
            v = g(k)
            c[k].append(self.did(k, "" if v is None else str(v).strip()))
        sql = g("sql"); self.s["sql"].append(re.sub(r"\D", "", "" if sql is None else str(sql)))
        compl = g("compl"); self.s["compl"].append("" if compl is None else str(compl).strip())
        mt = g("matricula"); self.s["matricula"].append("" if mt is None else (int(mt) if isinstance(mt, float) and mt.is_integer() else mt))
        self.n += 1
        return True

    def json(self):
        f = lambda v: None if v is None else (int(v) if float(v).is_integer() and abs(v) < 1e15 else round(v, 4))
        out = {"n": self.n, "dict": {k: list(d.keys()) for k, d in self.d.items()}, "s": self.s}
        for k, col in self.c.items():
            out[k] = [f(v) for v in col] if k in ("valor", "vvr", "base", "prop", "areaC", "num") else col
        return out


def processa(arquivo):
    print(f"Lendo {arquivo}", flush=True)
    wb = load_workbook(arquivo, read_only=True, data_only=True)
    cols = Colunas(); meses = set()
    for ws in wb.worksheets:
        reg_sheet = sheet_month(ws.title, arquivo)
        m = None; lidas = 0
        for i, row in enumerate(ws.iter_rows(values_only=True)):
            if m is None:
                if i > 15:
                    break
                if any("logradouro" in norm(c) for c in row):
                    m = {}
                    for j, c in enumerate(row):
                        n = norm(c)
                        for k, rx in COLS.items():
                            if k not in m and re.search(rx, n):
                                m[k] = j
                    if "valor" not in m:
                        m = None; break
                continue
            if cols.add(row, m, reg_sheet):
                lidas += 1
        if lidas:
            print(f"  {ws.title}: {lidas} transações", flush=True)
            if reg_sheet is not None:
                meses.add(reg_sheet)
    wb.close()
    return cols, meses


def main(args):
    os.makedirs(SAIDA, exist_ok=True)
    arquivos = args or sorted(glob.glob(os.path.join(PASTA, "*.xlsx")))
    if not args:
        for ods in sorted(glob.glob(os.path.join(PASTA, "*.ods"))):
            x = os.path.splitext(ods)[0] + ".xlsx"
            if not os.path.exists(x):
                sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
                from converte_ods import convert
                print(f"Convertendo {ods}", flush=True); convert(ods, x); arquivos.append(x)
        arquivos = sorted(set(arquivos))
    idx_path = os.path.join(SAIDA, "index.json")
    index = {"gerado": datetime.date.today().isoformat(), "arquivos": []}
    if os.path.exists(idx_path) and args:  # processamento parcial preserva os outros anos
        index["arquivos"] = [a for a in json.load(open(idx_path, encoding="utf-8"))["arquivos"] if a["origem"] not in [os.path.basename(x) for x in args]]
    for arq in arquivos:
        cols, meses = processa(arq)
        if not cols.n:
            print(f"  {arq}: nenhuma planilha com as colunas da base; ignorado", flush=True); continue
        f = re.search(r"20\d\d", os.path.basename(arq))
        ano = int(f.group(0)) if f else max(meses) // 12 if meses else 0
        # gzip em base64 num .txt: é o único formato compacto que o artefato publicado aceita como anexo
        nome = f"{ano}.gz.txt"
        bruto = json.dumps(cols.json(), ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        with open(os.path.join(SAIDA, nome), "wb") as fh:
            fh.write(base64.b64encode(gzip.compress(bruto, compresslevel=6)))
        tam = os.path.getsize(os.path.join(SAIDA, nome))
        index["arquivos"].append({"ano": ano, "arquivo": nome, "origem": os.path.basename(arq), "n": cols.n, "meses": sorted(meses), "bytes": tam})
        print(f"OK: {nome} ({cols.n} transações, {tam/1048576:.1f} MB)", flush=True)
    index["arquivos"].sort(key=lambda a: a["ano"])
    json.dump(index, open(idx_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"index.json: {len(index['arquivos'])} arquivos, {sum(a['n'] for a in index['arquivos'])} transações", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
