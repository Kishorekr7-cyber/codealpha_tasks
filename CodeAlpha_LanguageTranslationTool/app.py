"""
CodeAlpha Internship - Task 1: Language Translation Tool
Uses deep-translator (free, no API key needed) + Tkinter GUI
Install: pip install deep-translator tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox
from deep_translator import GoogleTranslator

# ── Supported languages ──────────────────────────────────────────────────────
LANGUAGES = {
    "Auto Detect": "auto",
    "English": "en",
    "Tamil": "ta",
    "Hindi": "hi",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Chinese (Simplified)": "zh-CN",
    "Japanese": "ja",
    "Korean": "ko",
    "Arabic": "ar",
    "Portuguese": "pt",
    "Russian": "ru",
    "Italian": "it",
    "Dutch": "nl",
    "Turkish": "tr",
    "Telugu": "te",
    "Malayalam": "ml",
    "Kannada": "kn",
    "Bengali": "bn",
}

# ── Main App ──────────────────────────────────────────────────────────────────
class TranslationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌐 Language Translation Tool — CodeAlpha")
        self.root.geometry("750x520")
        self.root.configure(bg="#0f172a")
        self.root.resizable(True, True)

        self._build_ui()

    def _build_ui(self):
        # ── Title ──
        title = tk.Label(
            self.root,
            text="🌐 Language Translator",
            font=("Segoe UI", 18, "bold"),
            fg="#38bdf8",
            bg="#0f172a",
        )
        title.pack(pady=(18, 4))

        subtitle = tk.Label(
            self.root,
            text="Powered by Google Translate  •  CodeAlpha AI Internship",
            font=("Segoe UI", 9),
            fg="#64748b",
            bg="#0f172a",
        )
        subtitle.pack(pady=(0, 14))

        # ── Language selectors ──
        lang_frame = tk.Frame(self.root, bg="#0f172a")
        lang_frame.pack(fill="x", padx=30)

        lang_names = list(LANGUAGES.keys())

        tk.Label(lang_frame, text="Source Language", font=("Segoe UI", 10),
                 fg="#94a3b8", bg="#0f172a").grid(row=0, column=0, sticky="w")
        tk.Label(lang_frame, text="Target Language", font=("Segoe UI", 10),
                 fg="#94a3b8", bg="#0f172a").grid(row=0, column=2, sticky="w")

        self.src_var = tk.StringVar(value="Auto Detect")
        self.tgt_var = tk.StringVar(value="Tamil")

        src_dd = ttk.Combobox(lang_frame, textvariable=self.src_var,
                              values=lang_names, width=28, state="readonly")
        src_dd.grid(row=1, column=0, padx=(0, 10), pady=4)

        swap_btn = tk.Button(
            lang_frame, text="⇄", font=("Segoe UI", 13, "bold"),
            bg="#1e293b", fg="#38bdf8", bd=0, cursor="hand2",
            command=self._swap_languages, padx=8
        )
        swap_btn.grid(row=1, column=1, padx=6)

        tgt_dd = ttk.Combobox(lang_frame, textvariable=self.tgt_var,
                              values=lang_names[1:], width=28, state="readonly")
        tgt_dd.grid(row=1, column=2, padx=(10, 0), pady=4)

        # ── Text areas ──
        text_frame = tk.Frame(self.root, bg="#0f172a")
        text_frame.pack(fill="both", expand=True, padx=30, pady=10)
        text_frame.columnconfigure(0, weight=1)
        text_frame.columnconfigure(1, weight=1)

        tk.Label(text_frame, text="Enter Text", font=("Segoe UI", 10),
                 fg="#94a3b8", bg="#0f172a").grid(row=0, column=0, sticky="w")
        tk.Label(text_frame, text="Translation", font=("Segoe UI", 10),
                 fg="#94a3b8", bg="#0f172a").grid(row=0, column=1, sticky="w", padx=(14, 0))

        self.input_text = tk.Text(
            text_frame, height=10, font=("Segoe UI", 11),
            bg="#1e293b", fg="#f1f5f9", insertbackground="#38bdf8",
            relief="flat", padx=10, pady=10, wrap="word"
        )
        self.input_text.grid(row=1, column=0, sticky="nsew", padx=(0, 7))

        self.output_text = tk.Text(
            text_frame, height=10, font=("Segoe UI", 11),
            bg="#1e293b", fg="#4ade80", insertbackground="#38bdf8",
            relief="flat", padx=10, pady=10, wrap="word", state="disabled"
        )
        self.output_text.grid(row=1, column=1, sticky="nsew", padx=(7, 0))
        text_frame.rowconfigure(1, weight=1)

        # ── Buttons ──
        btn_frame = tk.Frame(self.root, bg="#0f172a")
        btn_frame.pack(pady=12)

        translate_btn = tk.Button(
            btn_frame, text="  Translate  ", font=("Segoe UI", 12, "bold"),
            bg="#0284c7", fg="white", relief="flat", cursor="hand2",
            padx=20, pady=8, command=self._translate
        )
        translate_btn.grid(row=0, column=0, padx=8)

        clear_btn = tk.Button(
            btn_frame, text="  Clear  ", font=("Segoe UI", 12),
            bg="#334155", fg="#cbd5e1", relief="flat", cursor="hand2",
            padx=14, pady=8, command=self._clear
        )
        clear_btn.grid(row=0, column=1, padx=8)

        copy_btn = tk.Button(
            btn_frame, text="  Copy Result  ", font=("Segoe UI", 12),
            bg="#334155", fg="#cbd5e1", relief="flat", cursor="hand2",
            padx=14, pady=8, command=self._copy
        )
        copy_btn.grid(row=0, column=2, padx=8)

        # Status bar
        self.status = tk.Label(self.root, text="Ready", font=("Segoe UI", 9),
                               fg="#64748b", bg="#0f172a")
        self.status.pack(pady=(0, 8))

    # ── Actions ──────────────────────────────────────────────────────────────
    def _translate(self):
        text = self.input_text.get("1.0", "end").strip()
        if not text:
            messagebox.showwarning("Empty Input", "Please enter some text to translate.")
            return

        src_code = LANGUAGES[self.src_var.get()]
        tgt_code = LANGUAGES[self.tgt_var.get()]

        self.status.config(text="Translating…", fg="#fbbf24")
        self.root.update()

        try:
            result = GoogleTranslator(source=src_code, target=tgt_code).translate(text)
            self.output_text.config(state="normal")
            self.output_text.delete("1.0", "end")
            self.output_text.insert("end", result)
            self.output_text.config(state="disabled")
            self.status.config(text="✅ Translation complete", fg="#4ade80")
        except Exception as e:
            messagebox.showerror("Translation Error", str(e))
            self.status.config(text="❌ Error occurred", fg="#f87171")

    def _swap_languages(self):
        src, tgt = self.src_var.get(), self.tgt_var.get()
        if src == "Auto Detect":
            return
        self.src_var.set(tgt)
        self.tgt_var.set(src)

    def _clear(self):
        self.input_text.delete("1.0", "end")
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.config(state="disabled")
        self.status.config(text="Ready", fg="#64748b")

    def _copy(self):
        result = self.output_text.get("1.0", "end").strip()
        if result:
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            self.status.config(text="📋 Copied to clipboard!", fg="#38bdf8")
        else:
            messagebox.showinfo("Nothing to copy", "No translation result to copy.")


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = TranslationApp(root)
    root.mainloop()
