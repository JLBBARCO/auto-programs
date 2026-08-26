from pathlib import Path
import customtkinter as ctk


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("system")

        self.geometry("800x600")
        self.resizable(False, False)
        self.title("Programs Manager")

        icon_path = Path(__file__).resolve().parent / "assets" / "icons" / "icon.ico"
        if icon_path.is_file():
            self.iconbitmap(default=str(icon_path))


if __name__ == "__main__":
    app = App()
    app.mainloop()
