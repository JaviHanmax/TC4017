# A01411206_A4.2

Repositorio para la **Actividad 4.2** con los tres ejercicios solicitados en Python:

- `computeStatistics.py`
- `convertNumbers.py`
- `wordCount.py`

Los tres programas cumplen con lo pedido en la actividad:

- ejecución por línea de comandos,
- lectura de archivo como parámetro,
- manejo de datos inválidos sin detener la ejecución,
- salida en consola y en archivo,
- medición de tiempo de ejecución,
- apego a PEP 8,
- revisión con `pylint`.

## Estructura del repositorio

```text
A01411206_A4.2/
├── computeStatistics.py
├── convertNumbers.py
├── wordCount.py
├── requirements.txt
├── README.md
├── data/
│   ├── statistics_test.txt
│   ├── converter_test.txt
│   └── words_test.txt
└── evidence/
    ├── compute_statistics_console.txt
    ├── convert_numbers_console.txt
    ├── word_count_console.txt
    ├── StatisticsResults.txt
    ├── ConvertionResults.txt
    ├── WordCountResults.txt
    └── pylint_report.txt
```

## Requisitos de la actividad

De acuerdo con el documento, el primer programa debe llamarse `computeStatistics.py` y calcular media, mediana, moda, desviación estándar y varianza usando algoritmos básicos, imprimiendo resultados en pantalla y en `StatisticsResults.txt`. También debe continuar aun cuando existan datos inválidos y reportar el tiempo de ejecución. El segundo debe llamarse `convertNumbers.py`, convertir números a binario y hexadecimal y guardar los resultados en `ConvertionResults.txt`. El tercero debe llamarse `wordCount.py`, identificar palabras distintas y sus frecuencias, guardar los resultados en `WordCountResults.txt`, y también manejar datos inválidos y tiempo de ejecución. fileciteturn1file0 fileciteturn1file2 fileciteturn1file1

## Instalación

```bash
python -m pip install -r requirements.txt
```

O directamente:

```bash
python -m pip install pylint
```

## Ejecución

### 1) Estadística descriptiva

```bash
python computeStatistics.py data/statistics_test.txt
```

Salida adicional generada:

- `StatisticsResults.txt`

### 2) Conversión a binario y hexadecimal

```bash
python convertNumbers.py data/converter_test.txt
```

Salida adicional generada:

- `ConvertionResults.txt`

### 3) Conteo de palabras

```bash
python wordCount.py data/words_test.txt
```

Salida adicional generada:

- `WordCountResults.txt`

## Validación con pylint

```bash
pylint computeStatistics.py convertNumbers.py wordCount.py
```

Resultado incluido en:

- `evidence/pylint_report.txt`

## Notas importantes

- `computeStatistics.py` usa **varianza poblacional** y **desviación estándar poblacional**.
- `convertNumbers.py` acepta enteros positivos, negativos y cero.
- `wordCount.py` normaliza las palabras a minúsculas y limpia caracteres no alfanuméricos para hacer el conteo más consistente.
- Los archivos dentro de `data/` son **pruebas de ejemplo**.
