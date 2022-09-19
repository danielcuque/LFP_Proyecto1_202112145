from platform import system
from tkinter import (
    filedialog,
    Menu,
    messagebox,
    Text
)

import customtkinter as ctk
from typing import List

# Data
from controller.lexer import Lexer
from controller.token import Token

# Model
from model.helpers.windowPosition import get_window_position
from model.docs.processInformation import read_information, save_information, save_information_as
from model.docs.htmlFile import HTMLFile
from model.operations.executeOperation import ExecuteOperation

# Views
from view.showCredits import ShowCredits

# # Modes: "System" (standard), "Dark", "Light"
ctk.set_appearance_mode("dark")

# # Themes: "blue" (standard), "green", "dark-blue"
ctk.set_default_color_theme("blue")


class App(ctk.CTk):

    # Size of the window
    APP_WIDTH: int = 1096
    APP_HEIGHT: int = 700

    PATH_FILE: str = ""
    VALID_TOKENS: List[Token] = []
    INVALID_TOKENS: List[Token] = []
    RESULT_OF_OPERATIONS: List[str] = []

    def __init__(self):
        super().__init__()

        # Set minimum size of window
        self.minsize(self.APP_WIDTH, self.APP_HEIGHT)
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        command_to_execute = ""
        my_os = system()

        if my_os == "Windows":
            command_to_execute = "Ctrl"
        elif my_os == "Darwin":
            command_to_execute = "Cmd"

        # Position of the app
        self.geometry(get_window_position(self.winfo_screenwidth(
        ), self.winfo_screenheight(), self.APP_WIDTH, self.APP_HEIGHT))

        self.title("Analizador")

        # Custom grid layout (2x1)
        # create 2x1 grid system
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Menu
        self.menu_options = Menu(self)
        self.config(menu=self.menu_options)

        # Menu File
        self.file_menu = Menu(self.menu_options, tearoff=0)
        self.file_menu.add_command(label="Abrir", command=self.open_file,
                                   accelerator=f"{command_to_execute}+O")

        self.file_menu.add_separator()

        self.file_menu.add_command(
            label="Guardar", command=self.save_file, accelerator=f'{command_to_execute}+S')
        self.file_menu.add_command(
            label="Guardar como", command=self.save_file_as, accelerator=f"{command_to_execute}+Shift+S")

        # Menu Tools
        self.scanner_menu = Menu(self.menu_options, tearoff=0)
        self.scanner_menu.add_command(
            label="Analizar", command=self.scanner, accelerator=f"{command_to_execute}+r")
        self.scanner_menu.add_command(
            label="Resultados", command=self.show_results, accelerator=f'{command_to_execute}+p')
        self.scanner_menu.add_command(
            label="Errores", command=self.show_errors, accelerator=f'{command_to_execute}+e')

        # Menu Help
        self.help_menu = Menu(self.menu_options, tearoff=0)
        self.help_menu.add_command(
            label="Guía de usuario", command=self.about_creator, accelerator=f"{command_to_execute}+U")
        self.help_menu.add_command(
            label="Guía técnica", command=self.about_creator, accelerator=f"{command_to_execute}+T")
        self.help_menu.add_command(
            label="Temas de ayuda", command=self.about_creator, accelerator=f'{command_to_execute}+t')

        # Add menus to menu bar
        self.exit_menu = Menu(self.menu_options, tearoff=0)
        self.exit_menu.add_command(
            label="Salir", command=self.destroy, accelerator=f"{command_to_execute}+Q")

        # Adding menus to menu bar
        self.menu_options.add_cascade(label="Archivo", menu=self.file_menu)
        self.menu_options.add_cascade(
            label="Analizador", menu=self.scanner_menu)
        self.menu_options.add_cascade(label="Ayuda", menu=self.help_menu)
        self.menu_options.add_cascade(label="Salir", menu=self.exit_menu)

        ''' ====== Information frame ====== '''
        self.entry_information = Text(self, width=50)
        self.entry_information.grid(
            row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.create_short_cut()

    def about_creator(self):
        ShowCredits(master=self)

    def open_file(self):
        path_file = filedialog.askopenfilename(
            initialdir="/", title="Select file", filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
        if len(path_file) <= 0:
            messagebox.showerror(
                "Error", "No se ha seleccionado ningún archivo")
        else:
            self.PATH_FILE = path_file
            uploaded_information: str = read_information(
                self.PATH_FILE)

            if len(uploaded_information) <= 0:
                messagebox.showerror(
                    "Error", "No se ha podido cargar el archivo")
            else:
                self.show_info_file(uploaded_information)

    def show_info_file(self, uploaded_information: str):
        self.entry_information.insert("1.0", uploaded_information)

    def save_file(self):
        information: str = self.entry_information.get("1.0", "end-1c")
        save_information(self.PATH_FILE, information)

    def save_file_as(self):
        path_to_save = filedialog.asksaveasfilename(
            initialdir="/", title="Select file", filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
        if len(path_to_save) > 0:
            information: str = self.entry_information.get("1.0", "end-1c")
            save_information_as(path_to_save, information)
            self.PATH_FILE = path_to_save

    def scanner(self):
        information: str = self.entry_information.get("1.0", "end-1c")
        if len(information) <= 0:
            messagebox.showerror(
                "Error", "No hay texto para analizar")
        else:
            scanner: Lexer = Lexer(information)
            scanner.fill_table_of_tokens()

            self.VALID_TOKENS = scanner.get_table_of_valid_tokens()
            self.INVALID_TOKENS = scanner.get_table_of_invalid_tokens()
            self.RESULT_OF_OPERATIONS = ExecuteOperation(self.VALID_TOKENS).get_result_operations()

            print(self.VALID_TOKENS)
            print(self.INVALID_TOKENS)

            messagebox.showinfo(
                "Información", "El archivo se ha analizado correctamente")

    def show_results(self):
        if len(self.RESULT_OF_OPERATIONS) > 0:
            html_file = HTMLFile(self.VALID_TOKENS)
            html_file.report_of_operations(self.RESULT_OF_OPERATIONS)
        else:
            messagebox.showerror(
                "Error", "No hay resultados para mostrar")

    def show_errors(self):
        print(len(self.INVALID_TOKENS))
        if len(self.INVALID_TOKENS) > 0:
            html_file = HTMLFile(self.VALID_TOKENS)
            html_file.report_of_errors(self.INVALID_TOKENS)
        else:
            messagebox.showerror(
                "Error", "No hay errores para mostrar")

    def destroy(self):
        if messagebox.askokcancel("Salir", "¿Desea salir de la aplicación?"):
            if self.PATH_FILE:
                self.save_file()
            super().destroy()

    def create_short_cut(self):
        self.bind_all("<Command-o>", lambda event: self.open_file())
        self.bind_all("<Command-p>", lambda event: self.show_results())
        self.bind_all("<Command-q>", lambda event: self.destroy())
        self.bind_all("<Command-s>", lambda event: self.save_file())
        self.bind("<Command-Shift-s>", lambda event: self.save_file_as())
        self.bind_all("<Command-r>", lambda event: self.scanner())
        self.bind_all("<Command-t>", lambda event: self.about_creator())
        self.bind_all("<Command-Shift-t>", lambda event: self.about_creator())
        self.bind_all("<Command-Shift-u>", lambda event: self.about_creator())


if __name__ == "__main__":
    app = App()
    app.mainloop()
