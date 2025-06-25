import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import win32com.client

INDEX_PATH = r'' # Insert your file path cache here, see Cache VSIndex in the PowerShell repository for more info.
current_suggestions = []

def load_index():
    index = {}
    if not os.path.exists(INDEX_PATH):
        messagebox.showerror("Error", f"Index file not found:\n{INDEX_PATH}")
        return index
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            if '|' in line:
                name, dirs = line.strip().split('|', 1)
                full_name = f"{name}.cs"
                paths = [
                    os.path.join(d.strip(), full_name)
                    for d in dirs.split(';') if os.path.isdir(d.strip())
                ]
                index[full_name] = paths
    return index

def open_files_in_vs(paths):
    try:
        dte = win32com.client.GetActiveObject("VisualStudio.DTE.17.0")
        for path in paths:
            dte.ItemOperations.OpenFile(path)
    except Exception:
        existing = [p for p in paths if os.path.exists(p)]
        if existing:
            subprocess.run(["devenv.exe", "/Edit"] + existing)

def on_open(event=None):
    selected = entry_var.get()
    if not selected or selected not in file_map:
        messagebox.showwarning("Error", f"'{selected}' is not a valid selection.")
        status_var.set(f"Error: '{selected}' not found")
        return "break"
    paths = file_map[selected]
    valid = [p for p in paths if os.path.exists(p)]
    if not valid:
        messagebox.showerror("Not Found", f"No file found on disk for '{selected}'.")
        status_var.set(f"No file found for '{selected}'")
        return "break"
    open_files_in_vs(valid)
    status_var.set(f"Opened {selected}")
    hide_list()
    return "break"

def show_list(items):
    listbox.delete(0, tk.END)
    for item in items:
        listbox.insert(tk.END, item)
    list_frame.pack(padx=20, fill='both', pady=(0,5))

def hide_list():
    list_frame.pack_forget()

def on_click(event):
    global current_suggestions
    current_suggestions = sorted(file_map.keys())
    show_list(current_suggestions)

def on_keyrelease(event):
    global current_suggestions
    typed = entry_var.get().lower()
    all_names = sorted(file_map.keys())
    prefix = [n for n in all_names if n.lower().startswith(typed)]
    contains = [n for n in all_names if typed in n.lower() and not n.lower().startswith(typed)]
    current_suggestions = prefix + contains
    if current_suggestions:
        show_list(current_suggestions)
    else:
        hide_list()

def on_listbox_select(event):
    sel = event.widget.curselection()
    if sel:
        value = event.widget.get(sel[0])
        entry_var.set(value)
    hide_list()
    entry.icursor(tk.END)
    entry.focus_set()

def accept_autocomplete(event):
    if current_suggestions:
        suggestion = current_suggestions[0]
        entry_var.set(suggestion)
        entry.icursor(len(suggestion))
        entry.select_range(len(event.widget.get()), len(suggestion))
        hide_list()
    return "break"

def center_window(win, width=400, height=250):
    sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
    x, y = (sw - width)//2, (sh - height)//2
    win.geometry(f"{width}x{height}+{x}+{y}")

file_map = load_index()

root = tk.Tk()
root.title("Visual Studio File Opener UI")
center_window(root)
root.resizable(True, True)

tk.Label(root, text="Click or type to filter, then select a .cs file:")\
    .pack(pady=(15,5))

entry_var = tk.StringVar()
entry = tk.Entry(root, textvariable=entry_var)
entry.pack(padx=20, fill='x')
entry.bind('<Button-1>', on_click)
entry.bind('<KeyRelease>', on_keyrelease)
entry.bind('<Tab>', accept_autocomplete)
entry.bind('<Return>', on_open)

list_frame = tk.Frame(root)
scroll = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
listbox = tk.Listbox(list_frame, yscrollcommand=scroll.set, height=8)
scroll.config(command=listbox.yview)
scroll.pack(side=tk.RIGHT, fill=tk.Y)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
list_frame.pack_forget()
listbox.bind('<<ListboxSelect>>', on_listbox_select)

status_var = tk.StringVar()
status_label = tk.Label(root, textvariable=status_var, fg='green')
status_label.pack(fill='x', pady=(0,5), padx=20)

open_btn = tk.Button(root, text="Open in Visual Studio", command=lambda: on_open())
open_btn.pack(side=tk.BOTTOM, pady=15)

root.mainloop()
