# Actividad 5.2 – Compute Sales

Este repositorio implementa el programa **`computeSales.py`** para la *Actividad 5.2* (Compute sales).

## Requisitos del ejercicio

- Ejecutar desde línea de comandos y recibir **2 archivos JSON**: catálogo de precios y registro de ventas. 
- Calcular el costo total de todas las ventas e imprimirlo en pantalla y en **`SalesResults.txt`**.
- Manejar datos inválidos: mostrar errores en consola y **continuar** la ejecución. 
- Incluir el **tiempo transcurrido** en consola y en el archivo de resultados.
- Cumplir PEP-8. 

## Ejecución

```bash
python computeSales.py data/priceCatalogue.json data/salesRecord.json
```

Al finalizar:
- Se despliega el reporte en consola.
- Se creará o actualizará `SalesResults.txt` en el directorio actual.

## Formatos JSON soportados (tolerante)

### Catálogo de precios
Soporta:
- Mapa `{ "producto": 10.5, "otro": 7 }`
- Lista `[{ "product": "producto", "price": 10.5 }, ...]` (también acepta `name/title/id/sku` y `cost/value`)

### Registro de ventas
Soporta estructuras anidadas: busca objetos tipo `{ "product": "...", "quantity": ... }` en listas/diccionarios.
También soporta un mapa plano `{ "producto": 2, "otro": 1 }`.

Si detecta:
- producto no existente en catálogo
- cantidad inválida (no numérica o <= 0)
- entradas mal formadas

…lo reporta como error y omite esa línea (sin detener el programa).

## Pruebas unitarias (unittest)

```bash
python -m unittest -v
```

## Flake8 y Pylint (linters)

1) Instala dependencias (en tu venv):

```bash
python -m pip install -r requirements-dev.txt
```

2) Ejecuta linters:

```bash
flake8 .
pylint computeSales.py
```

> En `docs/evidence.md` tienes un formato sugerido para documentar evidencias (comandos + salidas).

## Estructura

- `computeSales.py` – programa principal
- `data/` – JSON de ejemplo
- `tests/` – pruebas unitarias
- `docs/evidence.md` – plantilla de evidencias
- `.flake8`, `.pylintrc` – configuración de linters
