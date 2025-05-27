import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from pathlib import Path

class SlideshowApp:
    def __init__(self, root, assets_dir: Path, width=900, height=600):
        self.root = root
        self.assets_dir = assets_dir
        self.width = width
        self.height = height
        self.index = 0

        # Load image file paths
        self.images = sorted([photo for photo in assets_dir.iterdir() if photo.is_file()])
        if not self.images:
            messagebox.showerror("Error", f"No images found in {assets_dir}")
            root.destroy()
            return

        # Configure root window
        root.title("Image Slideshow")
        root.geometry(f"{width}x{height}")
        root.minsize(width, height)
        root.resizable(False, False)

        # Build UI
        self.container = tk.Frame(root)
        self.canvas = tk.Canvas(self.container)
        self.buttons_frame = tk.Frame(self.container)
        self.btn_prev = tk.Button(self.buttons_frame, text="<", command=self.previous_image)
        self.btn_next = tk.Button(self.buttons_frame, text=">", command=self.next_image)

        # Layout
        self.container.pack(expand=True, fill="both")
        self.canvas.pack(side="top", expand=True, fill="both")
        self.buttons_frame.pack(side="bottom", pady=10)
        self.btn_prev.grid(row=0, column=0, padx=5, pady=5)
        self.btn_next.grid(row=0, column=1, padx=5, pady=5)

        # Initialize first image
        self.load_current_image()
        self.draw_image()

    def load_current_image(self):
        """Load the PIL image for self.index into self.current_image."""
        path = self.images[self.index]
        self.current_image = Image.open(path)

    def draw_image(self):
        """Resize (if needed) and draw the current image on the canvas."""
        image = self.current_image.copy()
        width, height = image.size

        # Resize if larger than canvas
        if width > self.width or height > self.height:
            image.thumbnail((self.width, self.height))

        # Center calculation
        width_calc, height_calc = image.size
        x = (self.width - width_calc) // 2
        y = (self.height - height_calc) // 2

        # Clear and draw
        self.canvas.delete("all")
        self.tk_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(x, y, anchor="nw", image=self.tk_image)

    def next_image(self):
        """Advance the index and update the display."""
        self.index = (self.index + 1) % len(self.images)
        self.load_current_image()
        self.draw_image()

    def previous_image(self):
        """Go back one image and update the display."""
        self.index = (self.index - 1) % len(self.images)
        self.load_current_image()
        self.draw_image()


if __name__ == "__main__":
    root = tk.Tk()
    assets_path = Path(__file__).parent / "assets"
    app = SlideshowApp(root, assets_path)
    root.mainloop()
