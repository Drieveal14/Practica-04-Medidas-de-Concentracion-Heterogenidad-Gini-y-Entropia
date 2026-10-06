import numpy as np


def validar_proporciones(pi):
    """
    Convierte las proporciones a un vector numérico y valida
    que sean finitas, no negativas y no vacías.
    """

    p = np.asarray(pi, dtype=float)

    if p.ndim != 1 or p.size == 0:
        raise ValueError(
            "Se requiere un vector unidimensional no vacío."
        )

    if not np.isfinite(p).all():
        raise ValueError(
            "Todas las proporciones deben ser finitas."
        )

    if np.any(p < 0):
        raise ValueError(
            "Las proporciones deben ser no negativas."
        )

    if np.sum(p) <= 0:
        raise ValueError(
            "La suma de las proporciones debe ser mayor que cero."
        )

    # Normalizamos por seguridad para que la suma sea 1.
    p = p / np.sum(p)

    return p


def gini_simpson(pi):
    """
    Calcula el índice de Gini-Simpson.

    Valores cercanos a 0 indican baja heterogeneidad.
    Valores mayores indican mayor diversidad entre categorías.
    """

    p = validar_proporciones(pi)

    return float(
        1 - np.sum(p ** 2)
    )


def iqv(pi):
    """
    Calcula el Índice de Variación Cualitativa (IQV).

    IQV = 0 indica heterogeneidad nula.
    IQV = 1 indica heterogeneidad máxima.
    """

    p = validar_proporciones(pi)

    k = p.size

    if k <= 1:
        return 0.0

    gs = gini_simpson(p)

    return float(
        (k * gs) / (k - 1)
    )


def entropia_shannon(pi):
    """
    Calcula la entropía de Shannon utilizando logaritmo base 2.
    """

    p = validar_proporciones(pi)

    # Se ignoran proporciones iguales a 0 porque:
    # lim p*log2(p), cuando p -> 0, es 0.
    p_positivas = p[p > 0]

    entropia = -np.sum(
        p_positivas * np.log2(p_positivas)
    )

    return float(entropia)


def medidas_heterogeneidad(pi):
    """
    Calcula en conjunto Gini-Simpson, IQV y entropía de Shannon.
    """

    p = validar_proporciones(pi)

    k = p.size

    return {
        "categorias": int(k),
        "gini_simpson": gini_simpson(p),
        "iqv": iqv(p),
        "entropia_shannon": entropia_shannon(p),
        "entropia_maxima": float(np.log2(k)) if k > 0 else 0.0,
    }