import os


class Config:
    """Configuração da aplicação, lida via variáveis de ambiente.

    DATABASE_URL nunca deve ser hardcoded — vem do Render (que por sua vez
    aponta para o Postgres hospedado no Railway).
    """

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Cache leve em memória — dados só mudam quando o Airflow roda,
    # então não precisamos bater no Postgres a cada request.
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get("CACHE_TIMEOUT_SECONDS", 300))
