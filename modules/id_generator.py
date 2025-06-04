"""
Módulo para generar IDs únicos autoincrementales.
"""
from typing import Dict, Any, List

def get_next_id(data: List[Dict[str, Any]], id_field: str = "id") -> int:
    """
    Genera el siguiente ID único basado en los datos existentes.
    
    Args:
        data: Lista de registros existentes
        id_field: Nombre del campo ID (por defecto "id")
        
    Returns:
        Siguiente ID disponible
    """
    return  max(record.get(id_field, 0) for record in data) + 1 if data else 1 