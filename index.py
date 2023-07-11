from uib_inf100_graphics import *
import player
import level
import sound

def app_started(app):
    sound.init_music("sound/backgroundMusic.mp3", 0.15)
    app.jump_sound = sound.Sound("sound/jump.wav")
    app.switch = True
    app.debug_mode = False
    app.level_num = 1
    app.level = level.get(app.level_num)
    app.player = player.initialize_player(465, 600, 40, 55)
    app.timer_delay = 1
    app.player_sprites = {
        "standing": app.load_image("characterSprites/standing.png"),    
        "crouching": app.load_image("characterSprites/crouching.png")
    }

def key_pressed(app, event):
    if event.key == "n":
        app.level_num += 1
        app.level = level.get(app.level_num)
    if event.key == "d":
        app.debug_mode = not app.debug_mode
    elif event.key == "r":
        run_app(width=960, height=720, title="Jump King")
    elif not app.player["is_falling"]:
        if event.key == "Space" and not app.player["jump_initiated"]:
            player.initiate_jump(app.player)
        elif event.key == "Left":
            player.walk(app.player, "l")
        elif event.key == "Right":
            player.walk(app.player, "r")

def key_released(app, event):
    if app.player["is_falling"]:
        return
    if event.key == "Space" and app.player["jump_initiated"]:
        app.jump_sound.play()
        player.jump(app.player)
    elif event.key == "Left" and app.player["direction"] == "l": 
        app.player["direction"] = None
        app.player["x_vel"] = 0
    elif event.key == "Right" and app.player["direction"] == "r": 
        app.player["direction"] = None
        app.player["x_vel"] = 0

def timer_fired(app):
    app.switch = not app.switch
    if app.player["jump_initiated"] and app.player["charge"] <= 18 and app.switch:
        app.player["charge"] += 2
    app.level, app.level_num = level.switch_scene(app.player, app.level, app.level_num)
    player.update_pos(app.player)
    player.collisions(app.player, app.level)

def redraw_all(app, canvas):
    level.draw(canvas, app.level, app)
    player.draw(canvas, app.player, app.player_sprites)

run_app(width=960, height=720, title="Jump King")