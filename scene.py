import pygame

class Scene:
    def __init__(self, scene_handler : 'SceneHandler') -> None:
        self.scene_handler : 'SceneHandler' = scene_handler
    
    def start(self) -> None: 
        pass
    
    def update(self) -> None: 
        pass
    
    def on_exit(self) -> None:
        pygame.quit()