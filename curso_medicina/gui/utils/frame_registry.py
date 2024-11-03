from curso_medicina.gui.frames.base_frame import BaseFrame

from typing import Dict, Type, Callable


class FrameRegistry:
    """
    Registro centralizado de frames disponibles en la aplicación.
    Permite un manejo más flexible de la navegación y la creación de frames.
    """
    _frames: Dict[str, Type[BaseFrame]] = {}
    
    @classmethod
    def register(cls, name: str, frame_class: Type[BaseFrame]):
        cls._frames[name] = frame_class
    
    @classmethod
    def get_frame(cls, name: str) -> Type[BaseFrame]:
        return cls._frames.get(name)
    
    @classmethod
    def create_frame(cls, name: str, parent, conn) -> BaseFrame:
        frame_class = cls.get_frame(name)
        if frame_class:
            return frame_class(parent, conn)
        raise ValueError(f"Frame {name} no encontrado")