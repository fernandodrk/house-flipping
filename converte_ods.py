"""Converte a base de ITBI da Prefeitura de São Paulo de .ods para .xlsx.

Os arquivos .ods anuais têm um content.xml de centenas de MB, que o navegador não
consegue abrir. Este script lê o XML em streaming (sem carregar tudo na memória)
e grava um .xlsx com as mesmas planilhas mensais, que o simulador lê normalmente.

Uso:
    python converte_ods.py ITBI\\2025.ods            -> gera ITBI\\2025.xlsx
    python converte_ods.py ITBI\\2024.ods ITBI\\2025.ods

Só usa a biblioteca padrão e o openpyxl.
"""
import sys, os, zipfile, datetime
import xml.etree.ElementTree as ET
from openpyxl import Workbook

NS = {
    "table": "urn:oasis:names:tc:opendocument:xmlns:table:1.0",
    "office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
    "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
}
T = lambda n: "{%s}%s" % (NS["table"], n)
O = lambda n: "{%s}%s" % (NS["office"], n)
MAX_REPEAT = 64  # repetições de célula/linha vazia além disso são preenchimento até o fim da grade


def cell_value(cell):
    vt = cell.get(O("value-type"))
    if vt in ("float", "percentage", "currency"):
        v = cell.get(O("value"))
        try:
            f = float(v)
            return int(f) if f.is_integer() and abs(f) < 1e15 else f
        except (TypeError, ValueError):
            return v
    if vt == "date":
        v = cell.get(O("date-value"), "")
        try:
            return datetime.datetime.fromisoformat(v[:19])
        except ValueError:
            return v
    if vt == "boolean":
        return cell.get(O("boolean-value")) == "true"
    # string: concatena os parágrafos
    txt = "".join(cell.itertext())
    return txt if txt != "" else None


def convert(src, dst):
    wb = Workbook(write_only=True)
    with zipfile.ZipFile(src) as z, z.open("content.xml") as f:
        ws = None
        sheets = rows_total = 0
        for ev, el in ET.iterparse(f, events=("start", "end")):
            if ev == "start" and el.tag == T("table"):
                ws = wb.create_sheet(title=(el.get(T("name")) or f"Planilha{sheets+1}")[:31])
                sheets += 1
                print(f"  planilha {ws.title}", flush=True)
            elif ev == "end" and el.tag == T("table-row") and ws is not None:
                row = []
                for c in el:
                    if c.tag not in (T("table-cell"), T("covered-table-cell")):
                        continue
                    rep = int(c.get(T("number-columns-repeated"), "1"))
                    v = cell_value(c)
                    if v is None and rep > MAX_REPEAT:
                        rep = 0
                    row.extend([v] * min(rep, 1024))
                while row and row[-1] is None:
                    row.pop()
                rrep = int(el.get(T("number-rows-repeated"), "1"))
                if row:
                    for _ in range(min(rrep, MAX_REPEAT)):
                        ws.append(row); rows_total += 1
                el.clear()
            elif ev == "end" and el.tag == T("table"):
                el.clear()
    wb.save(dst)
    print(f"OK: {dst} ({sheets} planilhas, {rows_total} linhas)", flush=True)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    for src in sys.argv[1:]:
        dst = os.path.splitext(src)[0] + ".xlsx"
        print(f"Convertendo {src} -> {dst}", flush=True)
        convert(src, dst)
