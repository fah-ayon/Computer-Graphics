from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

cam_dist = 500
cam_height = 500
cam_angle = 0 
field_view_Y = 100
GRID_LENGTH = 100
GRID_SIZE = 14
min_bound = -GRID_SIZE * GRID_LENGTH // 2
max_bound = GRID_SIZE * GRID_LENGTH // 2

p_pos = [0, 0, 0]
p_angle = 0


camera_mode = "third"
game_over = False
bullets = []
enemies = []
num_enemies = 5
life = 5
missed_bullets = 0
score = 0
cheat = False
gun = False


lastx, lasty, lastz = 0.1, 0.1, 55.0
last_look_x, last_look_y = 1.0, 1.0 


def text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 600)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def grid():
    glBegin(GL_QUADS)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if (i + j) % 2 == 0:
                glColor3f(1, 1, 1)
            else:
                glColor3f(0.7, 0.5, 0.95)
            x = (i - GRID_SIZE // 2) * GRID_LENGTH
            y = (j - GRID_SIZE // 2) * GRID_LENGTH
            glVertex3f(x, y, 0)
            glVertex3f(x + GRID_LENGTH, y, 0)
            glVertex3f(x + GRID_LENGTH, y + GRID_LENGTH, 0)
            glVertex3f(x, y + GRID_LENGTH, 0)
    glEnd()


def walls():
    wall_height = 100
    offset = GRID_LENGTH * GRID_SIZE // 2
    glBegin(GL_QUADS)
    
    
    glColor3f(0.01, 0.9, 1)
    glVertex3f(-offset, -offset, 0)
    glVertex3f(offset, -offset, 0)
    glVertex3f(offset, -offset, wall_height)
    glVertex3f(-offset, -offset, wall_height)
    
    glColor3f(1, 1, 1)
    glVertex3f(-offset, offset, 0)
    glVertex3f(offset, offset, 0)
    glVertex3f(offset, offset, wall_height)
    glVertex3f(-offset, offset, wall_height)
    
    glColor3f(0, 0, 1)
    glVertex3f(-offset, -offset, 0)
    glVertex3f(-offset, offset, 0)
    glVertex3f(-offset, offset, wall_height)
    glVertex3f(-offset, -offset, wall_height)
    
    glColor3f(0.01, 0.9, 0.01)
    glVertex3f(offset, -offset, 0)
    glVertex3f(offset, offset, 0)
    glVertex3f(offset, offset, wall_height)
    glVertex3f(offset, -offset, wall_height)
    
    glEnd()


def player():
    glPushMatrix()
    glTranslatef(p_pos[0], p_pos[1], p_pos[2])
    glRotatef(p_angle, 0, 0, 1)
    
    if game_over: 
        glRotatef(90, 0, 1, 0) 

    #Leg
    glColor3f(0.0, 0.0, 0.8)
    for side in [-10, 10]:
        glPushMatrix()
        glTranslatef(0, side, 0)
        gluCylinder(gluNewQuadric(), 8, 8, 15, 10, 10) 
        glPopMatrix()

    #Body
    glColor3f(0.4, 0.6, 0.2)
    glPushMatrix()
    glTranslatef(0, 0, 25)
    glScalef(30, 20, 30)
    glutSolidCube(1)
    glPopMatrix()

    #Gun
    glColor3f(0.7, 0.7, 0.7)
    glPushMatrix() 
    glTranslatef(15, 0, 35) 
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 5, 5, 60, 10, 10)
    glPopMatrix()

    #Arm
    glColor3f(0.94, 0.81, 0.70)
    for side in [-15, 15]:
        glPushMatrix()
        glTranslatef(0, side, 35)
        glRotatef(90, 0, 1, 0)
        gluCylinder(gluNewQuadric(), 5, 5, 25, 10, 10)
        glPopMatrix()

    #Head
    glColor3f(0.0, 0.0, 0.0) 
    glPushMatrix()
    glTranslatef(0, 0, 50)
    gluSphere(gluNewQuadric(), 15, 20, 20)
    glPopMatrix()
    
    glPopMatrix()
    

def bullet_maker():
    glColor3f(1, 0, 0)
    for bullet in bullets:
        glPushMatrix()
        glTranslatef(*bullet['pos'])
        glutSolidCube(10)
        glPopMatrix()


def enemy_func(e):
    glPushMatrix()
    glTranslatef(*e['pos'])
    glScalef(e["scale"], e["scale"], e["scale"])
    
    # Body
    glColor3f(1, 0, 0)
    glPushMatrix()
    glTranslatef(0, 0, 40)
    gluSphere(gluNewQuadric(), 40, 20, 20)
    glPopMatrix()
    
    # Head
    glColor3f(0, 0, 0)
    glPushMatrix()
    glTranslatef(0, 0, 80)
    gluSphere(gluNewQuadric(), 30, 20, 20)
    glPopMatrix()
    glPopMatrix()


def enemy_respawn():
    while True:
        x = random.randint(-600, 500)
        y = random.randint(-600, 500)
        if abs(x) > 200 or abs(y) > 200:
            break
    return {'pos': [x, y, 0], 'scale': 1.0, 'scale_dir': 0.005}


def keyboardListener(key, x, y):
    global p_pos, p_angle, camera_mode, life, missed_bullets, score
    global game_over, cheat, gun, lastx, lasty, lastz, last_look_x, last_look_y
    global enemies, bullets
    
    speed = 20
    rad = math.radians(p_angle)
    

    if key == b'r' or key == b'R':
        if game_over:
            score = 0
            life = 5
            missed_bullets = 0
            p_pos = [0, 0, 0]
            p_angle = 0
            game_over = False
            cheat = False
            gun = False
            camera_mode = "third"
            bullets.clear()
            enemies.clear()
            
            for i in range(num_enemies):
                enemies.append(enemy_respawn())
                
            print("Game Restarted")
            return

    if not game_over:
        if key == b'w':
            p_pos[0] += math.cos(rad) * speed
            p_pos[1] += math.sin(rad) * speed
        elif key == b's':
            p_pos[0] -= math.cos(rad) * speed
            p_pos[1] -= math.sin(rad) * speed
        elif key == b'a':
            p_angle += 5
        elif key == b'd':
            p_angle -= 5
        elif key == b'c':
            cheat = not cheat
        elif key == b'v':
            if camera_mode == "first" and cheat:
                gun = not gun
                if gun: 
                    rad = math.radians(p_angle)
                    lastx = p_pos[0] 
                    lasty = p_pos[1]
                    lastz = 80.0 
                    last_look_x = lastx + math.cos(rad) * 100
                    last_look_y = lasty + math.sin(rad) * 100
                    print(f"Camera Frozen")


def specialKeyListener(key, x, y):
    global cam_height, cam_angle
    
    if key == GLUT_KEY_UP and cam_height < 800:
        cam_height += 10
    if key == GLUT_KEY_DOWN and cam_height > 50:
        cam_height -= 10
    if key == GLUT_KEY_LEFT:
        cam_angle += 5
    if key == GLUT_KEY_RIGHT:
        cam_angle -= 5
    cam_angle %= 360


def mouseListener(button, state, x, y):
    global camera_mode, bullets
    
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and not game_over:
        rad = math.radians(p_angle)
        bullet_start = [p_pos[0] + math.cos(rad) * 80, p_pos[1] + math.sin(rad) * 80, 30]
        bullets.append({'pos': bullet_start, 'dir': (math.cos(rad), math.sin(rad))})
        
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN and not game_over:
        if camera_mode == "third":
            camera_mode = "first"
        else:
            camera_mode = "third"


def setupCamera():
    global lastx, lasty, lastz, last_look_x, last_look_y
    global p_pos, camera_mode, cheat, gun, field_view_Y
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    aspect = 1.25
    gluPerspective(field_view_Y, aspect, 0.1, 1500) 
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    

    px, py, pz = p_pos[0], p_pos[1], p_pos[2]
    
    if camera_mode == "third":
        theta = math.radians(cam_angle)
        eye_x = cam_dist * math.cos(theta)
        eye_y = cam_dist * math.sin(theta)
        
        gluLookAt(eye_x, eye_y, cam_height, 0, 0, 0, 0, 0, 1)
        
    elif camera_mode == "first":
        if cheat and gun:
            target_h = 55.0
            gluLookAt(
                lastx, lasty, lastz, 
                last_look_x, last_look_y, target_h, 
                0, 0, 1
            )                  
        else:
            angle_rad = math.radians(p_angle)
            offset = 30
            

            eye_x = px + math.cos(angle_rad) * offset
            eye_y = py + math.sin(angle_rad) * offset
            eye_z = 55
            look_dist = 100
            at_x = eye_x + math.cos(angle_rad) * look_dist
            at_y = eye_y + math.sin(angle_rad) * look_dist
            at_z = 55
            
            gluLookAt(eye_x, eye_y, eye_z, at_x, at_y, at_z, 0, 0, 1)


def game_logic():
    global bullets, enemies, missed_bullets, score, life, game_over
    global p_angle, cheat, p_pos
    
    for bullet in bullets:
        bullet['pos'][0] += bullet['dir'][0] * 15
        bullet['pos'][1] += bullet['dir'][1] * 15
    
    b = 0
    while b < len(bullets):
        bx, by = bullets[b]['pos'][0], bullets[b]['pos'][1]
        if abs(bx) >= 600 or abs(by) >= 600:
            bullets.pop(b)
            missed_bullets += 1
        else: 
            b += 1
    

    new_enemies = []
    hit_bullets = []
    for e in enemies:
        hit = False
        ex, ey = e['pos'][0], e['pos'][1] 
        
        for b_obj in bullets:
            bx, by = b_obj['pos'][0], b_obj['pos'][1] 
            
            if abs(bx - ex) < 45 and abs(by - ey) < 45:
                hit = True
                score += 1
                hit_bullets.append(b_obj)
                break
        
        if hit: 
            new_enemies.append(enemy_respawn())
        else: 
            new_enemies.append(e)
    

    for b_obj in hit_bullets:
        if b_obj in bullets: 
            bullets.remove(b_obj)
    enemies[:] = new_enemies


    for e in enemies:
        ex, ey = e['pos'][0], e['pos'][1]
        px, py = p_pos[0], p_pos[1]
        
        dx = px - ex
        dy = py - ey
        dist = math.sqrt(dx**2 + dy**2)
        
        if dist > 1:
            e['pos'][0] += dx / dist * 0.5
            e['pos'][1] += dy / dist * 0.5
        
        e['scale'] += e['scale_dir']
        if e['scale'] >= 1.2 or e['scale'] <= 0.8: 
            e['scale_dir'] *= -1

    if not game_over:
        px, py = p_pos[0], p_pos[1] 
        
        for e in enemies:
            ex, ey = e['pos'][0], e['pos'][1]
            if abs(px - ex) < 50 and abs(py - ey) < 50: 
                if not cheat:
                    life -= 1
                    enemies.remove(e)
                    enemies.append(enemy_respawn())
                    print(f"Player Hit, Life remaining: {life}")
                else:
                    enemies.remove(e)
                    enemies.append(enemy_respawn())
                break 

    if cheat and not game_over:
        p_angle = (p_angle + 6) % 360 
        rad = math.radians(p_angle)
        
        look_x, look_y = math.cos(rad), math.sin(rad)
        px, py = p_pos[0], p_pos[1]
        
        for e in enemies:
            ex, ey = e['pos'][0], e['pos'][1]
            dx, dy = ex - px, ey - py
            dist = math.sqrt(dx**2 + dy**2)
            
            if dist<600 and dist>1:
                target_dir_x = dx / dist
                target_dir_y = dy / dist
                alignment = (look_x * target_dir_x + look_y * target_dir_y)   
            
                if alignment > 0.99:
                    curr_time = glutGet(GLUT_ELAPSED_TIME) / 1000.0
                    
                    if not hasattr(game_logic, "last_fire"): 
                        game_logic.last_fire = 0
                    if curr_time - game_logic.last_fire > 0.3:
                        bullets.append({'pos': [px + target_dir_x * 85, py + target_dir_y * 85, 30], 'dir': (target_dir_x, target_dir_y)})
                        game_logic.last_fire = curr_time
                        break


    if not cheat:
        if missed_bullets >= 10 or life <= 0:
            game_over = True

def idle(): 
    game_logic()
    glutPostRedisplay()


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    setupCamera()
    grid()
    walls()
    
    if not game_over:
        text(10, 560, f"Player Life Remaining: {life}")
        text(10, 540, f"Game Score: {score}")
        text(10, 520, f"Player Bullet Missed: {missed_bullets}")
        player()
        bullet_maker()
        for e in enemies:
            enemy_func(e)
    else:
        text(10, 560, f"Game is Over. Your score is {score}.")
        text(10, 540, f'Press "R" to RESTART the Game.')
        player() 

    glutSwapBuffers()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutCreateWindow(b"CSE423 Assignment 3")
    glEnable(GL_DEPTH_TEST)
    
    for i in range(num_enemies):
        enemies.append(enemy_respawn())
    
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    glutMainLoop()

if __name__ == "__main__":
    main()