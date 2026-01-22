# CSE423 - Computer Graphics

This repository contains academic resources, lab work, and materials for the **Computer Graphics (CSE423)** course.

## Course Overview

Computer Graphics is a comprehensive course covering the fundamental concepts and practical implementations of graphics programming, including:

- **Introduction**: Overview of graphics systems, applications, and display technologies
- **Line Drawing**: DDA and Mid Point line drawing algorithms
- **Clipping**: Cohen-Sutherland and Cyrus beck clipping algorithms
- **Transformation**: 2D and 3D transformations (translation, rotation, scaling, etc)
- **Projection**: Parallel and perspective projections, viewing transformations
- **Color Model**: RGB, CMY, HSV color spaces
- **Lighting Model**: Ambient, diffuse, and specular lighting, Phong reflection model
- **Curves**: Continuity, Bezier curves, and parametric representations

## Repository Structure

```
CSE423/
├── Assignment/                      # Course assignments
├── Lab/                             # Lab assignments and exercises
├── Notes & Practice Sheet Solve/   # Course notes and practice materials
├── Previous Question/               # Previous exam questions and solutions
└── README.md                        # This file
```

## Lab Assignments

This repository contains Computer Graphics lab assignments implemented in **Python** using **PyOpenGL** and **GLUT**.

### **Lab 1: 2D Primitives & Animation**
*Focus: Basic OpenGL primitives (`GL_POINTS`, `GL_LINES`, `GL_TRIANGLES`), interaction, and animation.*
- **Task 1 (House in Rainfall):** A 2D scene featuring animated rain with wind direction control (arrow keys) and a day/night background transition.
![Lab 1 Task 1 - House in Rainfall](https://i.ibb.co.com/BHP5RdYb/L1-T1.jpg)
- **Task 2 (The Amazing Box):** An interactive simulation of bouncing points featuring mouse-click spawning, speed adjustments, and blink effects.
![Lab 1 Task 2 - The Amazing Box](https://i.ibb.co.com/TDvQtNSc/L1-T2.jpg)

### **Lab 2: Midpoint Line Drawing Algorithm**
*Focus: Scan conversion algorithms and 8-way symmetry.*
- **Project (Catch the Diamonds):** A falling-object game rendered entirely using the **Midpoint Line Drawing Algorithm** (generating lines using only `GL_POINTS`).
![Lab 2 - Catch the Diamonds](https://i.ibb.co.com/dwM6MZN1/L2.jpg)
- **Features:** Custom implementation of lines for all 8 zones, AABB collision detection, and interactive UI buttons (Pause, Resume, Restart).

### **Lab 3: 3D Transformations & Projections**
*Focus: 3D Coordinate systems, Geometric Transformations, and Camera Control.*
- **Project (Bullet Frenzy):** A 3D shooter game utilizing `gluPerspective` and `gluLookAt` for scene rendering.
![Lab 3 - Bullet Frenzy](https://i.ibb.co.com/7xsnjjw9/L3.jpg)
- **Features:**
  - **3D Modeling:** Hierarchical character models (Player, Enemies) built using cylinders and spheres.
  - **Camera:** Toggleable **First-Person** and **Third-Person** perspective modes.
  - **Mechanics:** Enemy pursuit AI, 3D collision detection, and an auto-aim "Cheat Mode".

## Course Project

**[View Project Repository](https://github.com/fah-ayon/StarWay-Survivor-3D-OpenGL-Space-Shooter)**

The project demonstrates advanced graphics concepts including:
- 3D object rendering
- Camera controls and perspective
- Collision detection
- Particle systems
- Game physics

## Technologies Used

- **OpenGL** - Graphics rendering
- **Python** - Programming language

## License

This repository is for academic purposes only.

---

## Author

**Abdullah Al Fahad**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/abdullahalfahadayon/)
[![Email](https://img.shields.io/badge/Email-Contact-red?style=flat&logo=gmail)](mailto:abdullah.al.fahad2@g.bracu.ac.bd)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=flat&logo=github)](https://github.com/fah-ayon)

---
