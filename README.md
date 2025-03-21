
📦 **Usar esta biblioteca en desarrollo (modo editable)**

Si estás trabajando en el desarrollo de esta biblioteca, puedes instalarla de forma que los cambios que hagas en el código se reflejen automáticamente, sin tener que reinstalarla.

🔹 **Pasos para instalación en modo editable**

1. Abre una terminal y navega a la raíz del proyecto, donde está el archivo `setup.py`.
2. Ejecuta el siguiente comando:

    ```bash
    pip install -e .
    ```

    El argumento `-e` significa editable, y el `.` indica que se instalará la biblioteca desde la carpeta actual.

📁 **Estructura típica del proyecto**

```bash
mi_libreria/               # Raíz del proyecto
├── mi_libreria/           # Código fuente de la biblioteca
│   ├── __init__.py
│   └── modulo.py
├── setup.py               # Configuración para instalación
├── README.md
```

📌 **Notas**

- Se debe ejecutar el comando `pip install -e .` desde la raíz del proyecto, **NO** dentro de la carpeta de código.
- Si estás usando un entorno virtual (venv, poetry, etc.), la instalación solo se aplicará dentro de ese entorno.
- Puedes probar la biblioteca importándola normalmente desde cualquier archivo Python:

    ```python
    from mi_libreria import modulo
    ```