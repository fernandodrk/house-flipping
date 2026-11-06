# Simulador de House Flipping

Simulador em página única (`house-flipping.html`) para avaliar operações de compra, reforma e revenda de imóveis em São Paulo, usando a base pública de ITBI da Prefeitura.

## Arquivos

- `house-flipping.html` — o simulador. Abra num servidor local (ex.: `python -m http.server 8765`) para que ele carregue os dados de `ITBI/dados/`.
- `prepara_itbi.py` — pré-processa as planilhas anuais de ITBI (`ITBI/*.xlsx`) e gera os arquivos compactos em `ITBI/dados/` (`<ano>.gz.txt` + `index.json`).
- `converte_ods.py` — converte `.ods` em `.xlsx`.
- `house-flipping-unificada.xlsx.ods` — planilha de referência.

## Dados brutos

As planilhas `ITBI/*.ods` e `ITBI/*.xlsx` não estão no repositório (são grandes demais). Baixe-as em
https://prefeitura.sp.gov.br/web/fazenda/w/acesso_a_informacao/31501 e rode:

```
python prepara_itbi.py
```

Os arquivos já processados em `ITBI/dados/` estão versionados, então o simulador funciona sem as planilhas brutas.
