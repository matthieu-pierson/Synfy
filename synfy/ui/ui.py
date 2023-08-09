import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import pystray
from PIL import Image

class UI:
    def __init__(self):
        self.root = None
        self.icon = None
        self.create_notification_icon()

    def create_notification_icon(self):
        icon_image = Image.open("../resources/music.png")
        menu_items = [
            pystray.MenuItem("Show UI", self.toggle_ui),
            pystray.MenuItem("Quit", self.quit),
        ]
        self.icon = pystray.Icon("name", icon_image, "Title", menu_items)
        self.icon.run()

    def toggle_ui(self):
        if self.root and self.root.winfo_exists():
            self.root.deiconify()
            self.root.focus_force()  # Bring the window to the front and give it focus
        else:
            self.show_ui()

    def show_ui(self):
        if not self.root:
            self.root = ttk.Window(themename="darkly")
            self.root.title("UI Window")
            self.create_ui_components()
            self.root.protocol("WM_DELETE_WINDOW", self.close_ui)  # Handle window close event
        else:
            self.root.deiconify()  # Show the existing window if it exists and is hidden
        self.root.mainloop()

    def create_ui_components(self):
        label = tk.Label(self.root, text="Hello, UI!")
        label.pack()

        styles = [PRIMARY, SECONDARY, SUCCESS, INFO, WARNING, DANGER, LIGHT, DARK]
        for style in styles:
            button = ttk.Button(self.root, text=style.lower(), bootstyle=style)
            button.pack(side=tk.LEFT, padx=5, pady=5)

    def close_ui(self):
        if self.root:
            self.root.withdraw()  # Hide the window instead of destroying it
            # No need to set self.root to None here

    def quit(self):
        self.close_ui()
        if self.icon:
            self.icon.stop()
        if self.root:
            self.root.destroy()  # Cleanly close the Tkinter window

if __name__ == "__main__":
    ui = UI()
