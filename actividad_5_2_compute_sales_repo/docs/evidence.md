# Evidencias – Actividad 5.2 (Compute Sales)

> **Nota:** este archivo es una plantilla. Llena/pega la salida real de tu ejecución.
> La actividad solicita registrar ejecución, casos de prueba y evidencias. fileciteturn0file0L29-L33

---

## 1) Ejecución del programa (con archivos de ejemplo)

Comando:

```bash
python computeSales.py data/priceCatalogue.json data/salesRecord.json
```

Evidencia (pega aquí la salida de consola):

```text
[ERROR] Unknown product at $[2].items[0]: 'unknown_product'
[ERROR] Quantity must be > 0 at $[2].items[1].quantity: -2
[ERROR] Invalid product value at $[3].items[0].product: 123
[ERROR] Invalid numeric value at $[3].items[1].quantity: 'two'
Sales Results
=============

Price catalogue file: data/priceCatalogue.json
Sales record file:   data/salesRecord.json

Line items processed: 5
Line items skipped:   1

TOTAL COST: 81.75

Time elapsed: 0.003579 seconds

Notes:
- Any invalid entries are reported to the console and skipped.
- Total cost is computed as sum(price(product) * quantity) for each valid line item.

```

Archivo generado:

- `SalesResults.txt` (adjunta/copia su contenido aquí si te lo piden)

---

## 2) Pruebas unitarias

Comando:

```bash
python -m unittest -v
```

Evidencia (pega aquí la salida de consola):

```text
test_compute_total_skips_unknown_product (tests.test_compute_sales.TestComputeSales.test_compute_total_skips_unknown_product) ... [ERROR] Unknown product at $[1]: 'missing'
ok
test_end_to_end_example_files (tests.test_compute_sales.TestComputeSales.test_end_to_end_example_files) ... [ERROR] Unknown product at $[2].items[0]: 'unknown_product'
[ERROR] Quantity must be > 0 at $[2].items[1].quantity: -2
[ERROR] Invalid product value at $[3].items[0].product: 123
[ERROR] Invalid numeric value at $[3].items[1].quantity: 'two'
ok
test_iter_line_items_finds_nested_items (tests.test_compute_sales.TestComputeSales.test_iter_line_items_finds_nested_items) ... ok
test_iter_line_items_supports_map (tests.test_compute_sales.TestComputeSales.test_iter_line_items_supports_map) ... ok
test_load_json_missing_returns_empty (tests.test_compute_sales.TestComputeSales.test_load_json_missing_returns_empty) ... [ERROR] File not found: does_not_exist.json
ok
test_parse_price_catalogue_dict (tests.test_compute_sales.TestComputeSales.test_parse_price_catalogue_dict) ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.002s

OK

```

---

## 3) Instalación de Flake8 y Pylint

Comando:

```bash
python -m pip install -r requirements-dev.txt
```

Evidencia:

```text
(pegue aquí)
```

---

## 4) Ejecución de Flake8

Comando:

```bash
flake8 .
```

Evidencia:

```text
(pegue aquí)
```

> Si aparece algún error (E***/W***/F***/C9**), corrige el código y vuelve a correr `flake8 .`

---

## 5) Ejecución de Pylint

Comando:

```bash
pylint computeSales.py
```

Evidencia:

```text
(pegue aquí)
```

---

## 6) Confirmación de que el programa sigue funcionando

Vuelve a correr:

```bash
python computeSales.py data/priceCatalogue.json data/salesRecord.json
```

y pega nuevamente la salida si cambiaste algo.
