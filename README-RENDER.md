# CiberSec News Hub — Render (Zero-Cost Free Tier)

Este pacote permite publicar o **CiberSec News Hub** na **Render** usando o plano **Free** (sem custo mensal), com API Python (FastAPI) e site estático.

## O que você precisa
- Uma conta gratuita na Render (https://render.com) — Free tier, conforme a própria documentação da Render. Veja "Deploy for Free" e "Pricing".

## Passo a passo (sem comandos complexos)
1) Crie um repositório no GitHub (botão **New** > vazio).
2) Faça upload de **todos** os arquivos deste pacote (incluindo `render.yaml`, `backend/` e `frontend/`).  
   Dica: arraste e solte a pasta inteira no GitHub Web.
3) Na Render, clique **New +** > **Blueprint** > **Use a Blueprint from a repo** e selecione seu repositório.
4) Confirme o deploy. A Render criará **dois serviços**:
   - **cibersec-news-api** (web service Python, plano *free*)
   - **cibersec-news-front** (static site, plano *free*)
5) Após o primeiro deploy, acesse:
   - API: `https://<SEU_API_HOST>.onrender.com/health`
   - Site: `https://<SEU_FRONT_HOST>.onrender.com`
6) **Ativar ingestão manual**: acesse via navegador `https://<SEU_API_HOST>.onrender.com/ingest/run` (para popular as primeiras notícias já).  
   A coleta diária automática roda às **07:00 America/Sao_Paulo**.
7) **Logo**: defina a variável de ambiente `LOGO_URL` no serviço **front** (Render > serviço `cibersec-news-front` > Settings > Environment). Por padrão, há um placeholder. Cole aqui a URL da sua logo.

> Observação: alguns feeds podem exigir confirmação de URL de RSS. Ajuste `backend/ingest/sources.yaml` se necessário (basta editar no GitHub e a Render redeploya automaticamente).

## Observações de plano gratuito
- Free tier da Render permite **web services** e **static sites** sem custo, porém com limites de uso e recursos. Isso é suficiente para protótipo e blog pessoal. Para persistência, usamos SQLite.
- Para ambientes de produção, considere Postgres pago e recursos adicionais.

## Suporte rápido
- Se a página do **front** não conseguir chamar a API (erro CORS, etc.), confirme a variável `API_URL` no serviço **front** para apontar ao host da API.

Bom deploy! :)
