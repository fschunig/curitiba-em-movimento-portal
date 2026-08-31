# Curitiba em Movimento — Dashboard

Landing page (Flask, deploy no Render) que mostra as aulas gratuitas
oferecidas pela prefeitura de Curitiba ("Curitiba em Movimento"), com
filtros ricos para encontrar rapidamente uma turma com vaga.

App **somente leitura**: consulta um Postgres (hospedado no Railway) que é
populado por um job Airflow separado (scraping do site da prefeitura). Este
repositório não faz scraping/ETL nem escreve no banco.

## Stack
- Flask + SQLAlchemy
- Postgres (Railway) via `DATABASE_URL`
- Flask-Caching (cache leve em memória, dados só mudam quando o Airflow roda)
- Deploy: Render (`gunicorn app:app`)

## Rodando localmente
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # preencha DATABASE_URL com o Postgres do Railway
python app.py             # http://localhost:5000
```

## Estrutura
```
app.py            # factory da app Flask + rotas
config.py         # configuração via env vars
extensions.py     # instâncias compartilhadas (db, cache)
models.py         # modelos SQLAlchemy refletindo o schema.sql
queries.py        # query principal (turmas ativas + snapshot mais recente)
templates/        # HTML (Jinja)
static/           # CSS/JS
```

## Pontos em aberto (ver instruções completas do projeto)
- Confirmar schema real de `categories` e `activity_categories`
- Definir lista final e UX dos filtros complexos
- Decidir onde normalizar `weekdays` (query/view vs. lado do Flask)

---

## Fluxo de trabalho (branches)

Usamos **GitHub Flow**: a `main` é sempre deployável (é o que o Render
publica). Todo trabalho novo nasce de uma branch curta e volta pra `main`
via Pull Request.

### Convenção de nomes
| Prefixo    | Quando usar                                  | Exemplo                          |
|------------|-----------------------------------------------|-----------------------------------|
| `feature/` | Nova funcionalidade                           | `feature/filtro-dia-semana`      |
| `fix/`     | Correção de bug                               | `fix/endereco-malformado`        |
| `chore/`   | Manutenção, deps, config, sem mudar comportamento | `chore/atualizar-requirements`|

### Passo a passo
```bash
# 1. Sempre partir da main atualizada
git checkout main
git pull origin main

# 2. Criar a branch
git checkout -b feature/nome-da-feature

# 3. Trabalhar e commitar
git add .
git commit -m "feat: descrição curta da mudança"

# 4. Subir a branch
git push -u origin feature/nome-da-feature

# 5. Abrir Pull Request no GitHub (feature/... -> main)
#    Revisar o diff, conferir se o Render faria o deploy sem quebrar.

# 6. Fazer merge (squash merge é o recomendado, mantém a main com
#    histórico limpo, um commit por feature/fix)

# 7. Apagar a branch (local e remota)
git branch -d feature/nome-da-feature
git push origin --delete feature/nome-da-feature
```

Prefixos de commit sugeridos (Conventional Commits, opcional mas ajuda):
`feat:`, `fix:`, `chore:`, `docs:`, `refactor:`.
