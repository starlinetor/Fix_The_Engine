import scene as sc

class SceneHandler:
    def __init__(self, default_scene : str) -> None:
        """Initialize the Scene Handler class

        Args:
            default_scene (str): name of the default scene
        """
        self.scenes : dict[str, sc.Scene] = {}
        self.active_scene_name : str = default_scene
        self.active_scene : sc.Scene = sc.Scene(self)
        self.init_scene : bool = False
        self.running = True
    
    def add_scene(self, name:str, scene : sc.Scene) -> None:
        """Add a scene to the scene handler

        Args:
            name (str): name of the scene
            scene (sc.Scene): scene to be added
        """
        self.scenes[name] = scene
    
    def run(self) -> bool:
        """
        Exectues the application\n
        Returns true if the scene_handler is working\n
        Use : \n
        while scene_handler.run():
            continue
        """
        #initialize a new scene
        if (not self.init_scene) and self.running:
            self.active_scene.on_exit()
            self.active_scene = self.scenes[self.active_scene_name]
            self.init_scene = True
            self.active_scene.start()
        #run the scene
        elif self.running:
            self.active_scene.update()
        #exit sequence
        if not self.running:
            self.active_scene.on_exit()
        #return running
        return self.running
    
    def change_scene(self, scene_name : str) -> None:
        """To be executed from another scene\n
        Will tell the scene handler to execute a new scene

        Args:
            scene_name (str): name of the new scene
        """
        self.active_scene_name = scene_name
        self.init_scene = False
    
    def quit(self) -> None:
        """Closes the full application and turns off the scene handler
        """
        self.running = False