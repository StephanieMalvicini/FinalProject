import os
import tkinter as tk
from tkinter import ttk

from user_interface.decision_algorithm_editor import DecisionAlgorithmEditor
from user_interface.dialogs import CustomDialog
from user_interface.fairness_definitions_calculator import FairnessDefinitionsCalculator
from user_interface.images import GoBackButtonImage
from user_interface.scrolled_frame import VerticalScrolledFrame


TOTAL_WIDTH = 1300
TOTAL_HEIGHT = 700


class CustomWindow:

    def __init__(self):
        self.window = tk.Tk()

        self.configure_window()
        self.style = self.configure_theme()
        self.dialog = self.create_custom_dialog()
        self.main_frame = self.create_main_frame()
        self.current_screen = None
        self.buttons_frame = ttk.Frame(self.main_frame)
        self.buttons_frame.pack()
        self.create_add_decision_algorithm_button()
        self.create_calculate_fairness_definitions_button()
        self.images = GoBackButtonImage()
        self.go_back_button = self.create_go_back_button()

        self.window.mainloop()

    def configure_window(self):
        self.window.title("Evaluador de fairness")
        self.window.iconbitmap("images/icon.ico")
        self.window.geometry("{}x{}".format(TOTAL_WIDTH, TOTAL_HEIGHT))

    def configure_theme(self):
        style = ttk.Style(self.window)
        self.window.tk.eval("""
                   set base_theme_dir {}/awthemes-10.3.0/

                   package ifneeded awthemes 10.3.0 \
                       [list source [file join $base_theme_dir awthemes.tcl]]
                   package ifneeded colorutils 4.8 \
                       [list source [file join $base_theme_dir colorutils.tcl]]
                   package ifneeded awdark 7.11 \
                       [list source [file join $base_theme_dir awdark.tcl]]
                   package ifneeded awlight 7.6 \
                       [list source [file join $base_theme_dir awlight.tcl]]
                   """.format(os.getcwd().replace("\\", "/")))
        self.window.tk.call("package", "require", "awdark")
        self.window.tk.call("package", "require", "awlight")
        #style.theme_use("awlight")
        self.window.configure(bg=style.lookup("TFrame", "background"))
        return style

    def create_main_frame(self):
        # Create a frame to put the VerticalScrolledFrame inside
        holder_frame = tk.Frame(self.window)
        holder_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        # Create the VerticalScrolledFrame
        vs_frame = VerticalScrolledFrame(holder_frame)
        vs_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=tk.TRUE)
        return vs_frame.interior

    def create_custom_dialog(self):
        return CustomDialog(self.window, self.style)

    def create_add_decision_algorithm_button(self):
        button = ttk.Button(self.buttons_frame, text="Añadir clasificador/algoritmo de decisión",
                            command=self.add_decision_algorithm_button)
        button.pack(side=tk.LEFT)

    def add_decision_algorithm_button(self):
        self.go_back_button.pack(anchor=tk.NW)
        self.buttons_frame.pack_forget()
        self.current_screen = DecisionAlgorithmEditor(self.main_frame, self.dialog)

    def create_calculate_fairness_definitions_button(self):
        button = ttk.Button(self.buttons_frame, text="Calcular definiciones de fairness",
                            command=self.calculate_fairness_definitions)
        button.pack(side=tk.RIGHT)

    def calculate_fairness_definitions(self):
        self.go_back_button.pack(anchor=tk.NW)
        self.buttons_frame.pack_forget()
        self.current_screen = FairnessDefinitionsCalculator(TOTAL_WIDTH, self.dialog, self.main_frame)

    def create_go_back_button(self):
        button = tk.Button(self.main_frame, image=self.images.go_back, command=self.go_back,
                           highlightthickness=0, bd=0)
        return button

    def go_back(self):
        self.go_back_button.pack_forget()
        self.buttons_frame.pack()
        self.current_screen.destroy()
        self.current_screen = None
