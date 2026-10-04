<div style="text-align: left;">
  <img width="200" src="https://www.fciencias.unam.mx/sites/default/files/logoFC_2.png" alt="Logo FC">
</div>
# Práctica 4. Medidas de Concentración, Heterogeneidad, Gini y Entropía
## ENDIREH 2021: Violencia contra las Mujeres

## 1. Objetivo de la practica

calcular e interpretar correctamente medidas de localizacion, medidas de variabilidad, medidas de heterogeneidad y medidas de concentracion, incluyendo especıficamente el coeficiente de Gini y la entropıa de Shannon, y las comunique mediante visualizaciones de datos adecuadas. Mas alla del calculo mecanico, se busca la reflexion crıtica sobre lo que estas medidas revelan y lo que ocultan acerca del fenomeno de la violencia contra las mujeres, y sobre como estos hallazgos deben orientar decisiones posteriores del proyecto (mejoras al preprocesamiento, seleccion de variables para modelado, comunicacion responsable de resultados).

## 2. Fuente de los datos

- **Archivo utilizado:** el CSV proporcionado por classroom, eliminando el prefijo del nombre:
  `endireh_ml_dataset_texto_fecha.csv`
- Se tiene que agregar manualmente a la carpeta `data/data-raw/` quitando el nombre propio y apellidos.
- **Base conservada de la Práctica 3:** `data/data-processed/endireh_2021_limpio.csv`.
- **Entrada de la Práctica 4:** `data/data-processed/endireh_2021_renombrado.csv`, generado a partir del CSV limpio en `notebooks/ajuste_columnas_practica_4.ipynb`.

## 3. Estructura del proyecto

```
proyecto-endireh-violencia/
   config/
      rutas.py             # Rutas de archivos estaticos
   data/
      data-raw/            # Datos originales, tal como se descargaron (nunca se editan)
      data-processed/      # Datos ya limpios: sin duplicados, tipos corregidos, imputados
      data-input-model/    # Datos ya transformados y listos como entrada de un modelo
      data-model/          # Salidas del modelo: predicciones, clusters, reglas obtenidas
   src/
      cleaning/            # Scripts de limpieza y preprocesamiento
      statistics/          # Funciones estadísticas reutilizables
      visualization/       # Scripts de graficas y EDA
      models/              # Scripts de entrenamiento y evaluacion de modelos
   notebooks/              # Notebooks exploratorios (no productivos)
   README.md               # Documentacion del proyecto
   requirements.txt        # Dependencias exactas del proyecto
```


## 4. Instalación del entorno

### 4.1 Requisitos previos

| Herramienta | Versión | Para qué se usa |
|---|---|---|
| Python | 3.10 o superior | Lenguaje base del proyecto |
| pip | Incluido con Python | Instalación de dependencias |
| Git | Cualquier versión reciente | Control de versiones |
| VS Code o Jupyter | Cualquiera | Ejecutar el notebook |

### 4.2 Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd proyecto-endireh-violencia
```

### 4.3 Crear y activar el entorno virtual

Crea el entorno, en la raíz del proyecto:

```bash
python3 -m venv .venv
```

Activalo (cada vez que se abra una terminal nueva):

```bash
source .venv/bin/activate
```

### 4.4 Instalar las dependencias

Con el entorno activado:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Colocar los datos

1. Descarga el CSV de la práctica desde **Classroom**.
2. **Renómbralo** quitando solo el nombre propio del prefijo, de modo que el archivo se
   llame exactamente:

   ```
   endireh_ml_dataset_texto_fecha.csv
   ```
3. Colócalo dentro de `data/data-raw/`.

Esto asegura que todo el equipo use el mismo nombre de archivo, definido en
`config/rutas.py`:

```python
RUTA_ENDIREH_CSV = RUTA_DATA_RAW / "endireh_ml_dataset_texto_fecha.csv"
```


### Rutas y carga de datos

Las rutas de los archivos se definen en `config/rutas.py`:

- `RUTA_ENDIREH_CSV`: datos crudos; se conservan sin cambios.
- `RUTA_ENDIREH_LIMPIO_CSV`: base procesada de la Práctica 3; se conserva.
- `RUTA_ENDIREH_RENOMBRADO_CSV`: derivado con nombres corregidos para los cinco análisis.

Los notebooks detectan la raíz del proyecto desde la carpeta raíz o desde
`notebooks/`, importan las librerías y cargan el CSV procesado con Polars.
Comprueban la presencia de las columnas necesarias para su análisis y muestran
una vista previa.

### Notebooks preparados

| Archivo | Contenido |
|---|---|
| `notebooks/ajuste_columnas_practica_4.ipynb` | Generación del CSV con columnas renombradas y nombres geográficos corregidos |
| `notebooks/medidas_de_localizacion.ipynb` | Localización completada: medidas ponderadas, comparación por grupos e histograma |
| `notebooks/medidas_de_variabilidad.ipynb` | Variabilidad completada: CV, IQR, boxplot,
| `notebooks/medidas_de_heteregionidad.ipynb` | Heterogeneidad |
| `notebooks/medidas_de_concentracion.ipynb` | Concentración |
| `notebooks/Comparacion_gini_y_entropia.ipynb` | Comparación de Gini y entropía |

### Ajuste para la Práctica 4

Ejecuta de principio a fin `notebooks/ajuste_columnas_practica_4.ipynb` con el
entorno Python `endireh`. El notebook carga el CSV limpio, muestra la tabla de
correspondencias, renombra las columnas y corrige los textos geográficos cuya
codificación está dañada. También recupera desde el archivo original los códigos
válidos de 0 a 9 de `anios_sin_convivencia_pareja`, tras comprobar la
correspondencia fila a fila con el CSV limpio. Verifica que la recuperación
conserve las demás columnas, los registros y su orden antes de escribir el CSV.

El trabajo de la Práctica 3 se conserva. Solo en el derivado de P4 se corrige el
filtro de 10 años aplicado a la columna entonces llamada `edad_primer_union`:
se recuperan **14,252 valores originales**, sin imputar. El código 0 significa
**menos de un año**; los códigos 98 (no se acuerda), 99 (no especificado) y los
blancos permanecen nulos. Se conserva la misma estructura de 110,127 filas y
24 columnas. El ajuste no modifica códigos especiales de ingreso.
