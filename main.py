from pins_utils import pin
import scene_handler as sh
import pin_game_scene

#initialize the scene handler
scene_handler : sh.SceneHandler = sh.SceneHandler("pin_game")

#initialize all scenes

random_seed : bool = False
seed : int = 1248831 #seed for the maze
width : int = 11 #width of the maze in number of hallways
height : int = 11 #height of the maze in number of hallways

scaling_factor : int = 25 #scaling factor for the maze png
border : int = 10 #size of the border around the maze in pixels


pin_game : pin_game_scene.PinGameScene = pin_game_scene.PinGameScene(scene_handler, random_seed, seed, width, height, scaling_factor, border, False)
scene_handler.add_scene("pin_game", pin_game)

while scene_handler.run():
    continue