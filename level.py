from json import loads

def get(level_num):
    f = open("json/levels.json", "rt")
    str = f.read()
    f.close()
    arr = loads(str)
    return arr[f"{level_num}"]

def draw_outlines(canvas, start_x, end_x, start_y, end_y):
    canvas.create_line(start_x, start_y, end_x, start_y, fill="red")
    canvas.create_line(start_x, start_y, start_x, end_y, fill="red")
    canvas.create_line(end_x, start_y, end_x, end_y, fill="red")
    canvas.create_line(start_x, end_y, end_x, end_y, fill="red")

def draw(canvas, board, app):
    background_colors = ["#87CEEB", "#7AB9D4", "#6CA5BC", "#5F90A5", "#517C8D", "#446776", "#36535E", "#293E46", "#1B252F"]
    index = app.level_num - 1
    canvas.create_rectangle(0, 0, app.width, app.height, width=0, fill=background_colors[index])
    step_x = ((app.width))/len(board[0])
    step_y = ((app.height))/len(board)
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 1: 
                start_x, end_x = (step_x*j, step_x*(j+1))
                start_y, end_y = (step_y*i, step_y*(i+1))
                canvas.create_rectangle(start_x, start_y, end_x, end_y, width=1, outline="#000", fill="#7BB369")
                if app.debug_mode: 
                    draw_outlines(canvas, start_x, end_x, start_y, end_y)

def switch_scene(player, level, level_num):
    y, height = player["y"], player["height"]
    top, bottom = int((y+height)//36), int(y//36)
    if bottom+1 < 0:
        level_num += 1
        level = get(level_num)
        player["y"] = 720-height
    elif top-1 >= 20:
        level_num -= 1
        level = get(level_num)
        player["y"] = 0
    return level, level_num