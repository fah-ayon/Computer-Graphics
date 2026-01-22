# ===== OpenGL 2D Point Drawing Example =====
# This program displays a single yellow point using PyOpenGL + GLUT.

from OpenGL.GL import *     # Core OpenGL functions (drawing, colors, etc.)
from OpenGL.GLUT import *   # GLUT library (window creation, display, loop)
from OpenGL.GLU import *    # OpenGL Utility Library (projection utilities)
import random
# --- Global coordinates of the point ---
x, y = 250, 250


# ===== Function to draw a single point =====
def draw_points(x, y):
    glPointSize(15)          # Set pixel size of the point (default = 1)
    glBegin(GL_POINTS)      # Start drawing points
    glVertex2f(450,450)        # Specify the (x, y) coordinate of the point
    glColor3f(1, 1, 0)     
    glVertex2f(100,100)
    glColor3f(random.random(),random.random(),random.random()) 
    glVertex2f(400,300)
    glEnd()        
    
    
    glLineWidth(2)
    glColor3f(1, 1, 1)
    glBegin(GL_LINES)
    glVertex2f(250,0)
    glVertex2f(250,500)
    glEnd()
    
    glLineWidth(2)
    glColor3f(0, 1, 1)
    glBegin(GL_LINES)
    glVertex2f(0,250)
    glVertex2f(500,250)
    glEnd()
    
    glBegin(GL_QUADS)
    glColor3f(1,1,0)
    glVertex2f(300,300)
    glColor3f(1,0,1)
    glVertex2f(200,300)
    glColor3f(0,1,1)
    glVertex2f(200,200)
    glColor3f(1,1,1)
    glVertex2f(300,200)
    glEnd()
    
    glColor3f(1,0,0)
    glBegin(GL_TRIANGLES)
    glColor3f(random.random(),random.random(),random.random()) 
    glVertex2f(400,250)
    glColor3f(random.random(),random.random(),random.random()) 
    glVertex2f(300,300)
    glColor3f(random.random(),random.random(),random.random()) 
    glVertex2f(300,200)
    glEnd()
    
    


# ===== Set up 2D coordinate system =====
def setup_projection():
    glViewport(0, 0, 500, 500)     # Define the portion of the window to render to
    glMatrixMode(GL_PROJECTION)    # Switch to the projection matrix
    glLoadIdentity()               # Reset the projection matrix
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)  # Define a 2D orthographic projection
    glMatrixMode(GL_MODELVIEW)     # Switch back to the modelview matrix


# ===== Display callback =====
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear screen and depth buffer
    glLoadIdentity()                                    # Reset transformations
    setup_projection()                                  # Set up coordinate system
    glColor3f(0.5, 0.7, 0.3)                            # Set color (R, G, B) → Yellow
    draw_points(x, y)                                   # Draw the point
    glutSwapBuffers()                                   # Swap buffers (double buffering)


# ===== Main entry point =====
def main():
    glutInit()                               # Initialize GLUT
    glutInitDisplayMode(GLUT_RGBA)           # Set display mode: RGBA color
    glutInitWindowSize(500, 500)             # Set window size (width, height)
    glutInitWindowPosition(0, 0)             # Set window position (top-left corner)
    glutCreateWindow(b"CSE423 lab 1")     # Create window with a title
    glutDisplayFunc(display)                 # Register display callback
    glutMainLoop()                           # Start the main event-processing loop


# ===== Run the program =====
if __name__ == "__main__":
    main()
