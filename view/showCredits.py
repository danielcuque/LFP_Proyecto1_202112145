from customtkinter import (
    CTkButton,
    CTkLabel,
    CTkToplevel,
)


class ShowCredits(CTkToplevel):
    WINDOW_WIDTH = 370
    WINDOW_HEIGHT = 200

    def __init__(self, master):
        super().__init__(master)

        self.title("Créditos")
        self.minsize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.geometry(
            f'{self.WINDOW_WIDTH - 100}x{self.WINDOW_HEIGHT - 100}+{int(self.WINDOW_WIDTH / 2)}+{int(self.WINDOW_HEIGHT / 2)}')
        # Course label
        course_label = CTkLabel(
            self, text="Lenguajes formales y de programación")
        course_label.pack(side="top", fill="both",
                          expand=True, pady=10, padx=10)
        # Students label
        students_label = CTkLabel(
            self, text="Desarrollado por Daniel Estuardo Cuque Ruíz",
            text_font=("Roboto Medium", -14),
            text_color="white")
        students_label.pack(side="top", fill="both",
                            expand=True, pady=10, padx=10)

        # ID student label
        id_student_label = CTkLabel(
            self, text="Carné: 202112145", text_font=("Roboto Medium", -14),
        )
        id_student_label.pack(side="top", fill="both",
                              expand=True, pady=10, padx=10)

        # Close button
        close_button = CTkButton(
            self, text="Cerrar", command=self.destroy)
        close_button.pack(side="top", fill="both",
                          expand=True, pady=10, padx=10)
