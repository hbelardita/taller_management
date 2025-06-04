"""
Módulo para la gestión de herramientas y máquinas
Maneja las operaciones CRUD y lógica de negocio relacionada con herramientas
"""

from typing import Any, Dict, List, Optional, Tuple, Union
from datetime import datetime
import json
import os

from modules.data_manager import load_json_data, save_json_data
from modules.id_generator import get_next_id
from modules.validators import validate_required_fields, validate_tool_data, validate_tool_state

# Constantes para estados válidos
VALID_STATES = ["Disponible", "En Uso",
                "En Mantenimiento", "Fuera de Servicio"]
VALID_TYPES = ["Herramienta Manual", "Máquina Eléctrica",
               "Equipo de Medición", "Consumible"]


def get_all_tools() -> List[Dict[str, Any]]:
    """
    Carga las herramientas

    Returns:
        Lista de diccionarios con información de herramientas
    """
    return load_json_data("herramientas")


def create_tool(data: Dict) -> Tuple[bool, str, Optional[int]]:
    """
    Crea una nueva herramienta

    Args:
        data: Diccionario con los datos de la herramienta

    Returns:
        Tupla (éxito, mensaje, id_usuario_creado)
    """
    # Validar datos
    is_valid, errors = validate_tool_data(data)
    if not is_valid:
        error_msg = "Errores de validación: " + "; ".join(errors)
        return False, error_msg, None

    # Cargar herramientas existentes
    tools = get_all_tools()
    tool_id = get_next_id(tools)
    # Crear nueva herramienta
    new_tool = {
        'id': tool_id,
        'name': data['name'].strip(),
        'type': data['type'],
        'brand': data.get('brand', '').strip(),
        'model': data.get('model', '').strip(),
        'serial_number': data.get('serial_number', '').strip(),
        'state': data['state'],
        'location': data['location'].strip(),
        'acquisition_date': data.get('acquisition_date', ''),
        'notes': data.get('notes', '').strip(),
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    # Agregar y guardar
    tools.append(new_tool)

    if save_json_data("herramientas", tools):
        return True, f"Herramienta creada exitosamente con ID {tool_id}", tool_id
    else:
        return False, "Error al guardar herramienta", None


def get_tool_by_id(tool_id: int) -> Optional[Dict[str, Any]]:
    """
    Obtiene una herramienta por su ID

    Args:
        tool_id: ID de la herramienta a buscar

    Returns:
        Diccionario con datos de la herramienta o None si no se encuentra
    """
    tools = get_all_tools()
    for tool in tools:
        if tool.get("id") == tool_id:
            return tool
    return None


def update_tool(tool_id: int, data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Actualiza los datos de una herramienta existente

    Args:
        tool_id: ID de la herramienta a actualizar
        data: Nuevos datos de la herramienta

    Returns:
         Tupla (éxito, mensaje)
    """
    tools = get_all_tools()
    # Buscar herramienta
    tool_index = None
    for i, tool in enumerate(tools):
        if tool.get("id") == tool_index:
            tool_index = i
            break

    if tool_index is None:
        return False, f'Herramienta con ID {tool_id} no encontrada'
    # Crear datos actualizados manteniendo el ID original
    current_tool = tools[tool_index].copy()
    current_tool.update(data)
    current_tool["id"] = tool_id  # Asegurar que el ID no cambie
    # Validar datos
    is_valid, errors = validate_tool_data(current_tool)
    if not is_valid:
        error_msg = "Errores de validación: " + "; ".join(errors)
        return False, error_msg

    # Actualizar usuario
    tools[tool_index] = current_tool

    # Guardar cambios
    if save_json_data("herramientas", tools):
        return True, f"Herramienta {tool_id} actualizada exitosamente"
    else:
        return False, "Error al guardar los cambios"


def delete_tool(tool_id: int) -> Tuple[bool, str]:
    """
    Elimina una herramienta

    Args:
        tool_id: ID de la herramienta a eliminar

    Returns:
         Tupla (éxito, mensaje)
    """
    tools = get_all_tools()

    # Buscar y eliminar herramienta
    original_count = len(tools)
    tools = [tool for tool in tools if tool.get("id") != tool_id]

    if len(tools) == original_count:
        return False, f"Herramienta con ID {tool_id} no encontrado"

    if save_json_data("herramientas", tools):
        return True, f"Herramienta {tool_id} eliminado exitosamente"
    else:
        return False, "Error al guardar los cambios"


def update_tool_state(tool_id: int, new_state: str) -> Tuple[bool, str]:
    """
    Actualiza solo el estado de una herramienta

    Args:
        tool_id: ID de la herramienta
        new_state: Nuevo estado de la herramienta

    Returns:
         Tuple (es_válido, mensaje_error)
    """
    is_valid, message = validate_tool_state(new_state)
    if not is_valid:
        return is_valid, message

    tools = get_all_tools()

    # Buscar herramienta
    for i, tool in enumerate(tools):
        if tool['id'] == tool_id:
            tools[i]['estado'] = new_state

            if save_json_data("herramientas", tools):
                return True, f'Estado actualizado a: {new_state}'
            return False, 'Error al guardar los cambios'
    return False, f"Herramienta con ID {tool_id} no encontrada"


def search_tools(filters: Dict) -> List[Dict[str, Any]]:
    """
    Busca herramientas según filtros especificados

    Args:
        filters: Diccionario con filtros de búsqueda

    Returns:
        Lista de herramientas que coinciden con los filtros
    """
    tools = get_all_tools()

    if not filters:
        return tools

    filtered_tools = []

    for tool in tools:
        match = True

        # Filtro por nombre (búsqueda parcial, insensible a mayúsculas)
        if filters.get('nombre'):
            if filters['nombre'].lower() not in tool['nombre'].lower():
                match = False

        # Filtro por tipo
        if filters.get('tipo'):
            if tool['tipo'] != filters['tipo']:
                match = False

        # Filtro por estado
        if filters.get('estado'):
            if tool['estado'] != filters['estado']:
                match = False

        # Filtro por ubicación (búsqueda parcial, insensible a mayúsculas)
        if filters.get('ubicacion'):
            if filters['ubicacion'].lower() not in tool['ubicacion'].lower():
                match = False

        # Filtro por marca (búsqueda parcial, insensible a mayúsculas)
        if filters.get('marca'):
            if filters['marca'].lower() not in tool.get('marca', '').lower():
                match = False

        if match:
            filtered_tools.append(tool)

    return filtered_tools


def get_tools_by_state(state: str) -> List[Dict]:
    """
    Obtiene todas las herramientas con un estado específico

    Args:
        state: Estado a filtrar

    Returns:
        Lista de herramientas con el estado especificado
    """
    return search_tools({'estado': state})


def get_available_tools() -> List[Dict]:
    """
    Obtiene todas las herramientas disponibles

    Returns:
        Lista de herramientas disponibles
    """
    return get_tools_by_state('Disponible')
