import customtkinter as ctk
from transliterate import Transliterator
import tkinter as tk

# Set default theme settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue") # We will override specific colors manually for premium look

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Kril-Lotin Converter Pro")
        self.geometry("950x650")
        self.minsize(800, 500)
        
        # Colors & Fonts
        self.col_bg = "#1a1a2e"       # Main Background (Deep Navy)
        self.col_card = "#16213e"     # Card Background (Lighter Navy) - slightly transparent feel logic
        self.col_accent = "#4CC9F0"   # Cyan Accent
        self.col_text = "#e0e0e0"     # Light Text
        self.col_input_bg = "#1f2945" # Input Field Background
        
        self.font_main = ("Segoe UI", 16)
        self.font_header = ("Segoe UI", 24, "bold")
        self.font_mono = ("Consolas", 14) # Good for text editing
        
        self.configure(fg_color=self.col_bg)

        # Logic
        self.transliterator = Transliterator()
        self.direction = "kril_to_lotin"

        # Layout Configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0) # Header
        self.grid_rowconfigure(1, weight=1) # Content
        self.grid_rowconfigure(2, weight=0) # Footer

        self.setup_ui()

    def setup_ui(self):
        # --- Header ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent", height=60)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=(20, 10))
        
        self.logo_label = ctk.CTkLabel(self.header_frame, text="Kril-Lotin Converter", 
                                     font=self.font_header, text_color=self.col_accent)
        self.logo_label.pack(side="left")
        
        # Toggle Button (Segmented Control style)
        self.seg_ctrl = ctk.CTkSegmentedButton(self.header_frame, values=["Krill -> Lotin", "Lotin -> Krill"],
                                             command=self.on_segment_change,
                                             font=("Segoe UI", 12, "bold"),
                                             selected_color=self.col_accent,
                                             fg_color=self.col_card,
                                             text_color=self.col_text,
                                             selected_hover_color="#3db5e0")
        self.seg_ctrl.set("Krill -> Lotin")
        self.seg_ctrl.pack(side="right")


        # --- Main Content Area ---
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.content_frame.grid_columnconfigure(0, weight=1) # Input
        self.content_frame.grid_columnconfigure(1, weight=0) # Swap Arrow
        self.content_frame.grid_columnconfigure(2, weight=1) # Output
        self.content_frame.grid_rowconfigure(0, weight=1) # Allow cards to expand vertically

        # Card 1: Input
        self.card_input = ctk.CTkFrame(self.content_frame, fg_color=self.col_card, corner_radius=15, border_width=1, border_color="#2e3a59")
        self.card_input.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.lbl_input = ctk.CTkLabel(self.card_input, text="KRILCHA (Kirish)", font=("Segoe UI", 12, "bold"), text_color="gray")
        self.lbl_input.pack(anchor="w", padx=15, pady=(15, 5))
        
        self.input_text = ctk.CTkTextbox(self.card_input, font=self.font_mono, fg_color=self.col_input_bg, 
                                       text_color=self.col_text, wrap="word", corner_radius=10)
        self.input_text.pack(expand=True, fill="both", padx=15, pady=(0, 15))
        self.input_text.bind("<KeyRelease>", self.on_text_change)
        self.input_text.bind("<<Paste>>", self.on_paste)
        
        # Middle Swap Indicator (Visual only, or functional? Visual for now as segmented ctrl handles logic)
        self.swap_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.swap_frame.grid(row=0, column=1, padx=5)
        self.swap_icon = ctk.CTkLabel(self.swap_frame, text="→", font=("Arial", 30), text_color=self.col_accent)
        self.swap_icon.pack()

        # Card 2: Output
        self.card_output = ctk.CTkFrame(self.content_frame, fg_color=self.col_card, corner_radius=15, border_width=1, border_color="#2e3a59")
        self.card_output.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
        
        self.lbl_output = ctk.CTkLabel(self.card_output, text="LOTINCHA (Natija)", font=("Segoe UI", 12, "bold"), text_color="gray")
        self.lbl_output.pack(anchor="w", padx=15, pady=(15, 5))
        
        self.output_text = ctk.CTkTextbox(self.card_output, font=self.font_mono, fg_color=self.col_input_bg, 
                                        text_color=self.col_text, wrap="word", corner_radius=10)
        self.output_text.pack(expand=True, fill="both", padx=15, pady=(0, 15))
        self.output_text.configure(state="disabled")

        # --- Footer ---
        self.footer_frame = ctk.CTkFrame(self, fg_color="#121826", height=40, corner_radius=0)
        self.footer_frame.grid(row=2, column=0, sticky="ew")
        
        self.words_label = ctk.CTkLabel(self.footer_frame, text="So'zlar: 0", font=("Segoe UI", 11), text_color="gray")
        self.words_label.pack(side="left", padx=20)
        
        self.author_label = ctk.CTkLabel(self.footer_frame, text="Muallif: Asliddin", font=("Segoe UI", 11, "italic"), text_color="#555")
        self.author_label.pack(side="left", padx=20)
        
        self.copy_btn = ctk.CTkButton(self.footer_frame, text="Nusxalash", command=self.copy_result, 
                                    font=("Segoe UI", 12, "bold"), 
                                    height=28, width=100, corner_radius=14,
                                    fg_color=self.col_accent, hover_color="#3db5e0", text_color="black")
        self.copy_btn.pack(side="right", padx=20, pady=6)

    def on_segment_change(self, value):
        if value == "Krill -> Lotin":
            self.direction = "kril_to_lotin"
            self.lbl_input.configure(text="KRILCHA (Kirish)")
            self.lbl_output.configure(text="LOTINCHA (Natija)")
        else:
            self.direction = "lotin_to_kril"
            self.lbl_input.configure(text="LOTINCHA (Kirish)")
            self.lbl_output.configure(text="KRILCHA (Natija)")
        self.on_text_change(None)

    def sanitize_input(self, text):
        safe_chars = []
        for char in text:
            if ord(char) >= 32 or char in "\n\t\r":
                safe_chars.append(char)
        cleaned = "".join(safe_chars)
        MAX_CHARS = 5000 
        if len(cleaned) > MAX_CHARS:
             cleaned = cleaned[:MAX_CHARS]
        return cleaned

    def on_text_change(self, event):
        raw_text = self.input_text.get("1.0", "end-1c")
        text = self.sanitize_input(raw_text)
        
        words = text.split()
        self.words_label.configure(text=f"So'zlar: {len(words)}")

        if not text.strip():
            self.output_text.configure(state="normal")
            self.output_text.delete("1.0", "end")
            self.output_text.configure(state="disabled")
            return

        if self.direction == "kril_to_lotin":
            result = self.transliterator.to_latin(text)
        else:
            result = self.transliterator.to_cyrillic(text)
        
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", result)
        self.output_text.configure(state="disabled")

    def on_paste(self, event):
        try:
            clipboard = self.clipboard_get()
            clipboard = self.sanitize_input(clipboard)
            words = clipboard.split()
            if len(words) > 200:
                truncated = " ".join(words[:200])
                self.input_text.insert("insert", truncated)
                self.words_label.configure(text=f"LIMIT: 200 so'z (Qisqartirildi)", text_color="red")
                self.after(3000, lambda: self.words_label.configure(text_color="gray"))
                self.on_text_change(None)
                return "break"
        except:
            pass
        self.after(10, lambda: self.on_text_change(None))

    def copy_result(self):
        result = self.output_text.get("1.0", "end-1c")
        self.clipboard_clear()
        self.clipboard_append(result)
        self.copy_btn.configure(text="Nusxalandi!")
        self.after(2000, lambda: self.copy_btn.configure(text="Nusxalash"))

if __name__ == "__main__":
    app = App()
    app.mainloop()
