# -*- coding: utf-8 -*-

import os
import shutil
import csv
import logging
import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import pandas as pd
from requests.auth import HTTPBasicAuth
import json
from digikey import digikey_search
import threading
from tkinter import ttk
from json_table import show_json_table, show_categorized_tables
from gen_ai import genAi

# Configuration (self-contained; no external modules needed)
# Where files will be copied when you click "Submit"
TARGET_DIR = os.path.join(os.path.expanduser("~"), "WCCA_Uploads")
# Max allowed file size (bytes) for upload
MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB

SUPPORTED_TYPES = {
    "xml": [".xml"],
    "csv": [".csv"],
    "yaml": [".yml", ".yaml"],
}

# Utility functions
def is_supported_file(filepath: str, exts):
    """Check if the file extension matches one of the supported ones (case-insensitive)."""
    ext = os.path.splitext(filepath)[1]
    return ext.lower() in [e.lower() for e in exts]

def is_file_size_valid(filepath: str, max_size: int):
    """Check if the file size is within the maximum allowed size."""
    try:
        return os.path.getsize(filepath) <= max_size
    except OSError:
        return False

def copy_file_to_target(src: str, target_dir: str) -> str:
    """Copy the file to target_dir. If a file with the same name exists,
    append a numeric suffix to avoid overwriting."""
    os.makedirs(target_dir, exist_ok=True)
    base = os.path.basename(src)
    dest = os.path.join(target_dir, base)

    if not os.path.exists(dest):
        shutil.copy2(src, dest)
        return dest

    # If exists, create unique name: name(1).ext, name(2).ext, ...
    name, ext = os.path.splitext(base)
    i = 1
    while True:
        alt = os.path.join(target_dir, f"{name}({i}){ext}")
        if not os.path.exists(alt):
            shutil.copy2(src, alt)
            return alt
        i += 1

# Configure logging
logging.basicConfig(
    filename="uploader.log",
    level=logging.ERROR,
    format="%(asctime)s %(levelname)s:%(message)s"
)

# Tkinter Application
class FileUploaderApp(tk.Tk):
    def __init__(self, target_dir=TARGET_DIR, max_file_size=MAX_FILE_SIZE):
        super().__init__()
        self.title("WCCA Automation")
        self.geometry("1400x800")
        self.resizable(True,True)
        self.after(0, lambda: self.state('zoomed'))
        # Remove default Tk icon by setting a transparent icon
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "samplelogo.png")
            self._app_icon = tk.PhotoImage(file=icon_path)  # keep a reference!
            self.iconphoto(True, self._app_icon)
        except Exception:
            pass

        # Dark theme colors
        self.bg_color = "#24143a"
        self.card_color = "#2f1d4a"
        self.text_color = "#fff"
        self.button_color = "#7c5fff"
        self.button_fg = "#fff"
        self.note_fg = "#bcb4d5"
        self.preview_bg = "#39275c"
        self.preview_fg = "#fff"
        self.configure(bg=self.bg_color)
        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except Exception:
            pass
        # Colors and flat relief
        self.style.configure("Dark.Vertical.TScrollbar", troughcolor=self.preview_bg, background=self.preview_bg, bordercolor=self.preview_bg, arrowcolor=self.preview_bg, borderwidth=0, troughrelief="flat", relief="flat")
        self.style.configure("Dark.Horizontal.TScrollbar", troughcolor=self.preview_bg, background=self.preview_bg, bordercolor=self.preview_bg, arrowcolor=self.preview_bg, borderwidth=0, troughrelief="flat", relief="flat")
        self.style.map("Dark.Vertical.TScrollbar", background=[["active", self.button_color]], bordercolor=[["!disabled", self.preview_bg]])
        self.style.map("Dark.Horizontal.TScrollbar", background=[["active", self.button_color]], bordercolor=[["!disabled", self.preview_bg]])
        # Treeview dark theme for JSON table
        self.style.configure("Dark.Treeview", background=self.preview_bg, fieldbackground=self.preview_bg, foreground=self.preview_fg, borderwidth=0, rowheight=22)
        self.style.configure("Dark.Treeview.Heading", background=self.card_color, foreground=self.text_color, borderwidth=0)
        self.style.map("Dark.Treeview", background=[["selected", "#4b3780"]])
        self.style.map("Dark.Treeview.Heading", background=[["active", self.card_color]])
        # Notebook (tabs) compact style
        self.style.configure("Dark.TNotebook", background=self.preview_bg, borderwidth=0, tabmargins=0)
        self.style.configure("Dark.TNotebook.Tab", background=self.card_color, foreground=self.text_color, padding=[8,2], borderwidth=0)
        self.style.map("Dark.TNotebook.Tab", background=[["selected", self.card_color]])
        # Remove arrows and extra borders by redefining the layout to only show trough + thumb
        self.style.layout("Dark.Vertical.TScrollbar", [
            ("Vertical.Scrollbar.trough", {"children": [
                ("Vertical.Scrollbar.thumb", {"sticky": "nswe"})
            ], "sticky": "ns"})
        ])
        self.style.layout("Dark.Horizontal.TScrollbar", [
            ("Horizontal.Scrollbar.trough", {"children": [
                ("Horizontal.Scrollbar.thumb", {"sticky": "nswe"})
            ], "sticky": "we"})
        ])

        # State
        self.target_dir = target_dir
        self.max_file_size = max_file_size
        self.selected_files = {"xml": None, "csv": None, "yaml": None}
        self.entries = {}
        self.previews = {}
        self.preview_containers = {}
        self.pending_preview = {}
        self.part_numbers = []  # holds first-column part numbers extracted from BOM CSV
        self.circuit_label = None
        self.show_circuit_frame = None
        self.show_circuit_btn = None
        # Track when each preview is ready
        self.preview_ready = {k: False for k in SUPPORTED_TYPES}
        self.controls_shown = False

        self._build_ui()

    def _build_ui(self):
        # UI Construction
        card = tk.Frame(self, bg=self.card_color, bd=0, highlightthickness=0)
        card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.85, relheight=0.85)

        tk.Label(
            card, text="WCCA Automation", font=("Segoe UI", 28, "bold"),
            fg=self.text_color, bg=self.card_color
        ).pack(pady=(25, 10))

        columns = tk.Frame(card, bg=self.card_color)
        columns.pack(pady=10, padx=15, fill="both", expand=True)
        for i in range(3):
            columns.grid_columnconfigure(i, weight=1)

        col_defs = [
            ("Netlist", "xml", ".xml file"),
            ("Bom", "csv", ".csv file"),
            ("Conditions", "yaml", ".yaml file"),
        ]

        for idx, (col_title, ftype, label_text) in enumerate(col_defs):
            col = tk.Frame(columns, bg=self.card_color)
            col.grid(row=0, column=idx, padx=18, sticky="nsew")

            tk.Label(
                col, text=col_title, font=("Segoe UI", 16, "bold"),
                fg=self.text_color, bg=self.card_color
            ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 5))

            tk.Label(
                col, text=label_text, fg=self.text_color,
                bg=self.card_color, font=("Segoe UI", 12)
            ).grid(row=1, column=0, sticky="w")

            entry = tk.Entry(
                col, width=72, state="readonly", font=("Segoe UI", 12),
                bg=self.bg_color, fg="#000000", relief="flat" # Changed fg to #fff for dark mode
            )
            entry.grid(row=1, column=1, sticky="ew", padx=(8, 0))

            browse_btn = tk.Button(
                col, text="Browse", command=lambda t=ftype: self._browse_file(t),
                bg=self.button_color, fg=self.button_fg,
                font=("Segoe UI", 9, "bold"), relief="flat",
                activebackground="#9b7cff", activeforeground=self.button_fg, height=1
            )
            browse_btn.grid(row=1, column=2, sticky="w", padx=(8, 0))

            self.entries[ftype] = entry
            col.grid_columnconfigure(1, weight=1)

            # Preview label
            tk.Label(
                col, text="Preview", font=("Segoe UI", 13, "bold"),
                fg=self.text_color, bg=self.card_color
            ).grid(row=2, column=0, columnspan=3, sticky="w", pady=(8, 0))

            # Preview with scrollbars
            container = tk.Frame(col, bg="#39275c")
            container.grid(row=3, column=0, columnspan=3, sticky="nsew")
            container.grid_columnconfigure(0, weight=1)
            container.grid_rowconfigure(0, weight=1)
            self.preview_containers[ftype] = container

            # Create a default Text preview inside the container (used for XML/YAML and CSV fallback)
            preview = tk.Text(
                container, height=9, bg=self.preview_bg, fg=self.preview_fg,
                font=("Consolas", 10), relief="flat", state="disabled", wrap="none"
            )
            vsb = ttk.Scrollbar(container, orient="vertical", command=preview.yview, style="Dark.Vertical.TScrollbar")
            hsb = ttk.Scrollbar(container, orient="horizontal", command=preview.xview, style="Dark.Horizontal.TScrollbar")
            preview.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

            preview.grid(row=0, column=0, sticky="nsew")
            vsb.grid(row=0, column=1, sticky="ns")
            hsb.grid(row=1, column=0, sticky="ew")

            self.previews[ftype] = preview

            col.grid_rowconfigure(3, weight=1)

        # Footer area to avoid overlaying content; sits above the note
        self.footer = tk.Frame(card, bg=self.card_color)
        self.footer.pack(side="bottom", fill="x", pady=(8, 16))

        note = tk.Label(
            card,
            text="Note: Supported file types are .xml, .csv, and .yaml.",
            fg=self.note_fg, bg=self.card_color, font=("Segoe UI", 11)
        )
        # Place at bottom-right inside the card with small margin
        note.place(relx=1.0, rely=1.0, anchor="se", x=-16, y=-16)

        # Footer controls (initially not packed). Will be shown centered after preview loads
        self.show_circuit_frame = tk.Frame(self.footer, bg=self.card_color)
        self.show_circuit_btn = tk.Button(
            self.show_circuit_frame,
            text="Indentify Circuit Type",
            command=self._show_circuit_name,
            bg=self.button_color,
            fg=self.button_fg,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            activebackground="#9b7cff",
            activeforeground=self.button_fg,
            padx=12,
            pady=12,
            
        )
        self.show_circuit_btn.pack(side="left")
        self.circuit_label = tk.Label(
            self.show_circuit_frame,
            text="",
            bg=self.card_color,
            fg=self.text_color,
            font=("Segoe UI", 12),
            justify="center",
            wraplength=1000,
        )
        self.circuit_label.pack(side="top", padx=(12, 0))

    def show_progress(self, total):
        self.progress_total = max(1, total)
        frame = tk.Frame(self, bg=self.card_color)
        # Place at bottom-left with some margin
        frame.place(relx=0.0, rely=1.0, x=112, y=-72, anchor="sw")
        size = 96
        pad = 8
        canvas = tk.Canvas(frame, width=size, height=size, bg=self.card_color, highlightthickness=0)
        canvas.pack()
        canvas.create_oval(pad, pad, size-pad, size-pad, outline=self.preview_bg, width=6)
        arc = canvas.create_arc(pad, pad, size-pad, size-pad, start=90, extent=0, style=tk.ARC, width=6, outline=self.button_color)
        text = canvas.create_text(size//2, size//2, text="0%", fill=self.text_color, font=("Segoe UI", 12, "bold"))
        self.progress_frame = frame
        self.progress_canvas = canvas
        self.progress_arc = arc
        self.progress_text = text

    def update_progress(self, done, total):
        self.progress_total = max(1, total)
        percent = int((done / self.progress_total) * 100)
        extent = (percent / 100) * 360
        try:
            self.progress_canvas.itemconfig(self.progress_arc, extent=-extent)
            self.progress_canvas.itemconfig(self.progress_text, text=f"{percent}%")
        except Exception:
            pass
        self.update_idletasks()

    def close_progress(self):
        try:
            self.progress_frame.destroy()
        except Exception:
            pass
        self.progress_frame = None
        self.progress_canvas = None
        self.progress_arc = None
        self.progress_text = None

    def _maybe_show_circuit_controls(self):
        try:
            if self.controls_shown:
                return
            if all(self.preview_ready.values()):
                # Pack centered in the footer to avoid overlaying the table
                if self.show_circuit_frame is not None:
                    self.circuit_label.config(text="")
                    self.show_circuit_frame.pack(side="bottom", anchor="center")
                    self.controls_shown = True
        except Exception:
            pass

    def _show_circuit_name(self):
        try:
            path = self.selected_files.get("csv")
            if not path:
                name = "Unknown"
            else:
                name = os.path.splitext(os.path.basename(path))[0]
                name = self.names
            text = f"{name}"
            if self.circuit_label is not None:
                # Center and show text
                self.circuit_label.config(text=text)
            # Remove the button after showing the text
            if self.show_circuit_btn is not None:
                try:
                    self.show_circuit_btn.destroy()
                except Exception:
                    pass
                self.show_circuit_btn = None
        except Exception:
            if self.circuit_label is not None:
                self.circuit_label.config(text="your circuit is Unknown")

    def _render_json_table_preview(self):
        try:
            json_path = os.path.join(os.path.dirname(__file__), "parts.json")
            with open(json_path, "r", encoding="utf-8") as jf:
                data = json.load(jf)
            if not isinstance(data, list):
                raise ValueError("parts.json content is not a list")
            container = self.preview_containers.get("csv")
            if container is None:
                return
            # Clear any previous widgets (e.g., Text fallback)
            for child in container.winfo_children():
                child.destroy()
            # Render categorized CAP/RES tables
            show_categorized_tables(
                container,
                data,
                tree_style="Dark.Treeview",
                heading_style="Dark.Treeview.Heading",
                vscroll_style="Dark.Vertical.TScrollbar",
                hscroll_style="Dark.Horizontal.TScrollbar",
                height_rows=8
            )
            # Mark CSV preview as ready and try to show controls if all are ready
            self.preview_ready["csv"] = True
            self._maybe_show_circuit_controls()
        except Exception as e:
            # Fallback: show error message in the CSV container
            container = self.preview_containers.get("csv")
            if container is not None:
                for child in container.winfo_children():
                    child.destroy()
                lbl = tk.Label(container, text=f"Error loading JSON preview: {e}", bg=self.preview_bg, fg=self.text_color)
                lbl.grid(row=0, column=0, sticky="w", padx=8, pady=8)

    def run_digikey_search(self, parts):
        self.show_progress(len(parts))

        def runner():
            def cb(done, total):
                self.after(0, lambda: self.update_progress(done, total))
            try:
                digikey_search(parts, on_progress=cb)
            finally:
                self.after(0, self.close_progress)
                self.after(0, self._render_json_table_preview)

        threading.Thread(target=runner, daemon=True).start()

    def _browse_file(self, ftype):
        # File Browsing & Preview
        exts = SUPPORTED_TYPES[ftype]
        # Proper filetypes pattern for Tk's dialog
        patterns = tuple("*" + e for e in exts)
        filetypes = [
            (f"{ftype.upper()} files", patterns),
            ("All files", "*.*"),
        ]

        filepath = filedialog.askopenfilename(filetypes=filetypes)
        if not filepath:
            return

        if not is_supported_file(filepath, exts):
            messagebox.showerror("Unsupported File", f"Selected file is not a supported {ftype.upper()} file.")
            return

        if not is_file_size_valid(filepath, self.max_file_size):
            messagebox.showerror(
                "File Too Large",
                f"File exceeds the maximum size of {self.max_file_size // 1024 // 1024} MB."
            )
            return

        self.selected_files[ftype] = filepath
        # Reset readiness for this type on new selection
        if ftype in self.preview_ready:
            self.preview_ready[ftype] = False
            # Controls need to be re-shown after all previews complete again
            self.controls_shown = False

        # Update entry
        self.entries[ftype].config(state="normal")
        self.entries[ftype].delete(0, tk.END)
        self.entries[ftype].insert(0, os.path.basename(filepath))
        self.entries[ftype].config(state="readonly")

        # Preview the first 10 lines
        preview_text = ""
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                lines = []
                for i in range(10): # Preview first 10 lines
                    line = f.readline()
                    if not line:
                        break
                    lines.append(line.rstrip())
                preview_text = "\n".join(lines)
        except Exception as e:
            preview_text = f"Error reading file preview: {e}"
            logging.error(f"Error reading preview for {filepath}: {e}", exc_info=True)

        if ftype == "csv":
            # Do not show raw CSV content; we'll render JSON table after loading
            self.pending_preview["csv"] = ""
        else:
            self.previews[ftype].config(state="normal")
            self.previews[ftype].delete("1.0", tk.END)
            self.previews[ftype].insert("1.0", preview_text)
            self.previews[ftype].config(state="disabled")

        # If CSV selected, extract part numbers from first column
        if ftype == "csv":
            try:
                self.part_numbers = self._extract_part_numbers_from_csv(filepath, col=0)
            except Exception as e:
                logging.error(str(e), exc_info=True)
                self.part_numbers = []
                messagebox.showwarning("CSV Parse", f"Couldn't parse part numbers:\n{e}")

            # Do not append part numbers to preview; we'll render JSON table instead
        else:
            # Mark XML/YAML preview as ready and try to show controls
            self.preview_ready[ftype] = True
            self._maybe_show_circuit_controls()

    def _extract_part_numbers_from_csv(self, filepath, col=0):
        """Reads the CSV and returns a de-duplicated list of values from column col (default: first column).
        Automatically sniffs delimiter and whether there is a header row."""
        part_numbers = []
        ref_num=[]
        with open(filepath, "r", encoding="utf-8", errors="ignore", newline="") as f:
            sample = f.read(2048)
            f.seek(0)

            # Detect delimiter
            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=[",", ";", "\t", "|"])
            except csv.Error:
                dialect = csv.get_dialect("excel")

            # Detect header
            has_header = False
            try:
                has_header = csv.Sniffer().has_header(sample)
            except Exception:
                # Some Python versions may raise ValueError("bad delimiter value").
                # Fall back to assuming there is no header.
                has_header = False

            reader = csv.reader(f, dialect)
            for idx, row in enumerate(reader):
                if not row:
                    continue
                if has_header and idx == 0:
                    # skip header row
                    continue

                if col < len(row):
                    val = row[col].strip()
                    val1 = row[col+1].strip()
                    if val:
                        part_numbers.append(val)
                        ref_num.append(val1)

        # De-duplicate while preserving order
        
        ind=[]
        print(ref_num)
        for e in range(len(ref_num)):
            if "u" in ref_num[e].lower():
                ind.append(e)
        chip=[]
        for e in ind:
            chip.append(part_numbers[e]) 
        self.names=genAi(chip)
        
        seen = set()
        uniq = [x for x in part_numbers if not (x in seen or seen.add(x))]
        self.run_digikey_search(uniq)
        return uniq
  
        try:
            self.part_numbers = self._extract_part_numbers_from_csv(filepath, col=0)
        except Exception as e:
            logging.error(str(e), exc_info=True)
            self.part_numbers = []
            messagebox.showwarning("CSV Parse", f"Couldn't parse part numbers:\n{e}")


def _extract_part_numbers_from_csv(self, filepath, col=0):
    """Reads the CSV and returns a de-duplicated list of values from column col (default: first column).
    Automatically sniffs delimiter and whether there is a header row."""
    part_numbers = []
    ref_num=[]
    with open(filepath, "r", encoding="utf-8", errors="ignore", newline="") as f:
        sample = f.read(2048)
        f.seek(0)

        # Detect delimiter
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=[",", ";", "\t", "|"])
        except csv.Error:
            dialect = csv.get_dialect("excel")

        # Detect header
        has_header = False
        try:
            has_header = csv.Sniffer().has_header(sample)
        except Exception:
            # Some Python versions may raise ValueError("bad delimiter value").
            # Fall back to assuming there is no header.
            has_header = False

        reader = csv.reader(f, dialect)
        for idx, row in enumerate(reader):
            if not row:
                continue
            if has_header and idx == 0:
                # skip header row
                continue

            if col < len(row):
                val = row[col].strip()
                val1=row[col+1].strip()
                if val:
                    part_numbers.append(val)
                    ref_num.append(val1)

  

    # De-duplicate while preserving order
    seen = set()
    uniq = [x for x in part_numbers if not (x in seen or seen.add(x))]
    self.run_digikey_search(uniq)
    return uniq


# ------------------------- Optional accessor -------------------------
def get_part_numbers(self):
    """Return the current list of extracted part numbers."""
    return self.part_numbers

# ------------------------- Entry point -------------------------
if __name__ == "__main__":
    app = FileUploaderApp()
    app.mainloop()