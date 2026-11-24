# Gestor de préstamos de libros

Aplicación de consola para que el bibliotecario de una pequeña biblioteca universitaria administre
el catálogo y registre préstamos y devoluciones. Proyecto del taller de Spec-Driven Development
asistido por IA.

- Intención del proyecto: [docs/intent.md](docs/intent.md)
- Registro de interacciones con la IA: [agent/prompts/](agent/prompts/)

## Pruebas

Desde la raíz del proyecto, sin variables de entorno ni dependencias de terceros (solo `unittest`):

```
python -m unittest discover -s tests -t .
```

Resultado esperado: todas las pruebas pasan y el comando termina con código 0.
