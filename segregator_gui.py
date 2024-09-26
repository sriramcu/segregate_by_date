import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import os
import shutil
from segregator import segregate_entire_folder

def run_segregation(input_dir, output_dir, log_output):
    try:
        segregate_entire_folder(input_dir, output_dir)
        log_output.config(text=f"Segregation completed successfully!")
    except Exception as e:
        log_output.config(text=f"Error: {str(e)}")


def select_input_folder(entry):
    folder = filedialog.askdirectory()
    if folder:
        entry.delete(0, tk.END)
        entry.insert(0, folder)


def select_output_folder(entry):
    folder = filedialog.askdirectory()
    if folder:
        entry.delete(0, tk.END)
        entry.insert(0, folder)


def create_gui():
    root = tk.Tk()
    root.title("File Segregator")

    # Input folder selection
    tk.Label(root, text="Input Directory:").grid(row=0, column=0, padx=10, pady=5)
    input_entry = tk.Entry(root, width=50)
    input_entry.grid(row=0, column=1, padx=10, pady=5)
    tk.Button(root, text="Browse", command=lambda: select_input_folder(input_entry)).grid(row=0, column=2, padx=10,
                                                                                          pady=5)

    # Output folder selection
    tk.Label(root, text="Output Directory:").grid(row=1, column=0, padx=10, pady=5)
    output_entry = tk.Entry(root, width=50)
    output_entry.grid(row=1, column=1, padx=10, pady=5)
    tk.Button(root, text="Browse", command=lambda: select_output_folder(output_entry)).grid(row=1, column=2, padx=10,
                                                                                            pady=5)

    # Log output
    log_output = tk.Label(root, text="", wraplength=400, justify="left")
    log_output.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    # Run button
    tk.Button(root, text="Run Segregation",
              command=lambda: run_segregation(input_entry.get(), output_entry.get(), log_output)).grid(row=3, column=1,
                                                                                                       pady=10)

    root.mainloop()


if __name__ == "__main__":
    create_gui()