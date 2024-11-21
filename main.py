import time
import curses
from engine import Engine
from scene import Scene
from camera import Camera
from renderer import Renderer
from input_handler import InputHandler
from object import Cube, Plane
from vector import Vector3

def initialize_demo_scene(scene):
    """Initialize scene with demo objects"""
    # Add a cube
    cube = Cube(2.0)
    cube.translate(0, 0, 0)
    scene.add_object(cube)
    
    # Add a ground plane
    ground = Plane(10.0, 10.0)
    ground.translate(0, -2, 0)
    scene.add_object(ground)
    
    return scene

def main():
    """
    Main function to initialize and run the 3D engine
    """
    try:
        # Create main components
        scene = Scene()
        scene = initialize_demo_scene(scene)
        camera = Camera(position=(0, 0, -10), target=(0, 0, 0))
        renderer = Renderer()
        input_handler = InputHandler()
        
        # Create and initialize engine
        engine = Engine(scene, camera, renderer, input_handler)
        engine.initialize()
        
        # Main loop variables
        target_fps = 30
        frame_time = 1.0 / target_fps
        last_time = time.time()
        
        try:
            # Main game loop
            while True:
                current_time = time.time()
                delta_time = current_time - last_time
                
                if delta_time >= frame_time:
                    # Process input
                    input_handler.process_input()
                    
                    # Update game state
                    engine.update(delta_time)
                    
                    # Render frame
                    engine.render()
                    
                    last_time = current_time
                else:
                    # Sleep to maintain frame rate
                    time.sleep(0.001)
                    
        except KeyboardInterrupt:
            pass
            
    except Exception as e:
        print(f"\nError: {str(e)}")
    finally:
        # Cleanup engine (which handles curses cleanup)
        if 'engine' in locals():
            engine.cleanup()

if __name__ == "__main__":
    main()