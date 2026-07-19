# Futebol Analytics

Este projeto foi criado para analisar dados de jogadores, clubes, seleções e ligas de futebol pelo mundo, com dados reais ao longo de diversas temporadas.

## Sobre

Este projeto une duas coisas que eu mais gosto de fazer: transformar dados complexos e reais em insights acionáveis, e futebol. Aqui teremos diversas análises sobre temas diferentes.

## Fonte dos dados

Os dados são coletados via web scraping do Sofascore. Este é um projeto de estudo.

## Estrutura do projeto

- `src/` — scripts de coleta de dados (raspagem de estatísticas e perfis dos jogadores)
- `data/` — dados coletados (não versionados; gerados ao rodar os scripts)
- `notebooks/` — análises e exploração dos dados
- `docs/` — documentação do projeto

## Como rodar

O projeto foi desenvolvido em Python 3.12.

1. Clone o repositório e entre na pasta:

```
git clone https://github.com/gabrielcondesilva/futebol-analytics.git
cd futebol-analytics
```

2. Crie e ative um ambiente virtual:

```
python -m venv .venv
.venv\Scripts\activate
```

3. Instale as dependências:

```
pip install -r requirements.txt
```

4. Rode os scripts de coleta na pasta `src/` para gerar os dados.

## Status

Projeto iniciado há pouco tempo e ainda em andamento. As análises serão adicionadas ao repositório com o tempo. Sinta-se à vontade para entrar em contato caso tenha alguma ideia de análise para eu desenvolver e publicar aqui.

## Contato

LinkedIn: [Gabriel Conde Silva](https://www.linkedin.com/in/gabrielcondesilva/)