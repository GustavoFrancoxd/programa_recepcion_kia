# main.py
import tkinter as tk
import sys
from pathlib import Path

# Configuración de paths
BASE_DIR = Path(__file__).parent
sys.path.append(str(BASE_DIR))

# Importación absoluta desde controllers
from controllers.citas_controller import CitasController

if __name__ == "__main__":
    root = tk.Tk()
    app = CitasController(root)
    root.mainloop()