import customtkinter as ctk
from lib.json import read_internal_json
from lib.log import error


class InitialScreen(ctk.CTkFrame):
    def __init__(self, master, on_new_execution):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        self.frame_buttons = ctk.CTkFrame(self)
        self.frame_buttons.pack(pady=20, padx=20, fill="both", expand=True)

        self.title_frame_buttons = ctk.CTkLabel(self.frame_buttons, text="Select an option:", font=ctk.CTkFont(size=16, weight="bold"))
        self.title_frame_buttons.pack(pady=10, padx=10)


        self.button_backup = ctk.CTkButton(self.frame_buttons, text="Backup")
        if self.backup_file_read() is None or self.backup_file_read() == {}:
            self.button_backup.configure(state="disabled")
        self.button_backup.pack(pady=20, padx=20, side="left")

        self.button_new_execution = ctk.CTkButton(
            self.frame_buttons, text="New Execution", command=on_new_execution
        )
        self.button_new_execution.pack(pady=20, padx=20, side="right")


    def backup_file_read(self):
        try:
            backup_data = read_internal_json("backup")
        except Exception as e:
            error(f"Error reading backup data: {e}")
            return None
        return backup_data

