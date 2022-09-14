from tkinter import filedialog, messagebox, Text
import customtkinter as ctk

# Data

# Helpers
from model.helpers.WindowPosition import WindowPosition
from model.docs.processInformation import ProcessInformation

# Views

# # Modes: "System" (standard), "Dark", "Light"
ctk.set_appearance_mode("dark")

# # Themes: "blue" (standard), "green", "dark-blue"
ctk.set_default_color_theme("blue")


class App(ctk.CTk):

    # Size of the window
    APP_WIDTH: int = 1096
    APP_HEIGHT: int = 700

    PATH_FILE: str = ""

    def __init__(self):
        super().__init__()

        # Set minimum size of window
        self.minsize(self.APP_WIDTH, self.APP_HEIGHT)
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        # Position of the app
        self.geometry(WindowPosition().get_window_position(self.winfo_screenwidth(
        ), self.winfo_screenheight(), self.APP_WIDTH, self.APP_HEIGHT))

        self.title("Analizador")

        # Custom grid layout (2x1)
        # create 2x1 grid system
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create a side menu
        self.side_menu = ctk.CTkFrame(self,
                                      width=200, corner_radius=0)
        self.side_menu.grid(row=0, column=0, sticky="nswe")

        '''====== Side menu buttons ======'''
        self.side_menu.grid_rowconfigure(0, minsize=10)
        self.side_menu.grid_rowconfigure((4, 10), weight=1)
        self.side_menu.grid_rowconfigure(11, minsize=10)

        # Create widgets
        self.upload_file_button = ctk.CTkButton(
            self.side_menu, text="Abrir",
            command=self.open_file)

        self.upload_file_button.grid(
            row=0, column=0, sticky="nsew", padx=15, pady=15)

        self.save_file_button = ctk.CTkButton(
            self.side_menu, text="Guardar",
            command=self.save_file)

        self.save_file_button.grid(
            row=1, column=0, sticky="nsew", padx=15, pady=15)

        self.scanner_button = ctk.CTkButton(
            self.side_menu, text="Analizar",
        )

        self.scanner_button.grid(
            row=2, column=0, sticky="nsew", padx=15, pady=15)

        self.errors_button = ctk.CTkButton(
            self.side_menu, text="Errores",
        )

        self.errors_button.grid(
            row=3, column=0, sticky="nsew", padx=15, pady=15)

        # Help buttons
        self.user_guide_button = ctk.CTkButton(
            self.side_menu, text="Guía de usuario",
        )

        self.user_guide_button.grid(
            row=7, column=0, sticky="nsew", padx=15, pady=15)

        self.tecnical_guide_button = ctk.CTkButton(
            self.side_menu, text="Guía técnica",
        )

        self.tecnical_guide_button.grid(
            row=8, column=0, sticky="nsew", padx=15, pady=15)

        self.helpul_topics_button = ctk.CTkButton(
            self.side_menu, text="Temas útiles",
        )

        self.helpul_topics_button.grid(
            row=9, column=0, sticky="nsew", padx=15, pady=15)

        self.exit_button = ctk.CTkButton(
            self.side_menu, text="Salir", command=self.destroy)
        self.exit_button.grid(
            row=11, column=0, sticky="nsew", padx=10, pady=20)

        ''' ====== Information frame ====== '''
        self.information_frame = ctk.CTkLabel(master=self,
                                              text="Cargue un archivo para comenzar",
                                              height=50,
                                              corner_radius=6,
                                              text_font=("Roboto Medium", -25), text_color="white",
                                              fg_color=("white", "gray38"),
                                              )
        self.information_frame.grid(
            row=0, column=1, sticky="nswe", padx=10, pady=10)

        self.disabled_buttons()

    def disabled_buttons(self):
        self.save_file_button.configure(state="disabled")
        self.scanner_button.configure(state="disabled")
        self.errors_button.configure(state="disabled")

    def enabled_buttons(self):
        self.save_file_button.configure(state="normal")
        self.scanner_button.configure(state="normal")
        self.errors_button.configure(state="normal")

    def open_file(self):
        path_file = filedialog.askopenfilename(
            initialdir="/", title="Select file", filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
        if len(path_file) <= 0:
            messagebox.showerror(
                "Error", "No se ha seleccionado ningún archivo")
        else:
            self.PATH_FILE = path_file
            uploaded_information: str = ProcessInformation.read_information(
                self.PATH_FILE)

            if len(uploaded_information) <= 0:
                messagebox.showerror(
                    "Error", "No se ha podido cargar el archivo")
            else:
                self.show_info_file(uploaded_information)

    def show_info_file(self, uploaded_inforation: str):
        self.entry_information = Text(self.information_frame, width=50)
        self.entry_information.grid(
            row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.entry_information.insert("1.0", uploaded_inforation)

        self.enabled_buttons()

    def save_file(self):
        if len(self.PATH_FILE) <= 0:
            messagebox.showerror(
                "Error", "No se ha cargado ningún archivo")
        else:
            information: str = self.entry_information.get("1.0", "end-1c")
            ProcessInformation.save_information(self.PATH_FILE, information)

    def destroy(self):
        return super().destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
