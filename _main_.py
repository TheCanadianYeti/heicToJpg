from pathlib import Path
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()

class HeicConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HEIC to JPG Converter")
        self.root.geometry("520x360")
        self.root.resizable(False, False)

        self.input_files = []
        self.output_directory = None

        self.build_ui()

    def build_ui(self):
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        self.btn_select_files = ttk.Button(frame, text="Select HEIC Files", command=self.select_files)
        self.btn_select_files.pack(fill=tk.X, pady=4)

        self.btn_select_dir = ttk.Button(frame, text="Or Select Folder with HEIC", command=self.select_directory)
        self.btn_select_dir.pack(fill=tk.X, pady=4)

        self.lbl_selected = ttk.Label(frame, text="No files selected", wraplength=480)
        self.lbl_selected.pack(pady=8)

        self.btn_output_dir = ttk.Button(frame, text="Select Output Folder", command=self.select_output)
        self.btn_output_dir.pack(fill=tk.X, pady=4)

        self.lbl_output = ttk.Label(frame, text="Output: Default (same folder as source)", wraplength=480)
        self.lbl_output.pack(pady=8)

        self.progress = ttk.Progressbar(frame, orient=tk.HORIZONTAL, mode="determinate")
        self.progress.pack(fill=tk.X, pady=10)

        self.btn_run = ttk.Button(frame, text="Convert to JPG", command=self.start_conversion)
        self.btn_run.pack(fill=tk.X, pady=8)

        self.lbl_status = ttk.Label(frame, text="Ready")
        self.lbl_status.pack()

    def select_files(self):
        paths = filedialog.askopenfilenames(
            title="Select HEIC Images",
            filetypes=[("HEIC Images", "*.heic *.HEIC")]
        )
        if paths:
            self.input_files = [Path(p) for p in paths]
            self.lbl_selected.config(text=f"Selected {len(self.input_files)} file(s)")

    def select_directory(self):
        dir_path = filedialog.askdirectory(title="Select Folder Containing HEIC Files")
        if dir_path:
            folder = Path(dir_path)
            found = list(folder.glob("*.heic")) + list(folder.glob("*.HEIC"))
            if not found:
                messagebox.showwarning("Empty", "No HEIC files found in selected directory.")
                return
            self.input_files = found
            self.lbl_selected.config(text=f"Selected {len(self.input_files)} files from {folder.name}")

    def select_output(self):
        target = filedialog.askdirectory(title="Select Destination Folder")
        if target:
            self.output_directory = Path(target)
            self.lbl_output.config(text=f"Output: {self.output_directory}")

    def start_conversion(self):
        if not self.input_files:
            messagebox.showwarning("Warning", "Select input files or a folder first.")
            return

        self.btn_run.config(state=tk.DISABLED)
        self.btn_select_files.config(state=tk.DISABLED)
        self.btn_select_dir.config(state=tk.DISABLED)
        self.btn_output_dir.config(state=tk.DISABLED)

        threading.Thread(target=self.run_batch, daemon=True).start()

    def run_batch(self):
        total = len(self.input_files)
        self.progress["maximum"] = total
        self.progress["value"] = 0

        for idx, file_path in enumerate(self.input_files, start=1):
            out_dir = self.output_directory if self.output_directory else file_path.parent
            out_dir.mkdir(parents=True, exist_ok=True)
            dest = out_dir / f"{file_path.stem}.jpg"

            try:
                with Image.open(file_path) as image:
                    exif_data = image.info.get("exif")
                    rgb_image = image.convert("RGB")
                    save_kwargs = {"quality": 95}
                    if exif_data:
                        save_kwargs["exif"] = exif_data
                    rgb_image.save(dest, "JPEG", **save_kwargs)
            except Exception as e:
                print(f"Error converting {file_path.name}: {e}")

            self.progress["value"] = idx
            self.lbl_status.config(text=f"Converting {idx}/{total}: {file_path.name}")
            self.root.update_idletasks()

        self.lbl_status.config(text="Complete")
        self.btn_run.config(state=tk.NORMAL)
        self.btn_select_files.config(state=tk.NORMAL)
        self.btn_select_dir.config(state=tk.NORMAL)
        self.btn_output_dir.config(state=tk.NORMAL)
        messagebox.showinfo("Done", f"Successfully converted {total} images.")

if __name__ == "__main__":
    app_root = tk.Tk()
    app = HeicConverterApp(app_root)
    app_root.mainloop()