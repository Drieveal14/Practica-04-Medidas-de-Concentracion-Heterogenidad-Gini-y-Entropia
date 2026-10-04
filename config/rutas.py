from pathlib import Path

# Carpeta raíz del proyecto
RUTA_PROYECTO = Path(__file__).resolve().parent.parent

# Carpetas de datos
RUTA_DATA = RUTA_PROYECTO / "data"

RUTA_DATA_RAW = RUTA_DATA / "data-raw"
RUTA_DATA_PROCESSED = RUTA_DATA / "data-processed"
RUTA_DATA_INPUT_MODEL = RUTA_DATA / "data-input-model"
RUTA_DATA_MODEL = RUTA_DATA / "data-model"

# Carpetas de código y notebooks
RUTA_SRC = RUTA_PROYECTO / "src"
RUTA_NOTEBOOKS = RUTA_PROYECTO / "notebooks"


# Se tiene que renombrar el nombre del archivo a este (Que es quitando solo el nombre propio) para
# para manejar un mismo nombre de archivo todos
RUTA_ENDIREH_CSV = RUTA_DATA_RAW / "endireh_ml_dataset_texto_fecha.csv"

# Entrada de los analisis de la Práctica 4
RUTA_ENDIREH_LIMPIO_CSV = RUTA_DATA_PROCESSED / "endireh_2021_limpio.csv"

# Derivado para la Practica 4, generado desde el CSV limpio en un notebook.
RUTA_ENDIREH_RENOMBRADO_CSV = RUTA_DATA_PROCESSED / "endireh_2021_renombrado.csv"

# Entregables de la persona 1.
RUTA_RESULTADOS_PERSONA_1 = RUTA_PROYECTO / "reports" / "persona_1"
RUTA_FIGURAS_PERSONA_1 = RUTA_RESULTADOS_PERSONA_1 / "figuras"
RUTA_HISTOGRAMA_PERSONA_1 = RUTA_FIGURAS_PERSONA_1 / "histograma_ponderado.png"
RUTA_BOXPLOT_PERSONA_1 = RUTA_FIGURAS_PERSONA_1 / "boxplot_ponderado.png"
