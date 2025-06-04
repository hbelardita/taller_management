# Sistema de Gestión de Taller Escolar

Este proyecto es una aplicación de terminal en Python diseñada para gestionar usuarios, herramientas, mantenimientos y asignaciones/préstamos dentro de un taller escolar.

## Características Implementadas (hasta ahora)

### Gestión de Usuarios
*   **Crear Usuario:** Permite registrar nuevos usuarios (Estudiantes, Personal, Administradores) con campos específicos según el tipo.
*   **Editar Usuario:** Permite modificar la información de usuarios existentes.
*   **Eliminar Usuario:** Permite eliminar usuarios del sistema con confirmación.
*   **Listar Usuarios:** Muestra un listado de todos los usuarios registrados.
*   **Buscar Usuario:** (En desarrollo)

### Gestión de Herramientas y Máquinas
*   (En desarrollo)

### Gestión de Mantenimientos
*   (En desarrollo)

### Gestión de Asignaciones / Préstamos
*   (En desarrollo)



## Configuración del Entorno

Para ejecutar este proyecto, se recomienda crear y activar un entorno virtual de Python.

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/hbelardita/taller_management
    cd taller_management
    ```

2.  **Crear y activar el entorno virtual:**
    ```bash
    python -m venv .venv
    ```
    *   **Windows:**
        ```bash
        .venv\Scripts\activate
        ```
    *   **macOS/Linux:**
        ```bash
        source .venv/bin/activate
        ```

3.  **Instalar dependencias:**
    Actualmente, el proyecto no tiene dependencias externas más allá de las librerías estándar de Python. Si en el futuro se añaden, se listarían aquí y se instalarían con `pip install -r requirements.txt`.

## Ejecución del Proyecto

Una vez que el entorno virtual esté activado, puedes ejecutar la aplicación principal:

```bash
python main.py
