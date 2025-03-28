# Guia para Desarrolladores
Esta guía está dirigida a desarrolladores que deseen contribuir al desarrollo de la biblioteca `slidepyv6`.

🧑🏽‍💻 **Para la contribución en el desarrollo de esta biblioteca deberás:**

    1. Haz fork del repositorio
    2. Crea una rama (git checkout -b feature/nueva-funcionalidad)
    3. Realiza commits descriptivos
    4. Haz push a la rama (git push origin feature/nueva-funcionalidad)
    5. Abre un Pull Request   



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
SlidePyV6-Library/               # Raíz del proyecto
├── slidepyv6/           # Código fuente de la biblioteca
│   ├── __init__.py
│   └── core.py
├── setup.py               # Configuración para instalación
├── README.md
```

📌 **Notas**

- Se debe ejecutar el comando `pip install -e .` desde la raíz del proyecto, **NO** dentro de la carpeta de código.
- Si estás usando un entorno virtual (venv, poetry, etc.), la instalación solo se aplicará dentro de ese entorno.
- Puedes probar la biblioteca importándola normalmente desde cualquier archivo Python:

    ```python
    from slidepyv6 import SlideProject
    ```

- Si necesitas desinstalar la biblioteca en modo editable, puedes hacerlo con el comando:

    ```bash
    pip uninstall slidepyv6
    ```
