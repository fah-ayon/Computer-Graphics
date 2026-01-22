#----------------------------------------------------------------------------------
#Task 1
#####################################################################################



from OpenGL.GL import *    
from OpenGL.GLUT import *  
from OpenGL.GLU import *   
import random

x, y = 250, 250
sky_color = [0, 0, 0]
rain_speed = 4
rain_angle = 0.0
rain_coordinates = [(random.uniform(0, 500), random.uniform(0, 500)) for i in range(500)]


# for field
def drawBackGround(x, y):
    glLineWidth(5)
    glColor3f(0.8, 0.4, 0.0)
    glBegin(GL_TRIANGLES)

    glVertex2f(0, 0)
    glVertex2f(500, 0)
    glVertex2f(500, 350)

    glVertex2f(0, 0)
    glVertex2f(500, 350)
    glVertex2f(0, 350)
    glEnd()


# for sky
def drawSky(x, y):
    glLineWidth(5)
    global sky_color
    glColor3f(*sky_color)
    glBegin(GL_TRIANGLES)

    glVertex2f(0, 350)
    glVertex2f(500, 350)
    glVertex2f(500, 500)

    glVertex2f(0, 500)
    glVertex2f(0, 350)
    glVertex2f(500, 500)
    glEnd()


def drawHills(x, y):
    glLineWidth(5)

    triangle_width = 500 / 15

    for i in range(15):
        star_point = i * triangle_width
        end_point = (i + 1) * triangle_width
        mid_point = (star_point + end_point) / 2

        glBegin(GL_TRIANGLES)
        glColor3f(0.11, 0.59, 0.02)
        glVertex2f(star_point, 280)
        glColor3f(0.2784, 0.8510, 0.1686)
        glVertex2f(end_point, 280)
        glColor3f(0.8, 0.4, 0.0)
        glVertex2f(mid_point, 350)
        glEnd()


def drawHouse(x, y):
    glLineWidth(5)
    # for roof
    glBegin(GL_TRIANGLES)
    glColor3f(0.5098, 0.1686, 0.8510)
    glVertex2f(100, 270)
    glVertex2f(250, 370)
    glVertex2f(400, 270)
    glEnd()

    # for house structure
    glBegin(GL_TRIANGLES)
    glColor3f(1, 1, 1)
    glVertex2f(120, 270)
    glVertex2f(380, 270)
    glVertex2f(380, 120)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(1, 1, 1)
    glVertex2f(380, 120)
    glVertex2f(120, 120)
    glVertex2f(120, 270)
    glEnd()

    # for door
    glBegin(GL_TRIANGLES)
    glColor3f(0.1686, 0.6353, 0.8510)
    glVertex2f(220, 250)
    glVertex2f(220, 120)
    glVertex2f(280, 120)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(0.1686, 0.6353, 0.8510)
    glVertex2f(220, 250)
    glVertex2f(280, 250)
    glVertex2f(280, 120)
    glEnd()

    glPointSize(10)
    glBegin(GL_POINTS)
    glColor3f(0, 0, 0)
    glVertex2f(265, 185)
    glEnd()

    # for window  
    glBegin(GL_TRIANGLES)
    glColor3f(0.1686, 0.6353, 0.8510)
    glVertex2f(145, 250)
    glVertex2f(145, 185)
    glVertex2f(200, 185)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(0.1686, 0.6353, 0.8510)
    glVertex2f(145, 250)
    glVertex2f(200, 250)
    glVertex2f(200, 185)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(0.1686, 0.6353, 0.8510)
    glVertex2f(300, 250)
    glVertex2f(300, 185)
    glVertex2f(360, 185)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(0.1686, 0.6353, 0.8510)
    glVertex2f(300, 250)
    glVertex2f(360, 250)
    glVertex2f(360, 185)
    glEnd()

    glLineWidth(2)
    glColor3f(0, 0, 0)
    glBegin(GL_LINES)
    glVertex2f(145, 217.5)
    glVertex2f(200, 217.5)
    glEnd()

    glLineWidth(2)
    glColor3f(0, 0, 0)
    glBegin(GL_LINES)
    glVertex2f(172.5, 250)
    glVertex2f(172.5, 185)
    glEnd()

    glLineWidth(2)
    glColor3f(0, 0, 0)
    glBegin(GL_LINES)
    glVertex2f(330, 250)
    glVertex2f(330, 185)
    glEnd()

    glLineWidth(2)
    glColor3f(0, 0, 0)
    glBegin(GL_LINES)
    glVertex2f(300, 217.5)
    glVertex2f(360, 217.5)
    glEnd()


def drawRain():
    glColor3f(0.678, 0.827, 0.941)
    glLineWidth(1)
    for x, y in rain_coordinates:
        glBegin(GL_LINES)
        glVertex2f(x, y)           
        glVertex2f(x + rain_angle, y - 10) 
        glEnd()


def rainFall():
    global rain_coordinates
    for i in range(len(rain_coordinates)):
        x, y = rain_coordinates[i]
        y -= rain_speed
        x += rain_angle * 0.1  
        
       
        if x < 0:
            x += 500
        elif x > 500:
            x -= 500
        
        
        if y < 0:
            x = random.uniform(0, 500)
            y = 500
            
        rain_coordinates[i] = (x, y)
    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global sky_color, rain_angle
    if key == GLUT_KEY_UP:
        sky_color[0] = min(sky_color[0] + 0.1, 0.5294)
        sky_color[1] = min(sky_color[1] + 0.1, 0.8078)
        sky_color[2] = min(sky_color[2] + 0.1, 0.9216)

    elif key == GLUT_KEY_DOWN:
        sky_color[0] = max(sky_color[0] - 0.1, 0.0)
        sky_color[1] = max(sky_color[1] - 0.1, 0.0)
        sky_color[2] = max(sky_color[2] - 0.1, 0.0)
    
    if key == GLUT_KEY_RIGHT:
        rain_angle += 1  
    elif key == GLUT_KEY_LEFT:
        rain_angle -= 1 

    glutPostRedisplay()

def setup_projection():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setup_projection()
    drawBackGround(x, y)
    drawSky(x, y)
    drawHills(x, y)
    drawHouse(x, y)
    drawRain()
    glutSwapBuffers()


# ===== Main entry point =====
def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"CSE423 Lab 1 Task 1")
    glutDisplayFunc(display)
    glutIdleFunc(rainFall)
    glutSpecialFunc(specialKeyListener)
    glutMainLoop()


# ===== Run the program =====
if __name__ == "__main__":
    main()






#----------------------------------------------------------------------------------
#Task 2
#####################################################################################

import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

W_Width, W_Height = 500, 500
create_new = []
speed = 1.0
min_speed = 0.0
max_speed = 10.0
flag = False
pause = False
blink_timer = 0
blink_visible = True

def convert_coordinate(x, y):
    return (x, W_Height - y)

def mouseListener(button, state, x, y):
    global create_new, pause, flag, blink_timer, blink_visible
    if not pause:
        if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
            coords = convert_coordinate(x, y)
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            direction = random.choice(directions)
            random_color = (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))
            create_new.append({
                'position': coords,
                'direction': direction,
                'color': random_color,
                'original_color': random_color
            })
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            flag = not flag
            blink_timer = 0
            blink_visible = True
    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global speed, pause, min_speed, max_speed
    if not pause:
        if key == GLUT_KEY_UP:
            speed *= 2
            if speed > max_speed:
                speed = max_speed
                print(f"Speed Increased")
            else:
                print(f"Speed Increased")
        if key == GLUT_KEY_DOWN:
            speed /= 2
            if speed < min_speed:
                speed = min_speed
                print(f"Speed  Decreased")
            else:
                print(f"Speed Decreased")
    glutPostRedisplay()

def keyboardListener(key, x, y):
    global pause
    if key == b' ':
        pause = not pause
    glutPostRedisplay()

def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    global create_new, flag, blink_visible
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    if create_new:
        for point in create_new:
            m, n = point['position']
            glPointSize(5.0)
            glBegin(GL_POINTS)
            if flag:
                if blink_visible:
                    glColor3f(point['original_color'][0], point['original_color'][1], point['original_color'][2])
                else:
                    glColor3f(0, 0, 0)
            else:
                glColor3f(point['color'][0], point['color'][1], point['color'][2])
            glVertex2f(m, n)
            glEnd()
    glutSwapBuffers()

def animate():
    global create_new, speed, W_Width, W_Height, pause, flag, blink_timer, blink_visible
    if not pause:
        if flag:
            blink_timer += 1
            if blink_timer >= 30:
                blink_visible = not blink_visible
                blink_timer = 0
        for point in create_new:
            x, y = point['position']
            dir_x, dir_y = point['direction']
            x += dir_x * speed
            y += dir_y * speed
            if x <= 0:
                x = 0
                dir_x = -dir_x
            elif x >= W_Width:
                x = W_Width
                dir_x = -dir_x
            if y <= 0:
                y = 0
                dir_y = -dir_y
            elif y >= W_Height:
                y = W_Height
                dir_y = -dir_y
            point['position'] = (x, y)
            point['direction'] = (dir_x, dir_y)
        glutPostRedisplay()

def main():
    glutInit()
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(0, 0)
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
    glutCreateWindow(b"CSE423 Lab 1 Task 2")
    glutDisplayFunc(showScreen)
    glutIdleFunc(animate)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutMainLoop()

if __name__ == "__main__":
    main()
