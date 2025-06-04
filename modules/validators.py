"""
Módulo de validación de datos actualizado con enums.
Contiene funciones para validar diferentes tipos de datos de entrada.
"""
import re
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime
from modules.enums import UserType, ToolState, ToolType, MaintenanceType, AssignmentStatus


def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> Tuple[bool, List[str]]:
    """
    Valida que todos los campos requeridos estén presentes y no vacíos.

    Args:
        data: Diccionario con los datos a validar
        required_fields: Lista de campos requeridos

    Returns:
        Tupla (es_válido, lista_de_errores)
    """
    errors = []

    for field in required_fields:
        if field not in data:
            errors.append(f"Campo requerido '{field}' no está presente")
        elif not data[field] or str(data[field]).strip() == "":
            errors.append(f"Campo requerido '{field}' está vacío")

    return len(errors) == 0, errors


def validate_email(email: str) -> bool:
    """
    Valida formato de email usando expresión regular.

    Args:
        email: String con el email a validar

    Returns:
        True si el formato es válido, False en caso contrario
    """
    if not email:
        return True  # Email es opcional

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_document_number(document: str) -> Tuple[bool, str]:
    """
    Valida número de documento (DNI/Identificación).

    Args:
        document: String con el número de documento

    Returns:
        Tupla (es_válido, mensaje_error)
    """
    if not document:
        return False, "Número de documento es requerido"

    # Remover espacios y convertir a string
    document = str(document).strip()

    # Verificar que solo contenga números
    if not document.isdigit():
        return False, "El documento debe contener solo números"

    # Verificar longitud (ejemplo para DNI argentino: 7-8 dígitos)
    if len(document) < 7 or len(document) > 8:
        return False, "El documento debe tener entre 7 y 8 dígitos"

    return True, ""


def validate_user_type(user_type: str) -> Tuple[bool, str]:
    """
    Valida tipo de usuario usando enum.

    Args:
        user_type: Tipo de usuario a validar

    Returns:
        Tupla (es_válido, mensaje_error)
    """
    if not UserType.is_valid(user_type):
        valid_types = ", ".join(UserType.get_all_values())
        return False, f"Tipo de usuario debe ser uno de: {valid_types}"

    return True, ""


def validate_tool_state(state: str) -> Tuple[bool, str]:
    """
    Valida estado de herramienta usando enum.

    Args:
        state: Estado a validar

    Returns:
        Tuple (es_válido, mensaje_error)
    """
    if not ToolState.is_valid(state):
        valid_states = ", ".join(ToolState.get_all_values())
        return False, f"Estado debe ser uno de: {valid_states}"

    return True, ""


def validate_tool_type(tool_type: str) -> Tuple[bool, str]:
    """
    Valida tipo de herramienta usando enum.

    Args:
        tool_type: Tipo de herramienta a validar

    Returns:
        Tupla (es_válido, mensaje_error)
    """
    if not ToolType.is_valid(tool_type):
        valid_types = ", ".join(ToolType.get_all_values())
        return False, f"Tipo debe ser uno de: {valid_types}"

    return True, ""


def validate_maintenance_type(maintenance_type: str) -> Tuple[bool, str]:
    """
    Valida tipo de mantenimiento usando enum.

    Args:
        maintenance_type: Tipo de mantenimiento a validar

    Returns:
        Tupla (es_válido, mensaje_error)
    """
    if not MaintenanceType.is_valid(maintenance_type):
        valid_types = ", ".join(MaintenanceType.get_all_values())
        return False, f"Tipo de mantenimiento debe ser: {valid_types}"

    return True, ""


def validate_assignment_status(status: str) -> Tuple[bool, str]:
    """
    Valida estado de asignación usando enum.

    Args:
        status: Estado a validar

    Returns:
        Tupla (es_válido, mensaje_error)
    """
    if not AssignmentStatus.is_valid(status):
        valid_statuses = ", ".join(AssignmentStatus.get_all_values())
        return False, f"Estado debe ser uno de: {valid_statuses}"

    return True, ""


def validate_date_format(date_str: str) -> Tuple[bool, str]:
    """
    Valida formato de fecha (YYYY-MM-DD).

    Args:
        date_str: String con fecha a validar

    Returns:
        Tupla (es_válido, mensaje_error)
    """
    if not date_str:
        return False, "Fecha es requerida"

    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True, ""
    except ValueError:
        return False, "Formato de fecha inválido. Use YYYY-MM-DD"


def validate_positive_number(value: Any, field_name: str) -> Tuple[bool, str]:
    """
    Valida que un valor sea un número positivo.

    Args:
        value: Valor a validar
        field_name: Nombre del campo para el mensaje de error

    Returns:
        Tupla (es_válido, mensaje_error)
    """
    try:
        num_value = float(value)
        if num_value < 0:
            return False, f"{field_name} debe ser un número positivo"
        return True, ""
    except (ValueError, TypeError):
        return False, f"{field_name} debe ser un número válido"


def validate_user_data(user_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Valida datos completos de un usuario.

    Args:
        user_data: Diccionario con datos del usuario

    Returns:
        Tupla (es_válido, lista_de_errores)
    """
    errors = []

    # Campos básicos requeridos
    basic_required = ["nombre", "apellido", "documento", "tipo_usuario"]
    is_valid, field_errors = validate_required_fields(
        user_data, basic_required)
    errors.extend(field_errors)

    # Validar documento
    if "documento" in user_data:
        is_valid_doc, doc_error = validate_document_number(
            user_data["documento"])
        if not is_valid_doc:
            errors.append(doc_error)

    # Validar tipo de usuario usando enum
    if "tipo_usuario" in user_data:
        is_valid_type, type_error = validate_user_type(
            user_data["tipo_usuario"])
        if not is_valid_type:
            errors.append(type_error)

    # Validar email si está presente
    if "email" in user_data and user_data["email"]:
        if not validate_email(user_data["email"]):
            errors.append("Formato de email inválido")

    # Validaciones específicas por tipo de usuario
    if "tipo_usuario" in user_data:
        if user_data["tipo_usuario"] == UserType.ESTUDIANTE.value:
            student_required = ["curso"]
            _, student_errors = validate_required_fields(
                user_data, student_required)
            errors.extend(student_errors)

        elif user_data["tipo_usuario"] == UserType.PERSONAL.value:
            staff_required = ["rol"]
            _, staff_errors = validate_required_fields(
                user_data, staff_required)
            errors.extend(staff_errors)

    return len(errors) == 0, errors


def validate_tool_data(tool_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Valida datos completos de una herramienta.

    Args:
        tool_data: Diccionario con datos de la herramienta

    Returns:
        Tupla (es_válido, lista_de_errores)
    """
    errors = []

    # Campos básicos requeridos
    required_fields = ["nombre", "tipo", "marca",
                       "estado", "ubicacion", "fecha_adquisicion"]
    is_valid, field_errors = validate_required_fields(
        tool_data, required_fields)
    errors.extend(field_errors)

    # Validar tipo de herramienta
    if "tipo" in tool_data:
        is_valid_type, type_error = validate_tool_type(tool_data["tipo"])
        if not is_valid_type:
            errors.append(type_error)

    # Validar estado
    if "estado" in tool_data:
        is_valid_state, state_error = validate_tool_state(tool_data["estado"])
        if not is_valid_state:
            errors.append(state_error)

    # Validar fecha de adquisición
    if "fecha_adquisicion" in tool_data:
        is_valid_date, date_error = validate_date_format(
            tool_data["fecha_adquisicion"])
        if not is_valid_date:
            errors.append(f"Fecha de adquisición: {date_error}")

    return len(errors) == 0, errors
