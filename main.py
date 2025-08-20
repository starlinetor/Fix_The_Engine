from pins_utils import pin
import scene_handler as sh
import pin_game_scene

#initialize the scene handler
scene_handler : sh.SceneHandler = sh.SceneHandler("pin_game")

#initialize all scenes
pin_game : pin_game_scene.PinGameScene = pin_game_scene.PinGameScene(scene_handler, True, 1920638152, 8, 8, 25, 10, False)
scene_handler.add_scene("pin_game", pin_game)

while scene_handler.run():
    continue