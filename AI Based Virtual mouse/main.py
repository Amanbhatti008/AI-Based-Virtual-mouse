from gui.gui import start_gui
from core.mouse_controller import start_mouse_control
from threading import Thread

if __name__ == "__main__":
    Thread(target=start_gui, daemon=True).start()
    start_mouse_control()
