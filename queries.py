from sqlalchemy import text
from extensions import db, cache

MAIN_QUERY = text(
    """
    SELECT
        cat.name                       AS categoria,
        act.name                       AS curso,
        c.class_name                   AS turma_genero,
        f.name                         AS local,
        f.address                      AS endereco,
        f.neighborhood                 AS bairro,
        r.name                         AS regiao,
        c.weekdays                     AS dias_semana,
        c.start_time                   AS horario_inicio,
        c.end_time                     AS horario_fim,
        c.min_age                      AS idade_min,
        c.max_age                      AS idade_max,
        c.is_active                    AS turma_ativa,
        snap.available_slots           AS vagas_disponiveis,
        snap.pcd_available_slots       AS vagas_pcd,
        snap.collected_at              AS data_coleta
    FROM classes c
    JOIN activities act               ON act.id = c.activity_id
    JOIN facilities f                 ON f.id = c.facility_id
    JOIN regions r                    ON r.id = c.region_id
    LEFT JOIN activity_categories ac  ON ac.activity_id = act.id
    LEFT JOIN categories cat          ON cat.id = ac.category_id
    LEFT JOIN LATERAL (
        SELECT s.available_slots, s.pcd_available_slots, s.collected_at
        FROM availability_snapshots s
        WHERE s.class_hash = c.class_hash
        ORDER BY s.collected_at DESC
        LIMIT 1
    ) snap ON true
    WHERE c.is_active = true
    ORDER BY cat.name NULLS LAST, act.name, f.name, c.start_time;
    """
)


@cache.cached(key_prefix="active_classes")
def get_active_classes():
    result = db.session.execute(MAIN_QUERY)
    return [dict(row._mapping) for row in result]
