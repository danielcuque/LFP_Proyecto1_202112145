from tkinter import filedialog, messagebox
import customtkinter as ctk

# Data

# Helpers
from model.helpers.WindowPosition import WindowPosition

# Views

# # Modes: "System" (standard), "Dark", "Light"
ctk.set_appearance_mode("dark")

# # Themes: "blue" (standard), "green", "dark-blue"
ctk.set_default_color_theme("blue")


class App(ctk.CTk):

    # Size of the window
    APP_WIDTH: int = 1096
    APP_HEIGHT: int = 700

    def __init__(self):
        super().__init__()

        # Set minimum size of window
        self.minsize(self.APP_WIDTH, self.APP_HEIGHT)
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        # Position of the app
        self.geometry(WindowPosition().get_window_position(self.winfo_screenwidth(
        ), self.winfo_screenheight(), self.APP_WIDTH, self.APP_HEIGHT))

        self.title("Simulación de enfermedades")

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
        self.side_menu.grid_rowconfigure(5, weight=1)
        self.side_menu.grid_rowconfigure(8, minsize=20)
        self.side_menu.grid_rowconfigure(11, minsize=10)
        # Create widgets
        self.upload_file_button = ctk.CTkButton(
            self.side_menu, text="Abrir",
        )
        self.upload_file_button.grid(
            row=0, column=0, sticky="nsew", padx=15, pady=15)

        self.save_file_button = ctk.CTkButton(
            self.side_menu, text="Guardar",
        )

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

        # Components
        # self.side_title = ctk.CTkLabel(self.side_menu, text="Simulaciones de:")
        # self.side_title.grid(row=1, column=0, pady=10, padx=10)

        self.exit_button = ctk.CTkButton(
            self.side_menu, text="Salir", command=self.destroy)
        self.exit_button.grid(
            row=11, column=0, sticky="nsew", padx=10, pady=20)

        ''' ====== Simulation frame ====== '''
        self.simulation_frame = ctk.CTkLabel(master=self,
                                             text="No hay patientes cargados",
                                             height=50,
                                             corner_radius=6,
                                             text_font=("Roboto Medium", -25), text_color="white",
                                             fg_color=("white", "gray38"),
                                             )
        self.simulation_frame.grid(
            row=0, column=1, sticky="nswe", padx=10, pady=10)

    # def create_button_for_patient(self, name, index):
    #     button_for_patient = ctk.CTkButton(
    #         self.side_menu, text=name, command=lambda: self.display_frame_simulation(name))
    #     button_for_patient.grid(
    #         row=index, column=0, sticky="nsew", padx=10, pady=10)

    def destroy(self):
        return super().destroy()

    def change_message(self):
        self.simulation_frame.configure(
            text="Escoger un patiente para simular")


if __name__ == "__main__":
    app = App()
    app.mainloop()
