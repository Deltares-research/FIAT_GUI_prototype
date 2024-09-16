"""util functions for FIAT GUI."""

from __future__ import annotations

import tkinter as tk
from tkinter import filedialog


def file_dialog(title: str, file_types, *, is_file: bool = True, multiple: bool = False) -> str | None:
    root = tk.Tk()
    # Force dialog to stay on top of all other open windows - this is the closest
    #  we can get to a browser popup.
    root.attributes("-topmost", True)
    # Remove window and task bar
    root.withdraw()
    if is_file and multiple:
        path = filedialog.askopenfilenames(title=title, filetypes=file_types)
    elif is_file:
        path = filedialog.askopenfilename(title=title, filetypes=file_types)
    else:
        path = filedialog.askdirectory(title=title)
    root.destroy()
    return path if path else None
