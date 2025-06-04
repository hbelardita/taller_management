
from modules.tool_manager import (
    create_tool, get_all_tools, get_tool_by_id, update_tool, delete_tool,
    update_tool_state, search_tools, get_available_tools,
    get_tools_by_state, VALID_STATES, VALID_TYPES
)
from modules.data_manager import load_json_data, save_json_data
from modules.id_generator import get_next_id
from modules.validators import validate_user_data
from modules.user_manager import (
    create_user, get_user_by_id, get_all_users,
    search_users, update_user, delete_user, format_user_info
)
from modules.enums import UserType, ToolState, ToolType


"""
Test del módulo de gestión de herramientas.
"""


def test_tool_crud():
    """Prueba las operaciones CRUD de herramientas."""
    print("=== Prueba del Sistema CRUD de Herramientas ===\n")

    # 1. Crear herramienta eléctrica
    electric_tool_data = {
        "name": "Taladro de Banco Bosch PBD 40",
        "type": "Máquina Eléctrica",
        "brand": "Bosch",
        "model": "PBD 40",
        "serial_number": "BSH2024001",
        "state": "Disponible",
        "location": "Taller de Carpintería - Estante A",
        "acquisition_date": "2024-01-15",
        "notes": "Taladro principal del taller de carpintería"
    }

    success, message, tool_id_1 = create_tool(electric_tool_data)
    print(f"Crear herramienta eléctrica: {success}")
    print(f"Mensaje: {message}")
    if success:
        print(f"ID asignado: {tool_id_1}")
    print()

    # 2. Crear kit de herramientas manuales
    manual_tool_data = {
        "name": "Kit de Destornilladores Phillips",
        "type": "Herramienta Manual",
        "brand": "Stanley",
        "model": "STHT60028",
        "serial_number": "",
        "state": "Disponible",
        "location": "Taller de Electrónica - Armario 3",
        "acquisition_date": "2024-02-20",
        "notes": "Kit completo con 6 tamaños diferentes"
    }

    success, message, tool_id_2 = create_tool(manual_tool_data)
    print(f"Crear herramienta manual: {success}")
    print(f"Mensaje: {message}")
    if success:
        print(f"ID asignado: {tool_id_2}")
    print()

    # 3. Crear equipo de medición
    measurement_tool_data = {
        "name": "Multímetro Digital Fluke 117",
        "type": "Equipo de Medición",
        "brand": "Fluke",
        "model": "117",
        "serial_number": "FLK117-2024-005",
        "state": "Disponible",
        "location": "Laboratorio de Electrónica - Mesa 1",
        "acquisition_date": "2024-03-10",
        "notes": "Multímetro profesional para mediciones precisas"
    }

    success, message, tool_id_3 = create_tool(measurement_tool_data)
    print(f"Crear equipo de medición: {success}")
    print(f"Mensaje: {message}")
    if success:
        print(f"ID asignado: {tool_id_3}")
    print()

    # 4. Intentar crear herramienta con datos inválidos
    invalid_tool_data = {
        "name": "",  # Nombre vacío
        "type": "Tipo Inexistente",  # Tipo inválido
        "state": "Estado Inválido",  # Estado inválido
        "location": "",  # Ubicación vacía
        "acquisition_date": "fecha-inválida"  # Fecha mal formateada
    }

    success, message, _ = create_tool(invalid_tool_data)
    print(f"Crear herramienta inválida: {success}")
    print(f"Mensaje: {message}\n")

    return tool_id_1, tool_id_2, tool_id_3


def test_tool_retrieval():
    """Prueba la obtención de herramientas."""
    print("=== Prueba de Obtención de Herramientas ===\n")

    # 1. Obtener todas las herramientas
    all_tools = get_all_tools()
    print(f"Total de herramientas: {len(all_tools)}")
    for tool in all_tools:
        print(f"  - ID {tool['id']}: {tool['name']} ({tool['type']})")
    print()

    # 2. Obtener herramienta por ID
    if all_tools:
        first_tool_id = all_tools[0]['id']
        tool = get_tool_by_id(first_tool_id)
        if tool:
            print(f"Herramienta ID {first_tool_id}:")
            print(f"  Nombre: {tool['name']}")
            print(f"  Tipo: {tool['type']}")
            print(f"  Estado: {tool['state']}")
            print(f"  Ubicación: {tool['location']}")
        else:
            print(f"No se encontró herramienta con ID {first_tool_id}")
    print()


def test_tool_search():
    """Prueba las funciones de búsqueda de herramientas."""
    print("=== Prueba del Sistema de Búsqueda ===\n")

    # 1. Buscar todas las herramientas disponibles
    available_tools = get_available_tools()
    print(f"Herramientas disponibles: {len(available_tools)}")
    for tool in available_tools:
        print(f"  - {tool['name']} ({tool['type']})")
    print()

    # 2. Buscar por tipo usando los nombres de campo correctos (español)
    electric_tools = search_tools({'tipo': 'Máquina Eléctrica'})
    print(f"Máquinas eléctricas: {len(electric_tools)}")
    for tool in electric_tools:
        brand = tool.get('brand', 'Sin marca')
        model = tool.get('model', 'Sin modelo')
        print(f"  - {tool['name']} - {brand} {model}")
    print()

    # 3. Buscar por ubicación
    carpentry_tools = search_tools({'ubicacion': 'Carpintería'})
    print(f"Herramientas en taller de carpintería: {len(carpentry_tools)}")
    for tool in carpentry_tools:
        print(f"  - {tool['name']} en {tool['location']}")
    print()

    # 4. Buscar por marca
    bosch_tools = search_tools({'marca': 'Bosch'})
    print(f"Herramientas marca Bosch: {len(bosch_tools)}")
    for tool in bosch_tools:
        model = tool.get('model', 'Sin modelo')
        print(f"  - {tool['name']} ({model})")
    print()


def test_tool_state_management(tool_id: int):
    """Prueba la gestión de estados de herramientas."""
    print("=== Prueba de Gestión de Estados ===\n")

    if not tool_id:
        print("No hay ID de herramienta para probar")
        return

    # 1. Obtener herramienta actual
    tool = get_tool_by_id(tool_id)
    if tool:
        print(f"Herramienta: {tool['name']}")
        print(f"Estado actual: {tool['state']}")
    print()

    # 2. Cambiar a "En Uso"
    success, message = update_tool_state(tool_id, "En Uso")
    print(f"Cambiar a 'En Uso': {success}")
    print(f"Mensaje: {message}")

    # Verificar cambio
    tool = get_tool_by_id(tool_id)
    if tool:
        print(f"Nuevo estado: {tool.get('estado', tool.get('state', 'N/A'))}")
    print()

    # 3. Cambiar a "En Mantenimiento"
    success, message = update_tool_state(tool_id, "En Mantenimiento")
    print(f"Cambiar a 'En Mantenimiento': {success}")
    print(f"Mensaje: {message}")
    print()

    # 4. Intentar cambiar a estado inválido
    success, message = update_tool_state(tool_id, "Estado Inexistente")
    print(f"Cambiar a estado inválido: {success}")
    print(f"Mensaje: {message}")
    print()

    # 5. Volver a disponible
    success, message = update_tool_state(tool_id, "Disponible")
    print(f"Volver a 'Disponible': {success}")
    print(f"Mensaje: {message}")
    print()


def test_tool_update(tool_id: int):
    """Prueba la actualización completa de herramientas."""
    print("=== Prueba de Actualización de Herramientas ===\n")

    if not tool_id:
        print("No hay ID de herramienta para probar")
        return

    # 1. Mostrar datos actuales
    tool = get_tool_by_id(tool_id)
    if tool:
        print(f"Datos actuales de herramienta ID {tool_id}:")
        print(f"  Nombre: {tool['name']}")
        print(f"  Ubicación: {tool['location']}")
        print(f"  Notas: {tool.get('notes', 'Sin notas')}")
    print()

    # 2. Actualizar datos
    updated_data = {
        "name": tool['name'],  # Mantener nombre
        "type": tool['type'],  # Mantener tipo
        "brand": tool.get('brand', ''),
        "model": tool.get('model', ''),
        "serial_number": tool.get('serial_number', ''),
        "state": tool['state'],
        "location": "Taller Principal - Estante B",  # Nueva ubicación
        "acquisition_date": tool.get('acquisition_date', ''),
        "notes": "Herramienta actualizada - Revisión completa realizada"  # Nuevas notas
    }

    success, message = update_tool(tool_id, updated_data)
    print(f"Actualizar herramienta: {success}")
    print(f"Mensaje: {message}")

    # 3. Verificar actualización
    updated_tool = get_tool_by_id(tool_id)
    if updated_tool:
        print(f"Datos actualizados:")
        print(f"  Ubicación: {updated_tool['location']}")
        print(f"  Notas: {updated_tool.get('notes', 'Sin notas')}")
    print()


def test_tool_deletion(tool_id: int):
    """Prueba la eliminación de herramientas."""
    print("=== Prueba de Eliminación de Herramientas ===\n")

    if not tool_id:
        print("No hay ID de herramienta para probar")
        return

    # 1. Verificar que la herramienta existe
    tool = get_tool_by_id(tool_id)
    if tool:
        print(f"Herramienta a eliminar: {tool['name']}")
    else:
        print(f"Herramienta ID {tool_id} no encontrada")
        return

    # 2. Eliminar herramienta
    success, message = delete_tool(tool_id)
    print(f"Eliminar herramienta: {success}")
    print(f"Mensaje: {message}")

    # 3. Verificar eliminación
    deleted_tool = get_tool_by_id(tool_id)
    if deleted_tool is None:
        print("Herramienta eliminada correctamente")
    else:
        print("Error: La herramienta aún existe")
    print()


def test_tool_validation():
    """Prueba el sistema de validación de herramientas."""
    print("=== Prueba del Sistema de Validación ===\n")

    # Herramienta con múltiples errores
    invalid_tool = {
        "name": "",  # Nombre vacío
        "type": "Tipo Inválido",  # Tipo no válido
        "state": "Estado Inválido",  # Estado no válido
        "location": "",  # Ubicación vacía
        "acquisition_date": "2024-13-45"  # Fecha inválida
    }

    success, message, _ = create_tool(invalid_tool)
    print(f"Herramienta inválida: {success}")
    if not success:
        print(f"Errores: {message}")
    print()


def show_valid_values():
    """Muestra los valores válidos para tipos y estados."""
    print("=== Valores Válidos ===")
    print(f"Estados válidos: {', '.join(VALID_STATES)}")
    print(f"Tipos válidos: {', '.join(VALID_TYPES)}")
    print()


def test_tools_by_state():
    """Prueba la consulta de herramientas por estado."""
    print("=== Herramientas por Estado ===\n")

    for state in VALID_STATES:
        tools = get_tools_by_state(state)
        print(f"{state}: {len(tools)} herramientas")
        for tool in tools:
            print(f"  - {tool['name']}")
        print()


def test_user_crud():
    """Prueba las operaciones CRUD de usuarios usando enums."""
    print("=== Prueba del Sistema CRUD de Usuarios con Enums ===\n")

    # 1. Crear usuario estudiante
    student_data = {
        "nombre": "Ana",
        "apellido": "González",
        "documento": "87654321",
        "tipo_usuario": UserType.ESTUDIANTE.value,  # Usando enum
        "email": "ana@email.com",
        "curso": "4to Año",
        "talleres_inscritos": ["Carpintería", "Electrónica"]
    }

    success, message, user_id = create_user(student_data)
    print(f"Crear estudiante: {success}")
    print(f"Mensaje: {message}\n")

    # 2. Crear usuario personal
    staff_data = {
        "nombre": "Carlos",
        "apellido": "Rodríguez",
        "documento": "11223344",
        "tipo_usuario": UserType.PERSONAL.value,  # Usando enum
        "email": "carlos@escuela.edu",
        "rol": "Profesor de Taller",
        "departamento": "Tecnología"
    }

    success, message, staff_id = create_user(staff_data)
    print(f"Crear personal: {success}")
    print(f"Mensaje: {message}\n")

    # 3. Probar validación con enum incorrecto
    invalid_user = {
        "nombre": "Test",
        "apellido": "User",
        "documento": "99999999",
        "tipo_usuario": "TipoIncorrecto",  # Esto debería fallar
        "curso": "1er Año"
    }

    success, message, _ = create_user(invalid_user)
    print(f"Crear usuario con tipo inválido: {success}")
    print(f"Mensaje: {message}\n")

    # 4. Buscar usuarios por tipo usando enum
    print("=== Búsqueda usando enums ===")
    students = search_users(user_type=UserType.ESTUDIANTE.value)
    print(f"Estudiantes encontrados: {len(students)}")

    staff = search_users(user_type=UserType.PERSONAL.value)
    print(f"Personal encontrado: {len(staff)}")

    # 5. Mostrar valores válidos de enums
    print(f"\n=== Valores válidos ===")
    print(f"Tipos de usuario: {UserType.get_all_values()}")
    print(f"Estados de herramientas: {ToolState.get_all_values()}")
    print(f"Tipos de herramientas: {ToolType.get_all_values()}")


def test_validation_system():
    """Prueba el sistema de validación."""
    print("=== Prueba del Sistema de Validación ===\n")

    # Usuario con errores
    user_invalid = {
        "nombre": "",
        "apellido": "García",
        "documento": "123abc",
        "tipo_usuario": "TipoInválido",
        "email": "email_inválido"
    }

    is_valid, errors = validate_user_data(user_invalid)
    print(f"Usuario inválido: {is_valid}")
    if errors:
        print("Errores encontrados:")
        for error in errors:
            print(f"  - {error}")
    print()


if __name__ == "__main__":
    show_valid_values()
    test_tool_validation()
    tool_id_1, tool_id_2, tool_id_3 = test_tool_crud()
    test_tool_retrieval()
    test_tool_search()

    # Usar los IDs creados para las pruebas adicionales
    if tool_id_1:
        test_tool_state_management(tool_id_1)
        test_tool_update(tool_id_1)

    if tool_id_3:  # Usar el tercer ID para la prueba de eliminación
        test_tool_deletion(tool_id_3)

    test_tools_by_state()
