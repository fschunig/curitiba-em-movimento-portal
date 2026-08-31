from flask import Flask, render_template
from sqlalchemy.exc import SQLAlchemyError

from config import Config
from extensions import db, cache
from queries import get_active_classes


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    cache.init_app(app)

    @app.route("/")
    def index():
        try:
            classes = get_active_classes()
            error = None
        except SQLAlchemyError:
            # Ex.: partição do mês corrente ainda não criada pelo Airflow,
            # ou banco temporariamente indisponível. Falha de forma amigável
            # em vez de estourar erro 500 cru pro usuário.
            classes = []
            error = (
                "Não foi possível carregar as aulas no momento. "
                "Tente novamente em alguns minutos."
            )
        return render_template("index.html", classes=classes, error=error)

    @app.route("/healthz")
    def healthz():
        return {"status": "ok"}

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
