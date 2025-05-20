from abc import ABC, abstractmethod
import pygame


class GameObject(ABC):
    @abstractmethod
    def update(self, dt: float):
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface):
        pass
