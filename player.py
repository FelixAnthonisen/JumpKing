def initialize_player(x, y, width, height):
    return {
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "x_vel": 0, 
        "y_vel": 0,
        "is_falling": False,
        "direction": None,
        "jump_initiated": False,
        "charge": 0,
    }

def draw(canvas, player, sprites):
    x, y = player["x"], player["y"]
    if player["jump_initiated"]:
        canvas.create_image(x, y, pil_image=sprites["crouching"], anchor="nw")
        return
    canvas.create_image(x, y, pil_image=sprites["standing"], anchor="nw")

def update_pos(player):
    if player["is_falling"] and player["y_vel"] <= 14:
        player["y_vel"] += 0.63
    player["x"] += player["x_vel"]
    player["y"] += player["y_vel"]

def snap(direction, new, player):
    if direction == "up":   
        player["is_falling"] = False
        player["y_vel"] = 0
        player["x_vel"] = 0
        player["y"] = new
        player["direction"] = None
    elif direction == "down":
        player["y_vel"] *= -1
        player["y"] = new
    elif direction == "left":    
        player["x_vel"] *= -1/2
        player["x"] = new
    elif direction == "right":    
        player["x_vel"] *= -1/2
        player["x"] = new

def collisions(player, level):
    x, y, width, height = player["x"], player["y"], player["width"], player["height"]
    left, right, bottom, top = int(x//48), int((x+width)//48), int((y+height)//36), int(y//36)
    if player["is_falling"]:
        if right == 20:
            player["x_vel"] *= -1/2
            player["x"] = right*48-width-3
            return
        elif left == -1:
            player["x_vel"] *= -1/2
            player["x"] = (left+1)*48+3
            return
        if bottom > 19 or top < 0: 
            return
        horisontal, vertical = None, None
        #right
        if level[bottom-1][right] == 1 or level[bottom][right] == 1: 
            horisontal = {
                "direction": "left",
                "new": right*48-width-3
            }
        #left
        elif level[bottom-1][left] == 1 or level[bottom][left] == 1: 
            horisontal = {
                "direction": "right",
                "new": (left+1)*48+3
            }
        #bottom
        if level[bottom][right] == 1 or level[bottom][left] == 1:
            while bottom >= 0 and (level[bottom][right] == 1 or level[bottom][left] == 1):
                bottom -= 1
            vertical = {
                "direction": "up", 
                "new": (bottom+1)*36-height+2
            }
        #top
        elif level[top][right] == 1 or level[top][left] == 1:
            vertical = {
                "direction": "down",
                "new": (top+1)*36
            }
        if horisontal == None and vertical == None: 
            return
        if horisontal != None and vertical != None:
            vertical_diff = abs(player["y"]-vertical["new"])
            horisontal_diff = abs(player["x"]-horisontal["new"])
            min = vertical if vertical_diff < horisontal_diff else horisontal
            snap(min["direction"], min["new"], player)
            return
        if horisontal != None:
            snap(horisontal["direction"], horisontal["new"], player)
            return
        snap(vertical["direction"], vertical["new"], player)

    else:
        #right
        if right == 20 or level[bottom-1][right] == 1: 
            player["x_vel"] = 0
            player["x"] = right*48-width-1
        #left
        elif left == -1 or level[bottom-1][left] == 1: 
            player["x_vel"] = 0
            player["x"] = (left+1)*48+1
        #check if player isn't standing on the floor
        elif level[bottom][right] == 0 and level[bottom][left] == 0:
            player["is_falling"] = True
        

def walk(player, direction):
    player["direction"] = direction
    if player["jump_initiated"]:
        return
    if direction == "l":
        player["x_vel"] = -5
    else: 
        player["x_vel"] = 5

def initiate_jump(player):
    player["height"] /= 2
    player["x_vel"] = 0
    player["jump_initiated"] = True
    player["y"] += player["height"]
    player["charge"] = 4

def jump(player):
    horisontal_vel = 8
    if player["direction"] == "r":
        player["x_vel"] = horisontal_vel
    elif player["direction"] == "l":
        player["x_vel"] = -horisontal_vel
    player["y"] -= player["height"]
    player["height"] *= 2
    player["y_vel"] = -player["charge"]
    player["is_falling"] = True
    player["charge"] = 0
    player["jump_initiated"] = False
    player["direction"] = None