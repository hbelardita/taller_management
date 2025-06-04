"""
Módulo con enumeraciones para valores constantes del sistema.
"""
from enum import Enum

class UserType(Enum):
    """Tipos de usuario del sistema."""
    ESTUDIANTE = "Estudiante"
    PERSONAL = "Personal"
    ADMINISTRADOR = "Administrador"
    
    @classmethod
    def get_all_values(cls) -> list[str]:
        """Retorna todos los valores válidos."""
        return [member.value for member in cls]
    
    @classmethod
    def is_valid(cls, value: str) -> bool:
        """Verifica si un valor es válido."""
        return value in cls.get_all_values()

class ToolState(Enum):
    """Estados de herramientas y máquinas."""
    DISPONIBLE = "Disponible"
    EN_USO = "En Uso"
    EN_MANTENIMIENTO = "En Mantenimiento"
    FUERA_DE_SERVICIO = "Fuera de Servicio"
    
    @classmethod
    def get_all_values(cls) -> list[str]:
        """Retorna todos los valores válidos."""
        return [member.value for member in cls]
    
    @classmethod
    def is_valid(cls, value: str) -> bool:
        """Verifica si un valor es válido."""
        return value in cls.get_all_values()

class ToolType(Enum):
    """Tipos de herramientas y máquinas."""
    HERRAMIENTA_MANUAL = "Herramienta Manual"
    MAQUINA_ELECTRICA = "Máquina Eléctrica"
    EQUIPO_MEDICION = "Equipo de Medición"
    CONSUMIBLE = "Consumible"
    EQUIPO_SEGURIDAD = "Equipo de Seguridad"
    
    @classmethod
    def get_all_values(cls) -> list[str]:
        """Retorna todos los valores válidos."""
        return [member.value for member in cls]
    
    @classmethod
    def is_valid(cls, value: str) -> bool:
        """Verifica si un valor es válido."""
        return value in cls.get_all_values()

class MaintenanceType(Enum):
    """Tipos de mantenimiento."""
    PREVENTIVO = "Preventivo"
    CORRECTIVO = "Correctivo"
    
    @classmethod
    def get_all_values(cls) -> list[str]:
        """Retorna todos los valores válidos."""
        return [member.value for member in cls]
    
    @classmethod
    def is_valid(cls, value: str) -> bool:
        """Verifica si un valor es válido."""
        return value in cls.get_all_values()

class AssignmentStatus(Enum):
    """Estados de asignación/devolución."""
    PENDIENTE = "Pendiente"
    DEVUELTO_OK = "Devuelto OK"
    DEVUELTO_CON_OBSERVACIONES = "Devuelto con Observaciones"
    PERDIDO = "Perdido"
    DAÑADO = "Dañado"
    
    @classmethod
    def get_all_values(cls) -> list[str]:
        """Retorna todos los valores válidos."""
        return [member.value for member in cls]
    
    @classmethod
    def is_valid(cls, value: str) -> bool:
        """Verifica si un valor es válido."""
        return value in cls.get_all_values()