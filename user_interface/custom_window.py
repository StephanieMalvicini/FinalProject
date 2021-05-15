import tkinter as tk
from tkinter import ttk
import tkinter.font as font

from databases import decision_algorithms
from user_interface.decision_algorithm_editor import DecisionAlgorithmEditor
from user_interface.dialogs import CustomDialog
from user_interface.fairness_definitions_window.calculator import FairnessDefinitionsCalculatorUI
from user_interface.images import MainWindowImages
from user_interface.scrolled_frame import VerticalScrolledFrame

TOTAL_WIDTH = 1300
TOTAL_HEIGHT = 700
WINDOW_TITLE = "Evaluador de fairness"
ADD_DECISION_ALGORITHM = "Añadir \n clasificador/algoritmo \n de decisión"
CALCULATE_FAIRNESS_DEFINITIONS = "Calcular \n definiciones \n de fairness"


class CustomWindow:

    def __init__(self):
        self.window = tk.Tk()

        self.configure_window()
        self.dialog = self.create_custom_dialog()
        self.main_frame = self.create_main_frame()
        self.current_screen = None
        self.images = MainWindowImages()
        self.buttons_frame = self.create_buttons_frame()
        self.create_background()
        self.create_add_decision_algorithm_button()
        self.calculate_button = self.create_calculate_fairness_definitions_button()
        self.go_back_button = self.create_go_back_button()

        self.window.mainloop()

    def configure_window(self):
        self.window.title(WINDOW_TITLE)
        self.window.iconbitmap("images/icon.ico")
        self.window.geometry("{}x{}".format(TOTAL_WIDTH, TOTAL_HEIGHT))

    def create_custom_dialog(self):
        return CustomDialog(self.window)

    def create_main_frame(self):
        # Create a frame to put the VerticalScrolledFrame inside
        holder_frame = tk.Frame(self.window)
        holder_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        # Create the VerticalScrolledFrame
        vs_frame = VerticalScrolledFrame(holder_frame)
        vs_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=tk.TRUE)
        return vs_frame.interior

    def create_background(self):
        background = tk.Label(self.buttons_frame, image=self.images.background)
        background.grid(column=0, row=0, rowspan=3, columnspan=2, sticky=tk.SW, pady=(10, 0))

    def create_buttons_frame(self):
        frame = ttk.Frame(self.main_frame)
        frame.pack(fill=tk.X)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(2, weight=1)
        return frame

    def create_add_decision_algorithm_button(self):
        button = tk.Button(self.buttons_frame, text=ADD_DECISION_ALGORITHM, width=25,
                           height=8, command=self.add_decision_algorithm_button, bg="white")
        button["font"] = font.Font(size=12)
        button.grid(column=1, row=0, sticky=tk.E, padx=(0, 150), pady=(70, 0))

    def add_decision_algorithm_button(self):
        self.go_back_button.pack(anchor=tk.NW, pady=10, padx=10)
        self.buttons_frame.pack_forget()
        self.current_screen = DecisionAlgorithmEditor(self.main_frame, self.dialog)

    def create_calculate_fairness_definitions_button(self):
        button = tk.Button(self.buttons_frame, text=CALCULATE_FAIRNESS_DEFINITIONS, width=25,
                           height=8, command=self.calculate_fairness_definitions, bg="white")
        button["font"] = font.Font(size=12)
        button.grid(column=1, row=1, sticky=tk.E, padx=(0, 150), pady=(20, 0))
        if decision_algorithms.no_entries():
            button.config(state="disabled")
        return button

    def calculate_fairness_definitions(self):
        self.go_back_button.pack(anchor=tk.NW, pady=10, padx=10)
        self.buttons_frame.pack_forget()
        self.current_screen = FairnessDefinitionsCalculatorUI(TOTAL_WIDTH, self.dialog, self.main_frame)

    def create_go_back_button(self):
        button = tk.Button(self.main_frame, image=self.images.go_back, command=self.go_back,
                           highlightthickness=0, bd=0)
        return button

    def go_back(self):
        self.go_back_button.pack_forget()
        self.buttons_frame.pack()
        self.current_screen.destroy()
        self.current_screen = None
        if decision_algorithms.no_entries():
            self.calculate_button.config(state="disabled")
        else:
            self.calculate_button.config(state="normal")
