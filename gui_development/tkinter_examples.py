"""
GUI Development with Tkinter

This module demonstrates comprehensive GUI development using Python's
built-in tkinter library, covering basic widgets, layouts, and advanced features.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser
import tkinter.scrolledtext as scrolledtext
from typing import Optional, Any, Callable
import json
import os
from datetime import datetime
import threading
import time


class BasicWidgetsDemo(tk.Tk):
    """Demonstrate basic tkinter widgets."""

    def __init__(self):
        super().__init__()
        self.title("Basic Widgets Demo")
        self.geometry("600x500")

        self.create_widgets()

    def create_widgets(self):
        """Create and layout basic widgets."""
        # Label
        ttk.Label(self, text="Basic Widgets Demonstration", font=("Arial", 16, "bold")).pack(pady=10)

        # Frame for organization
        main_frame = ttk.Frame(self)
        main_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # Entry and Label
        ttk.Label(main_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(main_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=(10, 0), pady=5)

        # Text widget
        ttk.Label(main_frame, text="Description:").grid(row=1, column=0, sticky=tk.NW, pady=5)
        self.text_widget = tk.Text(main_frame, height=4, width=30, wrap=tk.WORD)
        self.text_widget.grid(row=1, column=1, padx=(10, 0), pady=5)

        # Combobox
        ttk.Label(main_frame, text="Category:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.category_combo = ttk.Combobox(main_frame, values=["Option 1", "Option 2", "Option 3"], state="readonly")
        self.category_combo.grid(row=2, column=1, padx=(10, 0), pady=5)
        self.category_combo.set("Option 1")

        # Checkbuttons
        ttk.Label(main_frame, text="Options:").grid(row=3, column=0, sticky=tk.NW, pady=5)
        options_frame = ttk.Frame(main_frame)
        options_frame.grid(row=3, column=1, padx=(10, 0), pady=5, sticky=tk.W)

        self.option1_var = tk.BooleanVar()
        self.option2_var = tk.BooleanVar()
        self.option3_var = tk.BooleanVar()

        ttk.Checkbutton(options_frame, text="Option A", variable=self.option1_var).pack(anchor=tk.W)
        ttk.Checkbutton(options_frame, text="Option B", variable=self.option2_var).pack(anchor=tk.W)
        ttk.Checkbutton(options_frame, text="Option C", variable=self.option3_var).pack(anchor=tk.W)

        # Radiobuttons
        ttk.Label(main_frame, text="Priority:").grid(row=4, column=0, sticky=tk.W, pady=5)
        priority_frame = ttk.Frame(main_frame)
        priority_frame.grid(row=4, column=1, padx=(10, 0), pady=5, sticky=tk.W)

        self.priority_var = tk.StringVar(value="medium")
        ttk.Radiobutton(priority_frame, text="Low", variable=self.priority_var, value="low").pack(anchor=tk.W)
        ttk.Radiobutton(priority_frame, text="Medium", variable=self.priority_var, value="medium").pack(anchor=tk.W)
        ttk.Radiobutton(priority_frame, text="High", variable=self.priority_var, value="high").pack(anchor=tk.W)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Submit", command=self.submit_form).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_form).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exit", command=self.quit).pack(side=tk.LEFT, padx=5)

        # Status label
        self.status_label = ttk.Label(main_frame, text="", foreground="blue")
        self.status_label.grid(row=6, column=0, columnspan=2, pady=10)

    def submit_form(self):
        """Handle form submission."""
        name = self.name_entry.get().strip()
        description = self.text_widget.get("1.0", tk.END).strip()
        category = self.category_combo.get()

        if not name:
            messagebox.showerror("Error", "Name is required!")
            return

        # Collect options
        options = []
        if self.option1_var.get(): options.append("A")
        if self.option2_var.get(): options.append("B")
        if self.option3_var.get(): options.append("C")

        priority = self.priority_var.get()

        result = f"Name: {name}\nDescription: {description}\nCategory: {category}\nOptions: {', '.join(options)}\nPriority: {priority}"
        self.status_label.config(text="Form submitted successfully!")
        messagebox.showinfo("Form Data", result)

    def clear_form(self):
        """Clear all form fields."""
        self.name_entry.delete(0, tk.END)
        self.text_widget.delete("1.0", tk.END)
        self.category_combo.set("Option 1")
        self.option1_var.set(False)
        self.option2_var.set(False)
        self.option3_var.set(False)
        self.priority_var.set("medium")
        self.status_label.config(text="Form cleared")


class AdvancedWidgetsDemo(tk.Tk):
    """Demonstrate advanced tkinter widgets and features."""

    def __init__(self):
        super().__init__()
        self.title("Advanced Widgets Demo")
        self.geometry("800x600")

        self.create_widgets()
        self.create_menu()

    def create_menu(self):
        """Create application menu."""
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit, accelerator="Ctrl+Q")

        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Cut", command=self.cut_text, accelerator="Ctrl+X")
        edit_menu.add_command(label="Copy", command=self.copy_text, accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", command=self.paste_text, accelerator="Ctrl+V")

        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_checkbutton(label="Show Toolbar", command=self.toggle_toolbar)
        view_menu.add_checkbutton(label="Show Status Bar", command=self.toggle_statusbar)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

        # Bind keyboard shortcuts
        self.bind('<Control-n>', lambda e: self.new_file())
        self.bind('<Control-o>', lambda e: self.open_file())
        self.bind('<Control-s>', lambda e: self.save_file())
        self.bind('<Control-q>', lambda e: self.quit())

    def create_widgets(self):
        """Create advanced widgets."""
        # Toolbar
        self.toolbar = ttk.Frame(self)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        ttk.Button(self.toolbar, text="New", command=self.new_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.toolbar, text="Open", command=self.open_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.toolbar, text="Save", command=self.save_file).pack(side=tk.LEFT, padx=2)
        ttk.Separator(self.toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        ttk.Button(self.toolbar, text="Color", command=self.choose_color).pack(side=tk.LEFT, padx=2)

        # Main content area with paned window
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)

        # Left panel - Treeview
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=1)

        ttk.Label(left_frame, text="File Explorer", font=("Arial", 12, "bold")).pack(pady=5)

        # Treeview for file structure
        self.tree = ttk.Treeview(left_frame)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Add some sample data
        root_node = self.tree.insert("", "end", text="Project Root", open=True)
        self.tree.insert(root_node, "end", text="src")
        self.tree.insert(root_node, "end", text="tests")
        docs_node = self.tree.insert(root_node, "end", text="docs", open=True)
        self.tree.insert(docs_node, "end", text="README.md")
        self.tree.insert(docs_node, "end", text="API.md")

        # Right panel - Notebook with tabs
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=3)

        notebook = ttk.Notebook(right_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Text Editor Tab
        editor_frame = ttk.Frame(notebook)
        notebook.add(editor_frame, text="Editor")

        # Text editor with line numbers (simplified)
        editor_toolbar = ttk.Frame(editor_frame)
        editor_toolbar.pack(fill=tk.X)

        ttk.Button(editor_toolbar, text="Bold").pack(side=tk.LEFT, padx=2)
        ttk.Button(editor_toolbar, text="Italic").pack(side=tk.LEFT, padx=2)
        ttk.Button(editor_toolbar, text="Underline").pack(side=tk.LEFT, padx=2)

        self.text_editor = scrolledtext.ScrolledText(editor_frame, wrap=tk.WORD, font=("Consolas", 10))
        self.text_editor.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.text_editor.insert(tk.END, "Welcome to the text editor!\n\nThis is a scrolled text widget with syntax highlighting capabilities.")

        # Progress Tab
        progress_frame = ttk.Frame(notebook)
        notebook.add(progress_frame, text="Progress")

        ttk.Label(progress_frame, text="Progress Demonstration", font=("Arial", 12, "bold")).pack(pady=10)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, padx=20, pady=10)

        progress_controls = ttk.Frame(progress_frame)
        progress_controls.pack(pady=10)

        ttk.Button(progress_controls, text="Start", command=self.start_progress).pack(side=tk.LEFT, padx=5)
        ttk.Button(progress_controls, text="Stop", command=self.stop_progress).pack(side=tk.LEFT, padx=5)
        ttk.Button(progress_controls, text="Reset", command=self.reset_progress).pack(side=tk.LEFT, padx=5)

        # Canvas Tab
        canvas_frame = ttk.Frame(notebook)
        notebook.add(canvas_frame, text="Canvas")

        ttk.Label(canvas_frame, text="Interactive Canvas", font=("Arial", 12, "bold")).pack(pady=5)

        self.canvas = tk.Canvas(canvas_frame, bg='white', width=400, height=300)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Draw some shapes
        self.canvas.create_rectangle(50, 50, 150, 100, fill='lightblue', outline='blue')
        self.canvas.create_oval(200, 50, 300, 100, fill='lightgreen', outline='green')
        self.canvas.create_line(50, 150, 300, 150, fill='red', width=3)
        self.canvas.create_text(175, 200, text="Click to draw!", font=("Arial", 14))

        # Bind canvas events
        self.canvas.bind('<Button-1>', self.canvas_click)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def new_file(self):
        """Create new file."""
        self.text_editor.delete("1.0", tk.END)
        self.status_var.set("New file created")

    def open_file(self):
        """Open file dialog."""
        filename = filedialog.askopenfilename(
            title="Open File",
            filetypes=[("Text files", "*.txt"), ("Python files", "*.py"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r') as file:
                    content = file.read()
                    self.text_editor.delete("1.0", tk.END)
                    self.text_editor.insert(tk.END, content)
                self.status_var.set(f"Opened: {os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {e}")

    def save_file(self):
        """Save file dialog."""
        filename = filedialog.asksaveasfilename(
            title="Save File",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("Python files", "*.py"), ("All files", "*.*")]
        )
        if filename:
            try:
                content = self.text_editor.get("1.0", tk.END)
                with open(filename, 'w') as file:
                    file.write(content)
                self.status_var.set(f"Saved: {os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")

    def cut_text(self):
        """Cut selected text."""
        try:
            selected_text = self.text_editor.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.text_editor.delete(tk.SEL_FIRST, tk.SEL_LAST)
            self.clipboard_clear()
            self.clipboard_append(selected_text)
        except tk.TclError:
            pass  # No selection

    def copy_text(self):
        """Copy selected text."""
        try:
            selected_text = self.text_editor.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.clipboard_clear()
            self.clipboard_append(selected_text)
        except tk.TclError:
            pass  # No selection

    def paste_text(self):
        """Paste text from clipboard."""
        try:
            text = self.clipboard_get()
            self.text_editor.insert(tk.INSERT, text)
        except tk.TclError:
            pass  # No clipboard content

    def choose_color(self):
        """Choose color for text."""
        color = colorchooser.askcolor(title="Choose color")
        if color[1]:
            self.text_editor.config(fg=color[1])

    def toggle_toolbar(self):
        """Toggle toolbar visibility."""
        if self.toolbar.winfo_ismapped():
            self.toolbar.pack_forget()
        else:
            self.toolbar.pack(side=tk.TOP, fill=tk.X)

    def toggle_statusbar(self):
        """Toggle status bar visibility."""
        if self.status_bar.winfo_ismapped():
            self.status_bar.pack_forget()
        else:
            self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def show_about(self):
        """Show about dialog."""
        messagebox.showinfo("About", "Advanced Tkinter Demo\nVersion 1.0\nBuilt with Python and Tkinter")

    def start_progress(self):
        """Start progress bar animation."""
        self.progress_running = True
        self.progress_var.set(0)
        threading.Thread(target=self.run_progress, daemon=True).start()

    def stop_progress(self):
        """Stop progress bar animation."""
        self.progress_running = False

    def reset_progress(self):
        """Reset progress bar."""
        self.progress_running = False
        self.progress_var.set(0)

    def run_progress(self):
        """Run progress bar animation in background thread."""
        for i in range(101):
            if not getattr(self, 'progress_running', True):
                break
            self.progress_var.set(i)
            time.sleep(0.05)
        self.progress_running = False

    def canvas_click(self, event):
        """Handle canvas click events."""
        x, y = event.x, event.y
        # Draw a small circle where clicked
        self.canvas.create_oval(x-5, y-5, x+5, y+5, fill='red', outline='red')


class CalculatorApp(tk.Tk):
    """Simple calculator application."""

    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.geometry("300x400")
        self.resizable(False, False)

        self.expression = ""
        self.create_widgets()

    def create_widgets(self):
        """Create calculator interface."""
        # Display
        self.display = ttk.Entry(self, font=("Arial", 20), justify="right")
        self.display.pack(fill=tk.X, padx=10, pady=10)
        self.display.bind("<Key>", lambda e: "break")  # Disable keyboard input

        # Button frame
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Button layout
        buttons = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', '.', '=', '+']
        ]

        for row_idx, row in enumerate(buttons):
            for col_idx, button_text in enumerate(row):
                if button_text == '=':
                    btn = ttk.Button(button_frame, text=button_text,
                                   command=self.calculate)
                elif button_text in '+-*/':
                    btn = ttk.Button(button_frame, text=button_text,
                                   command=lambda x=button_text: self.append_operator(x))
                else:
                    btn = ttk.Button(button_frame, text=button_text,
                                   command=lambda x=button_text: self.append_digit(x))
                btn.grid(row=row_idx, column=col_idx, sticky="nsew", padx=2, pady=2)

        # Clear button
        ttk.Button(button_frame, text='C', command=self.clear).grid(
            row=4, column=0, columnspan=2, sticky="nsew", padx=2, pady=2)
        ttk.Button(button_frame, text='CE', command=self.clear_entry).grid(
            row=4, column=2, columnspan=2, sticky="nsew", padx=2, pady=2)

        # Configure grid weights
        for i in range(5):
            button_frame.rowconfigure(i, weight=1)
        for i in range(4):
            button_frame.columnconfigure(i, weight=1)

    def append_digit(self, digit):
        """Append digit to expression."""
        self.expression += digit
        self.update_display()

    def append_operator(self, operator):
        """Append operator to expression."""
        if self.expression and self.expression[-1] not in '+-*/':
            self.expression += operator
            self.update_display()

    def calculate(self):
        """Calculate the expression."""
        try:
            result = eval(self.expression)
            self.expression = str(result)
            self.update_display()
        except:
            self.display.delete(0, tk.END)
            self.display.insert(0, "Error")
            self.expression = ""

    def clear(self):
        """Clear everything."""
        self.expression = ""
        self.update_display()

    def clear_entry(self):
        """Clear current entry."""
        self.expression = ""
        self.update_display()

    def update_display(self):
        """Update display with current expression."""
        self.display.delete(0, tk.END)
        self.display.insert(0, self.expression)


def main():
    """Run GUI demonstrations."""
    print("Tkinter GUI Development Examples")
    print("=" * 40)

    # Create demo windows
    apps = []

    # Basic widgets demo
    print("Launching Basic Widgets Demo...")
    basic_app = BasicWidgetsDemo()
    apps.append(basic_app)

    # Advanced widgets demo
    print("Launching Advanced Widgets Demo...")
    advanced_app = AdvancedWidgetsDemo()
    apps.append(advanced_app)

    # Calculator app
    print("Launching Calculator App...")
    calc_app = CalculatorApp()
    apps.append(calc_app)

    print("\nAll GUI applications launched!")
    print("Close the windows to exit the demos.")

    # Start the main event loop for all apps
    # Note: In a real application, you'd typically run one app at a time
    for app in apps:
        app.mainloop()


if __name__ == "__main__":
    main()