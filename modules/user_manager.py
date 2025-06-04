"""
Módulo para gestión de usuarios.
Contiene funciones CRUD para el manejo de usuarios del sistema.
"""
from typing import Dict, Any, List, Optional, Tuple
from modules.data_manager import load_json_data, save_json_data
from modules.id_generator import get_next_id
from modules.validators import validate_user_data


def create_user(user_data: Dict[str, Any]) -> Tuple[bool, str, Optional[int]]:
    """
    Crea un nuevo usuario en el sistema.

    Args:
        user_data: Diccionario con los datos del usuario

    Returns:
        Tupla (éxito, mensaje, id_usuario_creado)
    """
    # Validar datos de entrada
    is_valid, errors = validate_user_data(user_data)
    if not is_valid:
        error_msg = "Errores de validación: " + "; ".join(errors)
        return False, error_msg, None

    users = get_all_users()

    # Verificar que el documento no esté duplicado
    document = str(user_data["documento"]).strip()
    if any(str(user.get("documento", "")).strip() == document for user in users):
        return False, f"Ya existe un usuario con documento {document}", None

    user_id = get_next_id(users, "id")

    # Crear registro de usuario
    new_user = {
        "id": user_id,
        "nombre": user_data["nombre"].strip(),
        "apellido": user_data["apellido"].strip(),
        "documento": document,
        "tipo_usuario": user_data["tipo_usuario"],
        "email": user_data.get("email", "").strip() if user_data.get("email") else ""
    }

    # Agregar campos específicos según tipo de usuario
    if user_data["tipo_usuario"] == "Estudiante":
        new_user.update({
            "curso": user_data.get("curso", "").strip(),
            "talleres_inscritos": user_data.get("talleres_inscritos", [])
        })
    elif user_data["tipo_usuario"] == "Personal":
        new_user.update({
            "rol": user_data.get("rol", "").strip(),
            "departamento": user_data.get("departamento", "").strip()
        })

    # Agregar usuario a la lista
    users.append(new_user)

    # Guardar datos
    if save_json_data("usuarios", users):
        return True, f"Usuario creado exitosamente con ID {user_id}", user_id
    else:
        return False, "Error al guardar el usuario", None


def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """
    Obtiene un usuario por su ID.

    Args:
        user_id: ID del usuario a buscar

    Returns:
        Diccionario con datos del usuario o None si no existe
    """
    users = get_all_users()
    return next((user for user in users if user.get("id") == user_id), None)


def get_user_by_document(document: str) -> Optional[Dict[str, Any]]:
    """
    Obtiene un usuario por su número de documento.

    Args:
        document: Número de documento a buscar

    Returns:
        Diccionario con datos del usuario o None si no existe
    """
    users = get_all_users()
    document = str(document).strip()
    return next((user for user in users if str(user.get("documento", "")).strip() == document), None)


def get_all_users() -> List[Dict[str, Any]]:
    """
    Obtiene todos los usuarios del sistema.

    Returns:
        Lista con todos los usuarios
    """
    return load_json_data("usuarios")


def search_users(search_term: str = "", user_type: str = "", course: str = "", role: str = "") -> List[Dict[str, Any]]:
    """
    Busca usuarios con filtros específicos.

    Args:
        search_term: Término de búsqueda (nombre, apellido o documento)
        user_type: Filtro por tipo de usuario
        course: Filtro por curso (solo estudiantes)
        role: Filtro por rol (solo personal)

    Returns:
        Lista de usuarios que coinciden con los criterios
    """
    users = get_all_users()
    filtered_users = []

    for user in users:
        # Filtro por término de búsqueda
        if search_term:
            search_lower = search_term.lower()
            name_match = search_lower in user.get("nombre", "").lower()
            lastname_match = search_lower in user.get("apellido", "").lower()
            document_match = search_term in str(user.get("documento", ""))

            if not (name_match or lastname_match or document_match):
                continue

        # Filtro por tipo de usuario
        if user_type and user.get("tipo_usuario") != user_type:
            continue

        # Filtro por curso (solo para estudiantes)
        if course and user.get("tipo_usuario") == "Estudiante":
            if user.get("curso", "").lower() != course.lower():
                continue

        # Filtro por rol (solo para personal)
        if role and user.get("tipo_usuario") == "Personal":
            if role.lower() not in user.get("rol", "").lower():
                continue

        filtered_users.append(user)

    return filtered_users


def update_user(user_id: int, updated_data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Actualiza los datos de un usuario existente.

    Args:
        user_id: ID del usuario a actualizar
        updated_data: Diccionario con los nuevos datos

    Returns:
        Tupla (éxito, mensaje)
    """
    # Cargar usuarios
    users = get_all_users()

    # Buscar usuario
    user_index = None
    for i, user in enumerate(users):
        if user.get("id") == user_id:
            user_index = i
            break

    if user_index is None:
        return False, f"Usuario con ID {user_id} no encontrado"

    # Crear datos actualizados manteniendo el ID original
    current_user = users[user_index].copy()
    current_user.update(updated_data)
    current_user["id"] = user_id  # Asegurar que el ID no cambie

    # Validar datos actualizados
    is_valid, errors = validate_user_data(current_user)
    if not is_valid:
        error_msg = "Errores de validación: " + "; ".join(errors)
        return False, error_msg

    # Verificar documento duplicado (excluyendo el usuario actual)
    document = str(current_user["documento"]).strip()
    for i, user in enumerate(users):
        if i != user_index and str(user.get("documento", "")).strip() == document:
            return False, f"Ya existe otro usuario con documento {document}"

    # Actualizar usuario
    users[user_index] = current_user

    # Guardar cambios
    if save_json_data("usuarios", users):
        return True, f"Usuario {user_id} actualizado exitosamente"
    else:
        return False, "Error al guardar los cambios"


def delete_user(user_id: int) -> Tuple[bool, str]:
    """
    Elimina un usuario del sistema.

    Args:
        user_id: ID del usuario a eliminar

    Returns:
        Tupla (éxito, mensaje)
    """
    # Cargar usuarios
    users = get_all_users()

    # Buscar y eliminar usuario
    original_count = len(users)
    users = [user for user in users if user.get("id") != user_id]

    if len(users) == original_count:
        return False, f"Usuario con ID {user_id} no encontrado"

    # Guardar cambios
    if save_json_data("usuarios", users):
        return True, f"Usuario {user_id} eliminado exitosamente"
    else:
        return False, "Error al guardar los cambios"


def format_user_info(user: Dict[str, Any]) -> str:
    """
    Formatea la información de un usuario para mostrar.

    Args:
        user: Diccionario con datos del usuario

    Returns:
        String formateado con la información del usuario
    """
    info = f"ID: {user.get('id', 'N/A')}\n"
    info += f"Nombre: {user.get('nombre', '')} {user.get('apellido', '')}\n"
    info += f"Documento: {user.get('documento', 'N/A')}\n"
    info += f"Tipo: {user.get('tipo_usuario', 'N/A')}\n"

    if user.get('email'):
        info += f"Email: {user.get('email')}\n"

    if user.get('tipo_usuario') == 'Estudiante':
        info += f"Curso: {user.get('curso', 'N/A')}\n"
        if user.get('talleres_inscritos'):
            info += f"Talleres: {', '.join(user.get('talleres_inscritos', []))}\n"

    elif user.get('tipo_usuario') == 'Personal':
        info += f"Rol: {user.get('rol', 'N/A')}\n"
        if user.get('departamento'):
            info += f"Departamento: {user.get('departamento')}\n"

    return info
