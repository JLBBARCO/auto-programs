from pathlib import Path
import customtkinter as ctk
from lib.log import info
from lib.screens import options


class App(ctk.CTk):
    info('Start system')
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("system")

        self.resizable(False, False)
        self.title("Programs Manager")

        icon_path = Path(__file__).resolve().parent / "assets" / "icons" / "icon.ico"
        if icon_path.is_file():
            self.iconbitmap(default=str(icon_path))

        self.options_screen = options.OptionsScreen(
            self
        )


    info("End system")


if __name__ == "__main__":
    app = App()
    app.mainloop()
