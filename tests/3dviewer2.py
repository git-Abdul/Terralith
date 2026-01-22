import pyvista as pv
import keyboard

plotter = pv.Plotter(window_size=(1000, 700))
plotter.set_background("#f4efe6")

mesh = pv.read("./assets/model.obj")
plotter.add_mesh(mesh)

plotter.camera_position = [
    (1.0, 0.0, 0.0),
    (0.0, 0.0, 0.0),
    (0.0, 0.0, 0.0)
]

plotter.enable_anti_aliasing("fxaa")
plotter.enable_eye_dome_lighting()
plotter.enable_3_lights()
plotter.reset_camera()
keyboard.on_press_key("R", plotter.reset_camera)

plotter.show()
