# Gestor de préstamos de libros

Aplicación de consola para que el bibliotecario de una pequeña biblioteca universitaria administre
el catálogo y registre préstamos y devoluciones. Proyecto del taller de Spec-Driven Development
asistido por IA.

- Intención del proyecto: [docs/intent.md](docs/intent.md)
- Registro de interacciones con la IA: [agent/prompts/](agent/prompts/)

## Uso

Requisitos: Python 3.12 o superior. Solo usa la biblioteca estándar; no hay que instalar nada.

Desde la raíz del proyecto:

```
python src/gestor_prestamos/__main__.py
```

Desde cualquier otra carpeta, use la ruta completa al mismo archivo, por ejemplo
`python C:\ruta\al\proyecto\src\gestor_prestamos\__main__.py`.

- Se abre un menú numerado: registrar libro, consultar catálogo, registrar préstamo, registrar
  devolución, consultar préstamos vencidos y salir. Las fechas se escriben como `DD/MM/AAAA`.
- **Datos:** se guardan en `ops/biblioteca.json` dentro del proyecto, sin importar la carpeta desde
  la que se ejecute. El archivo no se versiona en Git (`ops/.gitignore`).
- **Respaldo:** basta con copiar `ops/biblioteca.json`. Para restaurarlo, copie el respaldo de
  vuelta con la aplicación cerrada.
- Si el archivo de datos está dañado, la aplicación muestra el error y termina sin modificarlo.

## Pruebas

Desde la raíz del proyecto, sin variables de entorno ni dependencias de terceros (solo `unittest`):

```
python -m unittest discover -s tests -t .
```

Resultado esperado: todas las pruebas pasan y el comando termina con código 0.
