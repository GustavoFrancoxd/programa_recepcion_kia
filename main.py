import tkinter as tk
from controllers.citas_controller import CitasController

if __name__ == "__main__":
    root = tk.Tk()
    app = CitasController(root)
    root.mainloop()