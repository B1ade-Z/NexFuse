"""
Tool: Nexfuse Framework
Author: Blade-Z
Github: https://www.github.com/B1ade-Z
About: An anti-forensics tool inspired by NSA's Marble Framework to change the comment to different language to evade forensic.


*> WARNING: This tool is not made for illegal purposes I just tried to make a tool inspired from NSA, I will not be responsible for any of your activity. 
*> This tool only translatest comments. 
*> Some features are yet to come.

[!] Supported prorgamming language: Python, C++, C, Rust, Golang, Shell script

"""
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import customtkinter as ctk
import os
import re
from translator import translate_comments
from deep_translator import GoogleTranslator

ctk.set_appearance_mode("Dark")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("NeXFusE")
        self.iconbitmap("assets/icon.ico")
        self.geometry("1100x580")
        self.configure(bg=self.cget("bg"))

        # Create sidebar frame
        self.create_sidebar()

        # Create notebook widget
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=1, sticky="nsew")
        self.notebook.enable_traversal()

        # Configure notebook style
        self.configure_notebook_style()

        # Configure grid weights
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # Dictionary to store the tab widget and the corresponding file path
        self.tabs = {}

        # it for binding shortcuts
        self.bind_shortcuts()

        self.mainloop()

    def create_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=40, corner_radius=0, fg_color="#28282B")
        self.sidebar_frame.configure(border_width=1, border_color="#808080")
        self.sidebar_frame.grid(row=0, rowspan=2, column=0, sticky="ns")
        self.sidebar_frame.grid_rowconfigure(0, weight=1)
        
        self.open_file_button = ctk.CTkButton(self.sidebar_frame, text="Open File", command=self.open_file_event)
        self.open_file_button.pack(padx=20, pady=10)
        self.open_file_button.configure(fg_color="#28282B", hover_color="#1B1B1B", border_color="#808080", border_width=2)

        self.save_file_button = ctk.CTkButton(self.sidebar_frame, text="Save File As", command=self.save_file_event)
        self.save_file_button.pack(padx=20, pady=10)
        self.save_file_button.configure(fg_color="#28282B", hover_color="#1B1B1B", border_color="#808080", border_width=2, state="disabled")

        self.create_textbox()
        self.create_checkboxes()
        self.create_action_buttons()

    def create_textbox(self):
        self.textbox = ctk.CTkTextbox(self.sidebar_frame, width=165, height=160, text_color="white")
        self.textbox.pack(padx=(2, 0), pady=(10, 0))
        self.textbox.insert("0.0", "Keyboard Shortcuts\n\nCtrl+S [Save File]\n\nCtrl+G [Save File As]\n\nCtrl+W [Close Tab]\n\nCtrl+Q [Quit]")
        self.textbox.configure(font=("Consolas", 12), state="disabled")

    def create_checkboxes(self):
        self.checkbox_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="#1B1B1B")
        self.checkbox_frame.pack(padx=10, pady=(10, 0))

        languages = ["Russian", "Chinese", "Arabic", "Urdu", "English"]
        self.checkboxes = []
        for lang in languages:
            checkbox = ctk.CTkCheckBox(master=self.checkbox_frame, width=140, text=lang, border_width=2, hover_color="#C0C0C0", fg_color="#343434", state="normal")
            checkbox.pack(pady=(10, 0), padx=10)
            self.checkboxes.append(checkbox)

    def create_action_buttons(self):
        self.obfuscate_button = ctk.CTkButton(self.sidebar_frame, text="Translate", command=self.obfuscate_event)
        self.obfuscate_button.pack(padx=20, pady=10)
        self.obfuscate_button.configure(state="disabled", fg_color="#28282B", text_color="white", hover_color="#1B1B1B", border_width=2, border_color="#808080", width=140)

    def configure_notebook_style(self):
        style = ttk.Style()
        style.theme_create("custom_theme", parent="alt", settings={
            "TNotebook": {
                "configure": {"background": "#1B1B1B", "tabmargins": [0, 0, 0, 0]},
                "tab": {"configure": {"padding": [10, 2], "background": "#2B2B2B", "foreground": "#CCCCCC"}},
                "tabarea": {"configure": {"background": "#2B2B2B"}},
            },
            "TNotebook.Tab": {
                "configure": {"padding": [10, 2], "background": "#1B1B1B", "foreground": "#CCCCCC", "font": ("Consolas", 12)},
                "map": {"background": [("selected", "#2B2B2B")], "foreground": [("selected", "#FFFFFF")]}
            }
        })
        style.theme_use("custom_theme")

    def bind_shortcuts(self):
        self.bind("<Control-s>", self.instant_save)
        self.bind("<Control-g>", self.save_file_event)
        self.bind("<Control-q>", self.quit_application)
        self.bind("<Control-w>", self.close_current_tab)

    def close_current_tab(self, event=None):
        tab_selected = self.notebook.select()
        tab_container = self.notebook.nametowidget(tab_selected)

        if tab_container in self.tabs:
            # Retrieve the text widget from the container frame
            text_widget = tab_container.winfo_children()[0]
            
            # Unbind the scrollbar from the text widget
            text_widget.config(yscrollcommand="")

            # Safely destroy the scrollbar
            if "scrollbar" in self.tabs[tab_container]:
                scrollbar = self.tabs[tab_container]["scrollbar"]
                if scrollbar.winfo_exists():
                    scrollbar.destroy()

            # Forget the tab
            self.notebook.forget(tab_selected)
            del self.tabs[tab_container]

            if len(self.notebook.tabs()) == 0:
                self.save_file_button.configure(state="disabled")
                self.obfuscate_button.configure(state="disabled")
                for checkbox in self.checkboxes:
                    checkbox.configure(state="disabled")
                
    def quit_application(self, event=None):
        self.destroy()

    def instant_save(self, event=None):
        selected_tab = self.notebook.select()
        tab_container = self.notebook.nametowidget(selected_tab)

        if tab_container in self.tabs:
            text_widget = tab_container.winfo_children()[0]
            self.save_file(text_widget)


    def open_file_event(self):
        file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.*"), ("Text Files", "*.txt")])
        if file_path:
            self.load_file(file_path)

    def load_file(self, file_path):
        file_name = os.path.basename(file_path)
        with open(file_path, "r", encoding='utf-8') as file:
            content = file.read()
            
            # Create a container frame for the tab
            container = tk.Frame(self.notebook, bg="#2b2b2b")
            
            # Create the text widget inside the container
            text_widget = tk.Text(container, wrap=tk.WORD, bg="#2b2b2b", font=("Consolas", 13), padx=16, pady=16)
            text_widget.config(borderwidth=1, highlightthickness=0, inactiveselectbackground=text_widget.cget("bg"))
            text_widget.configure(insertbackground="white")
            text_widget.insert(tk.END, content)
            
            # Create and configure scrollbar inside the container
            scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=text_widget.yview)
            text_widget.config(yscrollcommand=scrollbar.set)
            
            # Pack text widget and scrollbar in the container
            text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Add the container frame to the notebook
            self.notebook.add(container, text=file_name)
            
            self.save_file_button.configure(state=tk.NORMAL)
            self.obfuscate_button.configure(state=tk.NORMAL)
            for checkbox in self.checkboxes:
                checkbox.configure(state=tk.NORMAL)
            
            text_widget.tag_configure("custom_tag", foreground="white", font=("Consolas", 13))
            text_widget.tag_add("custom_tag", "1.0", tk.END)
            
            self.tabs[container] = {
                "file_path": file_path,
                "content": content,
                "saved": True,
                "initializing": True,
                "scrollbar": scrollbar  # Store the scrollbar instance
            }

        text_widget.after(100, lambda: self.set_initializing_flag(container))


    def set_initializing_flag(self, text_widget):
        if text_widget in self.tabs:
            self.tabs[text_widget]["initializing"] = False
    
    def save_file_event(self, event=None):
        selected_tab = self.notebook.select()
        tab_container = self.notebook.nametowidget(selected_tab)

        if tab_container in self.tabs:
            text_widget = tab_container.winfo_children()[0]  # Retrieve the text widget from the container
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Files", "*.txt")])
            if file_path:
                self.tabs[tab_container]["file_path"] = file_path
                self.save_file(text_widget)


    def save_file(self, text_widget):
        tab_container = text_widget.master  # Get the container frame from the text widget
        file_path = self.tabs[tab_container]["file_path"]
        content = text_widget.get("1.0", tk.END)

        with open(file_path, "w", encoding='utf-8') as file:
            file.write(content)

        self.tabs[tab_container]["saved"] = True

    # At the top of your main script, import the Cython module

    # Update your obfuscate_event method
    def obfuscate_event(self):
        selected_tab = self.notebook.select()
        tab_container = self.notebook.nametowidget(selected_tab)

        if tab_container in self.tabs:
            # Retrieve the text widget from the container frame
            text_widget = tab_container.winfo_children()[0]
            content = text_widget.get("1.0", tk.END)
            file_path = self.tabs[tab_container]["file_path"]
            language = self.detect_language(file_path)

            if language == "Unknown" or not language:
                messagebox.showinfo("Translation Error",
                                    "Error: Unable to determine language or target language not selected.\n\nOnly Python, C++, C, Rust, Golang and Shell script is supported")
                return

            target_language = self.get_target_language()
            if not target_language:
                messagebox.showinfo("Translation Error", "Error: Target language not selected.")
                return

            # Use the Cython function for translation
            translated_content = translate_comments(content, language, target_language)
            text_widget.delete("1.0", tk.END)
            text_widget.insert("1.0", translated_content)
            text_widget.tag_add("custom_tag", "1.0", tk.END)  # Apply the custom text tag

            # Show success message
            messagebox.showinfo("Translation Complete",
                                "Alert: Remember to match the modified code with existing code to ensure any unwanted error.\n\nFile translation completed successfully!")

    def detect_language(self, file_path):
        extension = os.path.splitext(file_path)[1].lower()
        if extension == ".py":
            return "Python"
        elif extension == ".cpp" or extension == ".cxx" or extension == ".cc":
            return "C++"
        elif extension == ".c":
            return "C"
        elif extension == ".rs":
            return "Rust"
        elif extension == ".go":
            return "Golang"
        elif extension == ".sh":
            return "Shell"
        return None

    def translate_comments(self, content, language):
        patterns = {
            "Python": r"(^\s*#.*?$)|(^\s*\"\"\"[\s\S]*?\"\"\"|\'\'\'[\s\S]*?\')",
            "C++": r"(//.*?$)|(/\*[\s\S]*?\*/)",
            "C": r"(//.*?$)|(/\*[\s\S]*?\*/)",
            "Rust": r"(//.*?$)|(/\*[\s\S]*?\*/)",
            "Golang": r"(//.*?$)|(/\*[\s\S]*?\*/)",
            "Shell": r"(^\s*#.*?$)"
        }

        pattern = patterns.get(language)
        if not pattern:
            return content

        def translate_match(match):
            comment = match.group(0)
            target_language = self.get_target_language()
            if not target_language:
                return comment

            try:
                translated_comment = GoogleTranslator(source='auto', target=target_language).translate(comment)
                return translated_comment
            except Exception as e:
                return comment

        translated_content = re.sub(pattern, translate_match, content, flags=re.MULTILINE)
        return translated_content

    def get_target_language(self):
        for checkbox in self.checkboxes:
            if checkbox.get():
                lang = checkbox.cget("text")
                lang_code = {
                    "Russian": "ru",
                    "Chinese": "zh-CN",
                    "Arabic": "ar",
                    "Urdu": "ur",
                    "English": "en"
                }
                return lang_code.get(lang)
        return None

if __name__ == "__main__":
    App()
