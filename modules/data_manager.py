"""
Módulo para el manejo de datos JSON.
Contiene funciones para leer, escribir y gestionar archivos JSON de forma segura.
"""
import json
import os
from typing import Dict, List, Any, Optional
from pathlib import Path

# Configuración de rutas
DATA_DIR = Path("data")
DATA_FILES = {
    "usuarios": DATA_DIR / "usuarios.json",
    "herramientas": DATA_DIR / "herramientas.json", 
    "mantenimientos": DATA_DIR / "mantenimientos.json",
    "asignaciones": DATA_DIR / "asignaciones.json"
}

def ensure_data_directory() -> None:
    """Asegura que el directorio de datos exista."""
    DATA_DIR.mkdir(exist_ok=True)

def load_json_data(filename: str) -> List[Dict[str, Any]]:
    """
    Carga datos desde un archivo JSON.
    
    Args:
        filename: Nombre del archivo (sin extensión)
        
    Returns:
        Lista de diccionarios con los datos, o lista vacía si no existe
    """
    file_path = DATA_FILES.get(filename)
    if not file_path or not file_path.exists():
        return []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError) as e:
        return []

def save_json_data(filename: str, data: List[Dict[str, Any]]) -> bool:
    """
    Guarda datos en un archivo JSON.
    
    Args:
        filename: Nombre del archivo (sin extensión)
        data: Lista de diccionarios a guardar
        
    Returns:
        True si se guardó correctamente, False en caso contrario
    """
    ensure_data_directory()
    file_path = DATA_FILES.get(filename)
    
    if not file_path:
        return False
    
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        return True
    except IOError as e:
        return False