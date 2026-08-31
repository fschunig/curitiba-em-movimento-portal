import re
import unicodedata
from datetime import time

WEEKDAY_ORDER = ["dom", "seg", "ter", "qua", "qui", "sex", "sab"]

WEEKDAY_LABELS = {
    "dom": "Domingo",
    "seg": "Segunda",
    "ter": "Terça",
    "qua": "Quarta",
    "qui": "Quinta",
    "sex": "Sexta",
    "sab": "Sábado",
}

_ORDINAL_TO_CODE = {"2": "seg", "3": "ter", "4": "qua", "5": "qui", "6": "sex"}

TIME_PERIODS = {
    "manha": ("Manhã", time(0, 0), time(11, 59, 59)),
    "tarde": ("Tarde", time(12, 0), time(17, 59, 59)),
    "noite": ("Noite", time(18, 0), time(23, 59, 59)),
}

IDADE_MIN = 0
IDADE_MAX = 100


def _strip_accents(text):
    normalized = unicodedata.normalize("NFKD", text)
    return "".join(char for char in normalized if not unicodedata.combining(char))


def _fold(text):
    return _strip_accents(text or "").lower()


def normalize_weekdays(raw):
    if not raw:
        return []

    text = _fold(raw)
    codes = []
    for match in re.finditer(r"([2-6])a|sabado|domingo", text):
        token = match.group(0)
        if token == "sabado":
            code = "sab"
        elif token == "domingo":
            code = "dom"
        else:
            code = _ORDINAL_TO_CODE[match.group(1)]
        if code not in codes:
            codes.append(code)
    return codes


def filter_options(classes):
    categorias = sorted({c["categoria"] for c in classes if c["categoria"]})
    regioes = sorted({c["regiao"] for c in classes if c["regiao"]})
    bairros = sorted({c["bairro"] for c in classes if c["bairro"]})
    return {"categorias": categorias, "regioes": regioes, "bairros": bairros}


def region_bairro_pairs(classes):
    pairs = {(c["regiao"], c["bairro"]) for c in classes if c["regiao"] and c["bairro"]}
    return sorted(pairs)


def apply_filters(classes, params):
    busca = _fold(params.get("busca", "").strip())
    categorias = set(params.getlist("categoria"))
    regiao = params.get("regiao") or ""
    bairro = params.get("bairro") or ""
    dias = set(params.getlist("dia"))
    periodo = params.get("periodo") or ""
    idade_qualquer = "idade_qualquer" in params
    idade = params.get("idade", type=int)
    somente_com_vaga = "somente_com_vaga" in params
    vaga_pcd = "vaga_pcd" in params

    period_range = TIME_PERIODS.get(periodo)

    result = []
    for turma in classes:
        if categorias and turma["categoria"] not in categorias:
            continue
        if regiao and turma["regiao"] != regiao:
            continue
        if bairro and turma["bairro"] != bairro:
            continue

        if busca:
            haystack = _fold(
                " ".join(filter(None, [turma["curso"], turma["local"], turma["bairro"]]))
            )
            if busca not in haystack:
                continue

        if dias:
            turma_dias = set(normalize_weekdays(turma["dias_semana"]))
            if not turma_dias & dias:
                continue

        if period_range and turma["horario_inicio"]:
            _, start, end = period_range
            if not (start <= turma["horario_inicio"] <= end):
                continue

        if not idade_qualquer and idade is not None:
            turma_min = turma["idade_min"] if turma["idade_min"] is not None else IDADE_MIN
            turma_max = turma["idade_max"] if turma["idade_max"] is not None else IDADE_MAX
            if not (turma_min <= idade <= turma_max):
                continue

        vagas = turma["vagas_disponiveis"] or 0
        if somente_com_vaga and vagas <= 0:
            continue

        if vaga_pcd and not (turma["vagas_pcd"] or 0) > 0:
            continue

        result.append(turma)

    return result
