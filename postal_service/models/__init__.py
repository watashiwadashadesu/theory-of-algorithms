from .base import PostalItem
from .letter import Letter
from .parcel import Parcel
from .banderol import Banderol

# Указываем, что будет доступно при импорте из пакета models
__all__ = ['PostalItem', 'Letter', 'Parcel', 'Banderol']