import os
import tkinter as tk
from tkinter import ttk

from user_interface.dialogs import CustomDialog
from user_interface.scrolled_frame import VerticalScrolledFrame


class CustomWindow:

    def __init__(self, width, height):
        self.window = tk.Tk()
        self.configure_window(width, height)
        self.style = self.configure_theme()
        self.dialog = self.create_custom_dialog()
        self.main_frame = self.create_main_frame()

    def configure_window(self, width, height):
        self.window.title("Evaluador de fairness")
        self.window.iconbitmap("images/icon.ico")
        self.window.geometry("{}x{}".format(width, height))

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
        style.theme_use("awlight")
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
