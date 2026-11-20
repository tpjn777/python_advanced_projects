"""
YouTube Download Manager (Tkinter + yt-dlp)

Install:
    pip install yt-dlp
Optional but recommended (needed for 1080p+ merging and MP3 conversion):
    ffmpeg  ->  https://ffmpeg.org/download.html  (must be on your PATH)

Only download content you own or have permission to download.
"""

import os
import re
import queue
import shutil
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import yt_dlp


ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")
URL_RE = re.compile(r"^(https?://)?(www\.|m\.|music\.)?(youtube\.com|youtu\.be)/", re.I)


class DownloadCancelled(Exception):
    pass


def format_duration(seconds):
    if not seconds:
        return "Unknown"
    h, rem = divmod(int(seconds), 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def clean_error(error):
    return ANSI_RE.sub("", str(error)).strip()


class Application:

    BG = "#101827"
    CARD = "#1e293b"

    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Download Manager")
        self.root.geometry("950x760")
        self.root.minsize(750, 650)
        self.root.configure(bg=self.BG)

        self.download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        self.has_ffmpeg = shutil.which("ffmpeg") is not None

        self.url = None
        self.info = None
        self.options = []          # list of (label, kind, height)
        self.cancel_flag = threading.Event()

        # Thread-safe UI updates: workers put callables here, main thread runs them.
        self.ui_queue = queue.Queue()

        self.setup_styles()
        self.create_widgets()
        self.process_queue()

    # ---------------- THREAD-SAFE UI ----------------

    def ui(self, func, *args):
        self.ui_queue.put((func, args))

    def process_queue(self):
        try:
            while True:
                func, args = self.ui_queue.get_nowait()
                func(*args)
        except queue.Empty:
            pass
        self.root.after(100, self.process_queue)

    # ---------------- STYLES ----------------

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "TCombobox",
            fieldbackground="#334155",
            background="#334155",
            foreground="white",
            arrowcolor="white",
            padding=8,
        )
        style.map("TCombobox", fieldbackground=[("readonly", "#334155")],
                  foreground=[("readonly", "white")])

        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor="#263449",
            background="#38bdf8",
            thickness=12,
        )

    # ---------------- INTERFACE ----------------

    def label(self, parent, text, size=10, bold=False, fg="#94a3b8", bg=None, **kw):
        return tk.Label(
            parent,
            text=text,
            font=("Arial", size, "bold" if bold else "normal"),
            fg=fg,
            bg=bg or parent.cget("bg"),
            **kw,
        )

    def create_widgets(self):
        main = tk.Frame(self.root, bg=self.BG)
        main.pack(fill="both", expand=True, padx=45, pady=25)

        # Header
        header = tk.Frame(main, bg=self.BG)
        header.pack(fill="x", pady=(5, 25))
        self.label(header, "YT", 25, True, "#38bdf8").pack()
        self.label(header, "YouTube Download Manager", 28, True, "white").pack(pady=(8, 5))
        self.label(header, "Download videos with a simple and clean interface", 11).pack()

        # Card
        card = tk.Frame(main, bg=self.CARD, padx=30, pady=25)
        card.pack(fill="x", pady=10)

        self.label(card, "VIDEO URL", 10, True).pack(anchor="w", pady=(0, 10))

        self.url_entry = tk.Entry(
            card, font=("Arial", 13), bg="#334155", fg="white",
            insertbackground="white", relief="flat", bd=0,
        )
        self.url_entry.pack(fill="x", ipady=13)
        self.url_entry.bind("<Return>", lambda e: self.fetch_video())

        self.fetch_button = tk.Button(
            card, text="Fetch Video Information", font=("Arial", 11, "bold"),
            bg="#2563eb", fg="white", activebackground="#1d4ed8",
            activeforeground="white", relief="flat", cursor="hand2",
            command=self.fetch_video,
        )
        self.fetch_button.pack(fill="x", pady=(15, 20), ipady=10)

        self.info_label = self.label(
            card, "Video information will appear here.", 11, fg="#cbd5e1",
            wraplength=750, justify="left",
        )
        self.info_label.pack(anchor="w", pady=(0, 15))

        self.label(card, "VIDEO QUALITY", 10, True).pack(anchor="w", pady=(0, 8))

        self.quality = ttk.Combobox(
            card, state="readonly", values=["Best available"], font=("Arial", 11),
        )
        self.quality.current(0)
        self.quality.pack(fill="x", ipady=5)

        if not self.has_ffmpeg:
            self.label(
                card,
                "ffmpeg not found: quality is limited to pre-merged streams "
                "(usually up to 720p) and MP3 conversion is unavailable.",
                9, fg="#fbbf24", wraplength=750, justify="left",
            ).pack(anchor="w", pady=(8, 0))

        self.label(card, "DOWNLOAD LOCATION", 10, True).pack(anchor="w", pady=(18, 8))

        location_frame = tk.Frame(card, bg=self.CARD)
        location_frame.pack(fill="x")

        self.folder_label = tk.Label(
            location_frame, text=self.download_folder, font=("Arial", 10),
            fg="#cbd5e1", bg="#334155", anchor="w", padx=12,
        )
        self.folder_label.pack(side="left", fill="x", expand=True, ipady=11)

        tk.Button(
            location_frame, text="Browse", font=("Arial", 10, "bold"),
            bg="#475569", fg="white", relief="flat", cursor="hand2",
            command=self.choose_folder,
        ).pack(side="right", padx=(10, 0), ipady=8, ipadx=12)

        # Buttons
        button_row = tk.Frame(card, bg=self.CARD)
        button_row.pack(fill="x", pady=(25, 5))

        self.download_button = tk.Button(
            button_row, text="DOWNLOAD", font=("Arial", 12, "bold"),
            bg="#0ea5e9", fg="white", activebackground="#0284c7",
            activeforeground="white", relief="flat", cursor="hand2",
            command=self.start_download, state="disabled",
        )
        self.download_button.pack(side="left", fill="x", expand=True, ipady=13)

        self.cancel_button = tk.Button(
            button_row, text="CANCEL", font=("Arial", 12, "bold"),
            bg="#dc2626", fg="white", activebackground="#b91c1c",
            activeforeground="white", relief="flat", cursor="hand2",
            command=self.cancel_download, state="disabled",
        )
        self.cancel_button.pack(side="right", padx=(10, 0), ipady=13, ipadx=18)

        # Progress
        progress_frame = tk.Frame(main, bg=self.BG)
        progress_frame.pack(fill="x", pady=15)

        self.status_label = self.label(progress_frame, "Ready to download", 11)
        self.status_label.pack(anchor="w", pady=(0, 10))

        self.progress = ttk.Progressbar(
            progress_frame, style="Custom.Horizontal.TProgressbar", maximum=100,
        )
        self.progress.pack(fill="x")

        self.percent_label = self.label(progress_frame, "0%", 11, True, "#38bdf8")
        self.percent_label.pack(anchor="e", pady=8)

        self.label(main, "YouTube Download Manager  \u2022  Personal use", 9,
                   fg="#64748b").pack(side="bottom", pady=5)

    # ---------------- FOLDER ----------------

    def choose_folder(self):
        folder = filedialog.askdirectory(initialdir=self.download_folder)
        if folder:
            self.download_folder = folder
            self.folder_label.config(text=folder)

    # ---------------- VALIDATION ----------------

    def validate_url(self):
        url = self.url_entry.get().strip()

        if not URL_RE.match(url):
            messagebox.showerror("Invalid URL", "Please enter a valid YouTube video URL.")
            return None

        if not url.lower().startswith(("http://", "https://")):
            url = "https://" + url

        return url

    # ---------------- FETCH ----------------

    def fetch_video(self):
        if str(self.fetch_button["state"]) == "disabled":
            return

        url = self.validate_url()
        if not url:
            return

        self.fetch_button.config(state="disabled")
        self.download_button.config(state="disabled")
        self.status_label.config(text="Fetching video information...")
        self.info_label.config(text="Please wait...")

        threading.Thread(target=self.fetch_worker, args=(url,), daemon=True).start()

    def fetch_worker(self, url):
        try:
            opts = {"quiet": True, "no_warnings": True, "noplaylist": True,
                    "skip_download": True}
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)

            # Collect available video heights (ignore formats with no resolution).
            heights = sorted(
                {
                    f["height"]
                    for f in info.get("formats", [])
                    if f.get("height") and f.get("vcodec") not in (None, "none")
                },
                reverse=True,
            )

            if not self.has_ffmpeg:
                # Without ffmpeg only pre-merged formats are usable.
                progressive = {
                    f["height"]
                    for f in info.get("formats", [])
                    if f.get("height")
                    and f.get("vcodec") not in (None, "none")
                    and f.get("acodec") not in (None, "none")
                }
                heights = [h for h in heights if h in progressive]

            if not heights:
                raise Exception("No downloadable video formats were found.")

            options = [("Best available", "best", None)]
            options += [(f"{h}p (MP4)", "video", h) for h in heights]
            options.append(
                ("Audio only (MP3)" if self.has_ffmpeg else "Audio only (original format)",
                 "audio", None)
            )

            self.ui(self.fetch_success, url, info, options)

        except Exception as error:
            self.ui(self.fetch_error, clean_error(error))

    def fetch_success(self, url, info, options):
        self.url = url
        self.info = info
        self.options = options

        self.info_label.config(
            text=f"Title: {info.get('title', 'Unknown')}\n"
                 f"Author: {info.get('uploader') or info.get('channel') or 'Unknown'}\n"
                 f"Duration: {format_duration(info.get('duration'))}"
        )

        self.quality["values"] = [o[0] for o in options]
        self.quality.current(0)

        self.status_label.config(text="Video information loaded successfully.")
        self.fetch_button.config(state="normal")
        self.download_button.config(state="normal")

    def fetch_error(self, error):
        self.fetch_button.config(state="normal")
        self.status_label.config(text="Unable to fetch video.")
        messagebox.showerror("Fetch Error", error)

    # ---------------- DOWNLOAD ----------------

    def build_ydl_options(self, kind, height):
        opts = {
            "outtmpl": os.path.join(self.download_folder, "%(title)s.%(ext)s"),
            "noplaylist": True,
            "quiet": True,
            "no_warnings": True,
            "noprogress": True,
            "progress_hooks": [self.progress_hook],
            "restrictfilenames": False,
            "windowsfilenames": True,
        }

        if kind == "audio":
            opts["format"] = "bestaudio/best"
            if self.has_ffmpeg:
                opts["postprocessors"] = [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }]
        else:
            cap = f"[height<={height}]" if height else ""
            if self.has_ffmpeg:
                opts["format"] = f"bestvideo{cap}+bestaudio/best{cap}"
                opts["merge_output_format"] = "mp4"
            else:
                opts["format"] = f"best{cap}[acodec!=none][vcodec!=none]/best{cap}"

        return opts

    def start_download(self):
        if not self.url or not self.options:
            return

        selected = self.quality.current()
        if selected < 0:
            selected = 0
        _, kind, height = self.options[selected]

        self.cancel_flag.clear()
        self.download_button.config(state="disabled")
        self.fetch_button.config(state="disabled")
        self.cancel_button.config(state="normal")

        self.progress["value"] = 0
        self.percent_label.config(text="0%")
        self.status_label.config(text="Preparing download...")

        threading.Thread(
            target=self.download_worker, args=(kind, height), daemon=True
        ).start()

    def cancel_download(self):
        self.cancel_flag.set()
        self.status_label.config(text="Cancelling...")
        self.cancel_button.config(state="disabled")

    def download_worker(self, kind, height):
        try:
            os.makedirs(self.download_folder, exist_ok=True)
            opts = self.build_ydl_options(kind, height)
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([self.url])
            self.ui(self.download_success)

        except DownloadCancelled:
            self.ui(self.download_cancelled)

        except Exception as error:
            if self.cancel_flag.is_set():
                self.ui(self.download_cancelled)
            else:
                self.ui(self.download_error, clean_error(error))

    # ---------------- PROGRESS ----------------

    def progress_hook(self, d):
        # Runs in the worker thread.
        if self.cancel_flag.is_set():
            raise DownloadCancelled()

        status = d.get("status")

        if status == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate")
            if total:
                pct = d.get("downloaded_bytes", 0) / total * 100
                self.ui(self.update_progress, min(pct, 100.0))

        elif status == "finished":
            # One file (video or audio part) finished; merging/conversion may follow.
            self.ui(self.set_status, "Processing (merging / converting)...")

    def update_progress(self, percentage):
        self.progress["value"] = percentage
        self.percent_label.config(text=f"{percentage:.1f}%")
        self.status_label.config(text="Downloading...")

    def set_status(self, text):
        self.status_label.config(text=text)

    # ---------------- RESULTS ----------------

    def reset_buttons(self):
        self.download_button.config(state="normal")
        self.fetch_button.config(state="normal")
        self.cancel_button.config(state="disabled")

    def download_success(self):
        self.progress["value"] = 100
        self.percent_label.config(text="100%")
        self.status_label.config(text="Download completed successfully!")
        self.reset_buttons()

        messagebox.showinfo(
            "Success",
            f"Download completed successfully!\n\nLocation:\n{self.download_folder}",
        )

    def download_cancelled(self):
        self.progress["value"] = 0
        self.percent_label.config(text="0%")
        self.status_label.config(text="Download cancelled.")
        self.reset_buttons()

    def download_error(self, error):
        self.status_label.config(text="Download failed.")
        self.reset_buttons()
        messagebox.showerror("Download Error", error)


# ---------------- MAIN ----------------

if __name__ == "__main__":
    window = tk.Tk()
    app = Application(window)
    window.mainloop()