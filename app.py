from flask import Flask, render_template, request
from sqlalchemy.exc import SQLAlchemyError

from config import Config
from extensions import db, cache
from queries import get_active_classes
from filters import (
    apply_filters,
    filter_options,
    region_bairro_pairs,
    WEEKDAY_ORDER,
    WEEKDAY_LABELS,
    TIME_PERIODS,
    IDADE_MIN,
    IDADE_MAX,
)


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
            classes = []
            error = (
                "Não foi possível carregar as aulas no momento. "
                "Tente novamente em alguns minutos."
            )

        filters_submitted = "f" in request.args

        if filters_submitted:
            turmas = apply_filters(classes, request.args)
        else:
            turmas = [t for t in classes if (t["vagas_disponiveis"] or 0) > 0]

        return render_template(
            "index.html",
            classes=turmas,
            total_classes=len(classes),
            error=error,
            options=filter_options(classes),
            region_bairro_pairs=region_bairro_pairs(classes),
            weekday_order=WEEKDAY_ORDER,
            weekday_labels=WEEKDAY_LABELS,
            time_periods=TIME_PERIODS,
            idade_min=IDADE_MIN,
            idade_max=IDADE_MAX,
            params=request.args,
            filters_submitted=filters_submitted,
        )

    @app.route("/healthz")
    def healthz():
        return {"status": "ok"}

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
