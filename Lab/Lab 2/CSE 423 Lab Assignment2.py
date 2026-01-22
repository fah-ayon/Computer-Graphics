from OpenGL.GL import *
from OpenGL.GLUT import *
import random
import time

current_x, current_y = 0, 240

top_catcher_x1, top_catcher_y1, top_catcher_x2, top_catcher_y2 = -185, -220, -80, -220
bottom_catcher_x1, bottom_catcher_y1, bottom_catcher_x2, bottom_catcher_y2 = -100, -240, -165, -240
left_catcher_x1, left_catcher_y1, left_catcher_x2, left_catcher_y2 = -165, -240, -185, -220
right_catcher_x1, right_catcher_y1, right_catcher_x2, right_catcher_y2 = -100, -240, -80, -220
catcher_color = (1, 1, 1)

score = 0
missed = False
restart = False
cheat = False
paused = False
curr_color = (1, 1, 0)

cat_spd = 15
speed_inc = 0.2
base_spd = 2.0
diamond_spd = 2.0

last_time = time.time()
del_time = 0



def find_zone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0:
            return 0
        elif dx < 0 and dy >= 0:
            return 3
        elif dx < 0 and dy < 0:
            return 4
        else:
            return 7
    else:
        if dx >= 0 and dy >= 0:
            return 1
        elif dx < 0 and dy >= 0:
            return 2
        elif dx < 0 and dy < 0:
            return 5
        else:
            return 6


def convert_to_zone0(x, y, origin_zone):
    if origin_zone == 0:
        return x, y
    elif origin_zone == 1:
        return y, x
    elif origin_zone == 2:
        return -y, x
    elif origin_zone == 3:
        return -x, y
    elif origin_zone == 4:
        return -x, -y
    elif origin_zone == 5:
        return -y, -x
    elif origin_zone == 6:
        return y, -x
    elif origin_zone == 7:
        return x, -y


def convert_to_origin_zone(x, y, origin_zone):
    if origin_zone == 0:
        return x, y
    elif origin_zone == 1:
        return y, x
    elif origin_zone == 2:
        return -y, x
    elif origin_zone == 3:
        return -x, y
    elif origin_zone == 4:
        return -x, -y
    elif origin_zone == 5:
        return -y, -x
    elif origin_zone == 6:
        return y, -x
    elif origin_zone == 7:
        return x, -y


def MPL(x1, y1, x2, y2, origin_zone):
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)
    x, y = x1, y1

    while x <= x2:
        x_orig, y_orig = convert_to_origin_zone(x, y, origin_zone)
        glVertex2f(x_orig, y_orig)

        if d > 0:
            d += incNE
            y += 1
        else:
            d += incE
        x += 1


def draw_line(x1, y1, x2, y2, color=(1, 1, 1)):
    zone = find_zone(x1, y1, x2, y2)
    x1, y1 = convert_to_zone0(x1, y1, zone)
    x2, y2 = convert_to_zone0(x2, y2, zone)
    glBegin(GL_POINTS)
    glColor3f(*color)
    MPL(x1, y1, x2, y2, zone)
    glEnd()


def pause_play_button():
    if not paused:
        draw_line(-5, 200, -5, 230, (1, 0.7, 0))
        draw_line(15, 200, 15, 230, (1, 0.7, 0))
    else:
        draw_line(-10, 200, -10, 245, (1, 0.7, 0))
        draw_line(-10, 245, 20, 220, (1, 0.7, 0))
        draw_line(-10, 200, 20, 220, (1, 0.7, 0))


def restart_button():
    draw_line(-220, 220, -200, 200, (0.0, 0.8, 0.8))
    draw_line(-220, 220, -200, 245, (0.0, 0.8, 0.8))
    draw_line(-220, 220, -175, 220, (0.0, 0.8, 0.8))


def cross_button():
    draw_line(165, 232, 220, 200, (1.0, 0.0, 0.0))
    draw_line(165, 200, 222, 232, (1.0, 0.0, 0.0))


def box(x1, y1, x2, y2, x3, y3, x4, y4):
    draw_line(x1, y1, x2, y2, (0, 0, 0))
    draw_line(x2, y2, x3, y3, (0, 0, 0))
    draw_line(x3, y3, x4, y4, (0, 0, 0))
    draw_line(x1, y1, x4, y4, (0, 0, 0))


def catcher():
    global catcher_color
    draw_line(top_catcher_x1, top_catcher_y1, top_catcher_x2, top_catcher_y2, catcher_color)
    draw_line(bottom_catcher_x1, bottom_catcher_y1, bottom_catcher_x2, bottom_catcher_y2, catcher_color)
    draw_line(left_catcher_x1, left_catcher_y1, left_catcher_x2, left_catcher_y2, catcher_color)
    draw_line(right_catcher_x1, right_catcher_y1, right_catcher_x2, right_catcher_y2, catcher_color)


def diamond(x, y, diamond_color):
    if x - 10 < -250 or x + 10 > 250:
        pass
    else:
        draw_line(x, y - 10, x - 10, y, diamond_color)
        draw_line(x - 10, y, x, y + 10, diamond_color)
        draw_line(x, y + 10, x + 10, y, diamond_color)
        draw_line(x + 10, y, x, y - 10, diamond_color)


def check_collision():
    global current_x, current_y, cheat

    diamond_bottom = current_y - 10
    upper_limit = top_catcher_y1 + 5
    lower_limit = top_catcher_y1 - 30

    if lower_limit <= diamond_bottom <= upper_limit:

        catcher_cen = (top_catcher_x1 + top_catcher_x2) / 2
        catcher_half = (top_catcher_x2 - top_catcher_x1) / 2

        margin = 20 if cheat else 10

        if catcher_half + margin >= abs(current_x - catcher_cen):
            return True

    return False


def check_miss():
    if bottom_catcher_y1 > current_y + 10:
        return True
    return False


def move_catcher(dx):
    global top_catcher_x1, top_catcher_x2
    global bottom_catcher_x1, bottom_catcher_x2
    global left_catcher_x1, left_catcher_x2
    global right_catcher_x1, right_catcher_x2

    top_catcher_x1 += dx
    top_catcher_x2 += dx
    bottom_catcher_x1 += dx
    bottom_catcher_x2 += dx
    left_catcher_x1 += dx
    left_catcher_x2 += dx
    right_catcher_x1 += dx
    right_catcher_x2 += dx


def specialKeyListener(key, x, y):
    global paused, missed, cheat

    if paused or missed or cheat:
        return

    if key == GLUT_KEY_LEFT:
        if top_catcher_x1 - cat_spd > -250:
            move_catcher(-cat_spd)

    elif key == GLUT_KEY_RIGHT:
        if top_catcher_x2 + cat_spd < 250:
            move_catcher(cat_spd)


def keyboardListener(key, x, y):
    global cheat
    if key == b'c' or key == b'C':
        cheat = not cheat
        print("Cheat Mode Activated" if cheat else "Cheat Mode Deactivated")


def move_catcher_to_diamond_cheatMode():
    global current_x, del_time

    catcher_center = (bottom_catcher_x1 + bottom_catcher_x2) / 2
    distance = current_x - catcher_center

    if abs(distance) > 1:
        move_speed = 300 * del_time
        move_amount = min(move_speed, abs(distance))
        
        if distance > 0:
            if right_catcher_x2 + move_amount <= 250:
                move_catcher(move_amount)
            else:
                max_move = 250 - right_catcher_x2
                if max_move > 0:
                    move_catcher(max_move)

        else:
            if top_catcher_x1 - move_amount >= -250:
                move_catcher(-move_amount)
            else:
                max_move = top_catcher_x1 + 250
                if max_move > 0:
                    move_catcher(-max_move)


def reset_game():
    global current_x, current_y, score, diamond_spd, base_spd
    global catcher_color, missed, paused, curr_color, cheat

    score = 0
    diamond_spd = base_spd
    catcher_color = (1, 1, 1)
    missed = False
    paused = False
    cheat = False
    curr_color = (random.uniform(0.5, 1), random.uniform(0.5, 1), random.uniform(0.5, 1))

    current_x = random.randint(-240, 240)
    current_y = 250

    global top_catcher_x1, top_catcher_y1, top_catcher_x2, top_catcher_y2
    global bottom_catcher_x1, bottom_catcher_y1, bottom_catcher_x2, bottom_catcher_y2
    global left_catcher_x1, left_catcher_y1, left_catcher_x2, left_catcher_y2
    global right_catcher_x1, right_catcher_y1, right_catcher_x2, right_catcher_y2

    top_catcher_x1, top_catcher_y1, top_catcher_x2, top_catcher_y2 = -185, -220, -80, -220
    bottom_catcher_x1, bottom_catcher_y1, bottom_catcher_x2, bottom_catcher_y2 = -100, -240, -165, -240
    left_catcher_x1, left_catcher_y1, left_catcher_x2, left_catcher_y2 = -165, -240, -185, -220
    right_catcher_x1, right_catcher_y1, right_catcher_x2, right_catcher_y2 = -100, -240, -80, -220


def mouseListener(button, state, x, y):
    global paused, score, catcher_color, missed, base_spd

    x = x - 250
    y = 250 - y

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:

        if -10 <= x <= 20 and 200 <= y <= 245:
            if not missed:
                paused = not paused
                if paused:
                    print("Game Paused")
                else:
                    print("Game Resumed")

        elif 165 <= x <= 245 and 200 <= y <= 245:
            print("Score:", score)
            print("Goodbye")
            glutLeaveMainLoop()

        elif -230 <= x <= -175 and 200 <= y <= 245:
            reset_game()
            print("Starting Over")


def display():
    global current_x, current_y, curr_color, diamond_spd
    global score, catcher_color, missed, paused
    global last_time, del_time, cheat, base_spd

    current_time = time.time()
    delta_time = current_time - last_time
    last_time = current_time
    del_time = delta_time

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPointSize(2.0)

    catcher()
    box(-230, 200, -175, 200, -175, 245, -230, 245)
    box(-10, 200, 20, 200, 20, 245, -10, 245)
    box(230, 200, 175, 200, 175, 245, 230, 245)
    pause_play_button()
    restart_button()
    cross_button()
    
    if not missed:
        diamond(current_x, current_y, curr_color)
    

    if not paused and not missed:
        if cheat:
            move_catcher_to_diamond_cheatMode()

        collision_detected = check_collision()

        if collision_detected:
            score += 1
            diamond_spd = base_spd + (score * speed_inc)
            
            cheat_speed_limit = 9
            if cheat and diamond_spd > cheat_speed_limit:
                diamond_spd = cheat_speed_limit
                
            print("Score:", score)
            current_x = random.randint(-240, 240)
            current_y = 250
            curr_color = (random.uniform(0.5, 1), random.uniform(0.5, 1), random.uniform(0.5, 1))

        else:
            current_y -= diamond_spd * 60 * delta_time

            if check_miss() and not missed:
                catcher_color = (1.0, 0.0, 0.0)
                missed = True
                print("Game Over! Score:", score)

    glutSwapBuffers()
    glutPostRedisplay()




glutInit()
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(500, 500)
glutCreateWindow(b"CSE423 Lab Assignment 2")
glutDisplayFunc(display)
glutSpecialFunc(specialKeyListener)
glutKeyboardFunc(keyboardListener)
glutMouseFunc(mouseListener)
glClearColor(0.0, 0.0, 0.0, 1.0)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(-250, 250, -250, 250, -1, 1)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
glutMainLoop()
