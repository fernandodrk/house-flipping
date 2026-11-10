# Simulador de House Flipping

Simulador em página única (`house-flipping.html`) para avaliar operações de compra, reforma e revenda de imóveis em São Paulo, usando a base pública de ITBI da Prefeitura.

## Guia para quem nunca programou

Com este guia você terá uma cópia do simulador funcionando no seu computador sem digitar nenhum comando: quem faz o trabalho técnico é o Claude. Reserve cerca de 30 minutos.

### O que você vai precisar

| Item | Detalhe |
| --- | --- |
| Computador | Windows ou Mac, com internet |
| E-mail | Um endereço que você consiga abrir agora, para confirmar a conta do GitHub |
| Assinatura do Claude | Plano Pro, Max, Ultra, Team ou Enterprise. O plano gratuito não inclui a aba Code usada neste guia ([fonte](https://code.claude.com/docs/en/desktop-quickstart)) |
| Espaço em disco | Cerca de 50 MB para o projeto e seus dados |

### Passo 1: criar a conta no GitHub

O GitHub é o site onde o projeto está guardado. A conta é gratuita e leva cerca de 5 minutos.

1. Abra [github.com/signup](https://github.com/signup) no navegador.
2. Informe seu e-mail, crie uma senha e escolha um nome de usuário. O nome de usuário é público e aparece no endereço do seu perfil.
3. Resolva o desafio de verificação que o site mostrar, para provar que você é uma pessoa.
4. Abra seu e-mail, copie o código que o GitHub enviou e cole na tela de confirmação.
5. Se o site oferecer planos, escolha o gratuito ("Free"). Ele é suficiente para este guia.

Guarde o e-mail e a senha em local seguro. O Claude nunca precisa da sua senha do GitHub: se alguma tela pedir login, digite você mesmo.

O projeto é público, então a cópia do Passo 3 funciona mesmo sem conta. A conta passa a ser necessária quando você quiser guardar a sua própria versão no GitHub ou sugerir melhorias ao projeto original.

### Passo 2: instalar o Claude no computador

O aplicativo do Claude para computador já traz a aba Code pronta para uso ([fonte](https://code.claude.com/docs/en/desktop)). Se faltar algum programa auxiliar no seu computador, como Git ou Python, o Claude avisa no Passo 3.

1. Baixe o instalador do seu sistema: [Windows](https://claude.ai/api/desktop/win32/x64/setup/latest/redirect) ou [Mac](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect).
2. Abra o arquivo baixado e siga a instalação até o fim.
3. Abra o Claude e entre com a sua conta do Claude, a mesma da assinatura.
4. Clique na aba **Code**. É nela que o Claude consegue trabalhar com pastas e arquivos do seu computador.

Se a aba Code não aparecer ou pedir uma assinatura, a conta está no plano gratuito. Veja a tabela de requisitos acima.

### Passo 3: pedir ao Claude para copiar o projeto

Você cria uma pasta vazia, mostra essa pasta ao Claude e cola uma mensagem pronta. "Clonar" é o nome técnico dessa cópia.

1. Crie uma pasta vazia chamada `house-flipping` dentro de Documentos.
2. Na aba Code, olhe a linha de opções logo abaixo da caixa de mensagem. No seletor de ambiente, escolha a primeira opção do grupo **Local**.
3. Ao lado, clique no controle da pasta do projeto, escolha **Open folder…** e selecione a pasta `house-flipping` que você criou. Os nomes podem aparecer em português no seu aplicativo.
4. Cole a mensagem abaixo na caixa de mensagem e pressione Enter.
5. O Claude pode pedir sua autorização antes de executar cada comando. Leia o que ele pretende fazer e aprove.
6. Aguarde o aviso de que a cópia terminou. O download tem cerca de 25 MB.

```text
Esta pasta está vazia. Copie para dentro dela o projeto público
https://github.com/fernandodrk/house-flipping
(faça o git clone direto nesta pasta, sem criar subpasta).

Depois leia o README.md e abra o simulador house-flipping.html no
painel do navegador, usando o servidor local configurado em
.claude/launch.json.

Sou leigo em programação. Se faltar algum programa no meu computador,
como Git ou Python, pare e me explique como instalar, passo a passo.
```

Os itens 2 e 3 desta lista seguem o [guia oficial do aplicativo](https://code.claude.com/docs/en/desktop-quickstart).

### Passo 4: abrir o simulador

A mensagem do Passo 3 já pede ao Claude para abrir o simulador, então ele deve aparecer sozinho no painel **Browser**, dentro do próprio aplicativo.

- **Como saber que funcionou:** a página "Simulador de House Flipping" aparece com os resultados de uma simulação de exemplo, como lucro líquido e retorno sobre o investimento. Na aba "Mercado e ITBI", a base deve mostrar cerca de 604 mil transações de janeiro de 2024 a agosto de 2026.
- **Se o painel não abrir:** pressione Ctrl+Shift+B no Windows ou Cmd+Shift+B no Mac, ou escreva ao Claude "abra o simulador no navegador".
- **Nas próximas vezes:** abra a mesma pasta `house-flipping` na aba Code e escreva "abra o simulador".

O simulador não funciona com dois cliques no arquivo `house-flipping.html`. Ele precisa de um pequeno servidor local para ler os dados, e é o Claude quem liga esse servidor ([fonte](https://code.claude.com/docs/en/desktop)).

### Se algo der errado

Na dúvida, descreva ao Claude o que apareceu na tela, com as suas palavras. Ele costuma resolver na própria conversa.

| O que aconteceu | O que fazer |
| --- | --- |
| A aba Code não aparece ou pede assinatura | A conta está no plano gratuito. A aba Code exige Pro, Max, Ultra, Team ou Enterprise. |
| O Claude avisa que o Git não está instalado | No Windows, instale por [git-scm.com](https://git-scm.com/downloads) aceitando as opções padrão. No Mac, aceite a instalação das ferramentas de desenvolvedor que o sistema oferecer. Feche e abra o Claude e repita o Passo 3. |
| O Claude avisa que o Python não está instalado | Instale por [python.org/downloads](https://www.python.org/downloads/). No Windows, marque a opção de adicionar o Python ao PATH durante a instalação. Feche e abra o Claude e escreva "abra o simulador". |
| O Claude diz que a pasta não está vazia | Crie uma pasta nova, vazia, e repita o Passo 3 com ela. |
| A página abre, mas fica sem dados | O arquivo foi aberto com dois cliques. Peça ao Claude: "abra o simulador pelo servidor local". |
| Alguma tela pede a senha do GitHub | Digite você mesmo. Não envie a senha na conversa com o Claude. |

Existe também um caminho sem instalar nada: em [claude.ai/code](https://claude.ai/code), você conecta a conta do GitHub criada no Passo 1 e o Claude trabalha em qualquer repositório público, na nuvem ([fonte](https://code.claude.com/docs/en/web-quickstart)). A cópia, porém, não fica no seu computador.

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
