"""Medidas descriptivas de localizacion y variabilidad para la Practica 4."""
import numpy as np
import polars as pl

VARIABLE = "anios_sin_convivencia_pareja"
GRUPOS = (("Total disponible", None), ("No reporto violencia", 0), ("Reporto violencia", 1))
UNIVERSO_CUESTIONARIOS = ("A2", "B1", "B2")


def validar_vectores(valores, pesos=None):
    """Exige valores y pesos finitos, no vacios y pesos estrictamente positivos."""
    x = np.asarray(valores, dtype=float)
    w = np.ones_like(x) if pesos is None else np.asarray(pesos, dtype=float)
    if x.ndim != 1 or w.shape != x.shape or x.size == 0:
        raise ValueError("Se requieren vectores no vacios de la misma longitud.")
    if not np.isfinite(x).all() or not np.isfinite(w).all() or np.any(w <= 0):
        raise ValueError("Los valores deben ser finitos y los pesos positivos y finitos.")
    # Normalizar evita desbordamientos; los resultados no dependen de la escala de w.
    w = w / np.max(w)
    return x, w


def cuantiles_ponderados(valores, probabilidades, pesos=None):
    """Cuantiles de la CDF empirica inversa, sin interpolar entre observaciones."""
    x, w = validar_vectores(valores, pesos)
    q = np.asarray(probabilidades, dtype=float)
    if not np.isfinite(q).all() or np.any((q < 0) | (q > 1)):
        raise ValueError("Las probabilidades deben estar entre 0 y 1.")
    return np.quantile(x, q, weights=w, method="inverted_cdf")


def medidas_localizacion(valores, pesos=None):
    x, w = validar_vectores(valores, pesos)
    p10, q1, mediana, q3, p90 = cuantiles_ponderados(x, [.10, .25, .50, .75, .90], w)
    unicos, inverso = np.unique(x, return_inverse=True)
    masas = np.bincount(inverso, weights=w)
    # Ante empates se incluyen todas las modas, en orden ascendente.
    modas = unicos[np.isclose(masas, masas.max(), rtol=1e-12, atol=0)]
    return {
        "media": float(np.average(x, weights=w)), "mediana": float(mediana),
        "p10": float(p10), "q1": float(q1), "q3": float(q3), "p90": float(p90),
        "moda": ", ".join(f"{v:g}" for v in modas),
    }


def medidas_variabilidad(valores, pesos=None):
    x, w = validar_vectores(valores, pesos)
    media = float(np.average(x, weights=w))
    # Varianza de la distribucion descriptiva: divisor suma de pesos, sin ddof=1.
    varianza = float(np.average((x - media) ** 2, weights=w))
    desviacion = float(np.sqrt(varianza))
    q1, q3 = cuantiles_ponderados(x, [.25, .75], w)
    return {
        "media": media, "minimo": float(x.min()), "maximo": float(x.max()),
        "rango": float(np.ptp(x)), "varianza": varianza,
        "desviacion_estandar": desviacion,
        "cv_porcentaje": None if media <= 0 else 100 * desviacion / media,
        "q1": float(q1), "q3": float(q3), "iqr": float(q3 - q1),
    }


def preparar_base(df):
    """Selecciona casos disponibles del universo A2/B1/B2 sin imputar ni deduplicar."""
    requeridas = {VARIABLE, "factor_expansion", "sufrio_violencia_pareja", "tipo_cuestionario"}
    faltantes = requeridas.difference(df.columns)
    if faltantes:
        raise ValueError(f"Faltan columnas: {sorted(faltantes)}")
    if df.is_empty():
        raise ValueError("El dataset está vacío.")
    if df.filter(~pl.col("sufrio_violencia_pareja").is_in([0, 1]).fill_null(False)).height:
        raise ValueError("El indicador de violencia debe contener unicamente 0 y 1.")
    fuera = df.filter(
        pl.col(VARIABLE).is_not_null()
        & ~pl.col("tipo_cuestionario").is_in(UNIVERSO_CUESTIONARIOS).fill_null(False)
    )
    if fuera.height:
        raise ValueError("Hay tiempos disponibles fuera del universo A2/B1/B2; revisar la codificacin.")
    universo = df.filter(pl.col("tipo_cuestionario").is_in(UNIVERSO_CUESTIONARIOS))
    disponibles = universo.drop_nulls(subset=[VARIABLE])
    x = pl.col(VARIABLE).cast(pl.Float64)
    w = pl.col("factor_expansion").cast(pl.Float64)
    if disponibles.filter(~(x.is_finite() & x.is_between(0, 97)).fill_null(False)).height:
        raise ValueError("Se detectaron tiempos invalidos o codigos especiales; revisar antes de analizar.")
    if disponibles.filter(~(w.is_finite() & (w > 0)).fill_null(False)).height:
        raise ValueError("Hay factores de expansion invalidos en los casos disponibles.")
    if disponibles.is_empty():
        raise ValueError("No hay tiempos disponibles para analizar.")
    cobertura = []
    for nombre, codigo in GRUPOS:
        original = df if codigo is None else df.filter(pl.col("sufrio_violencia_pareja") == codigo)
        elegibles = universo if codigo is None else universo.filter(pl.col("sufrio_violencia_pareja") == codigo)
        base = disponibles if codigo is None else disponibles.filter(pl.col("sufrio_violencia_pareja") == codigo)
        cobertura.append({
            "grupo": nombre, "n_dataset": original.height, "n_universo_a2_b1_b2": elegibles.height,
            "n_disponibles": base.height, "n_faltantes_en_universo": elegibles.height - base.height,
            "porcentaje_disponible_dataset": 100 * base.height / original.height if original.height else None,
            "porcentaje_disponible_universo": 100 * base.height / elegibles.height if elegibles.height else None,
        })
    return disponibles, pl.DataFrame(cobertura)


def resumir_por_grupo(base, familia):
    funciones = {"localizacion": medidas_localizacion, "variabilidad": medidas_variabilidad}
    if familia not in funciones:
        raise ValueError("Familia no reconocida.")
    filas = []
    for nombre, codigo in GRUPOS:
        datos = base if codigo is None else base.filter(pl.col("sufrio_violencia_pareja") == codigo)
        if datos.is_empty():
            raise ValueError(f"No hay observaciones en el grupo {nombre}.")
        x = datos[VARIABLE].to_numpy()
        w = datos["factor_expansion"].to_numpy()
        for etiqueta, pesos in (("Sin ponderar", None), ("Factor de expansión", w)):
            filas.append({
                "grupo": nombre, "ponderacion": etiqueta, "n": datos.height,
                **funciones[familia](x, pesos),
            })
    return pl.DataFrame(filas)
