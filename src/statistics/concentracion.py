"""Medidas de concentración territorial para la Práctica 4"""
import numpy as np

def validar_valores_no_negativos(valores):
    """
    Convierte los valores a un vector numérico y valida que sean finitos, no negativos y no vacios
    """

    x = np.asarray(valores, dtype=float)

    if x.ndim != 1 or x.size == 0:
        raise ValueError(
            "Se requiere un vector unidimensional no vacio"
        )

    if not np.isfinite(x).all():
        raise ValueError(
            "Todos los valores deben ser finitos"
        )

    if np.any(x < 0):
        raise ValueError(
            "Los valores deben ser no negativos"
        )

    return x


def coeficiente_gini(valores):
    """
    Gini Cercano a 0: distribución más uniforme.
    Gini Mayor: mayor concentración.
    """

    x = validar_valores_no_negativos(valores)

    if np.all(x == 0):
        return 0.0

    x = np.sort(x)

    n = x.size
    indices = np.arange(1, n + 1)

    gini = (
        np.sum(
            (2 * indices - n - 1) * x
        )
        / (n * np.sum(x))
    )

    return float(gini)


def curva_lorenz(valores):
    """
    proporcion_unidades: Proporción acumulada de entidades
    proporcion_valores: Proporción acumulada de los casos
    """

    x = validar_valores_no_negativos(valores)

    x = np.sort(x)

    acumulados = np.cumsum(x)

    proporcion_unidades = np.linspace(
        0,
        1,
        x.size + 1
    )

    if acumulados[-1] == 0:
        proporcion_valores = np.zeros(
            x.size + 1
        )
    else:
        proporcion_valores = np.insert(
            acumulados / acumulados[-1],
            0,
            0,
        )

    return (
        proporcion_unidades,
        proporcion_valores,
    )