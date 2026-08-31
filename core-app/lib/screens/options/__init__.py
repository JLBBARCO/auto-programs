from typing import Any, Tuple

import customtkinter as ctk


class OptionsScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)


        self.advanced_options = ctk.CTkSwitch(self, text='Advanced Options')
        self.advanced_options.pack(padx=10, pady=10, side='right')

        self.button_run = ctk.CTkButton(self, text='Run')
        self.button_run.pack(padx=10, pady=10, side='bottom')