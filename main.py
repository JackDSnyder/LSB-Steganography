import customtkinter as ctk
from gui.mainGUI import MainWindow

def main():
    root = ctk.CTk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()