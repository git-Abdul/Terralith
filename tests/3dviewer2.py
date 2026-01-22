import pyvista as pv

plotter = pv.Plotter(window_size=(1000, 700))
plotter.set_background("#f4efe6")

mesh = pv.read("model.obj")
plotter.add_mesh(mesh)

plotter.camera_position = [
    (1.0, 0.0, 0.0),
    (0.0, 0.0, 0.0),
    (0.0, 0.0, 0.0)
]

plotter.enable_anti_aliasing("fxaa")
plotter.enable_eye_dome_lighting()
plotter.reset_camera()

plotter.show()
