# Solar System Simulation

## Overview
This 3D solar system simulation, built with Python, PyGame, and OpenGL in a Jupyter notebook, visualizes the Sun, eight planets, moons, an asteroid belt, comets, and a twinkling star skybox. Interactive camera controls and visual enhancements like orbital paths and comet trails make it an engaging tool for education or visualization.

## Features
- **Sun and Planets**: Includes the Sun and planets (Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune) with relative sizes, distances, orbits, and distinct colors (e.g., Earth: blue `(0, 0.5, 1)`, Mars: red `(1, 0.3, 0)`).
- **Moons**: Earth (1 moon), Mars (2), Jupiter (4), and Saturn (3) have orbiting moons with varied sizes and speeds.
- **Asteroid Belt**: 100 asteroids between Mars and Jupiter, with random sizes (0.05–0.1), grayish colors, and orbits.
- **Orbital Paths**: Faint gray circular paths show each planet’s orbit around the Sun.
- **Comets**: Three comets with alpha-blended trails move through the scene, visible from all perspectives.
- **Starry Skybox**: 1000 stars on a spherical background (radius 100) with slow twinkling (velocity: ±0.0005 radians/frame).
- **Camera Controls**: Mouse drag to rotate, scroll to zoom (10–60 units).
- **Lighting**: OpenGL lighting with ambient, diffuse, and specular components for realistic planet rendering.
- **Error Checking**: OpenGL error detection for debugging.

## Requirements
- Python 3.11+
- PyGame
- PyOpenGL
- NumPy
- Jupyter Notebook
- Optional: `space-rumble-29970.mp3` for background music (can be omitted)

## Installation
1. Install dependencies:
   ```bash
   pip install pygame PyOpenGL numpy jupyter
   ```
2. Save `solar_system.ipynb` in your working directory.
3. (Optional) Place `space-rumble-29970.mp3` in the same directory for music.
4. Run the notebook:
   ```bash
   jupyter notebook
   ```
   Open `solar_system.ipynb` and execute all cells.

## Running as a Standalone Script
1. Convert the notebook to a Python script:
   ```bash
   jupyter nbconvert --to script solar_system.ipynb
   ```
2. Run the script:
   ```bash
   python solar_system.py
   ```

## Controls
- **Left Mouse Drag**: Rotate camera.
- **Mouse Scroll Up/Down**: Zoom in/out (10–60 units).
- **Escape Key**: Exit simulation.

## Notes
- **Environment**: Optimized for Jupyter but works as a standalone script. Browser-based execution (e.g., Pyodide) may not support music due to file I/O restrictions.
- **GLError**: If `GLError: invalid operation` occurs on `glClear`, test in a standalone script or update OpenGL drivers.
- **Music**: Remove `pygame.mixer` code if `space-rumble-29970.mp3` is unavailable or for browser use.
- **Performance**: High object counts (1000 stars, 100 asteroids, 10 moons) may slow rendering. Reduce `num_stars` or `num_asteroids` in the code if needed.
- **Textures**: Texture support is included but not implemented due to file I/O limits. Add image files for desktop environments if desired.

## Potential Improvements
- Add planet/moon textures.
- Include moon orbital paths.
- Implement asteroid rotation.
- Convert to WebGL for browser compatibility.
- Add UI to toggle features (e.g., orbits, music).

## License
For educational and demonstration purposes. Modify and share freely with attribution.

## Contact
For issues or suggestions, contact the developer or refer to the project repository (if hosted).
