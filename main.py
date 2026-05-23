# =========================================
# CaesarCipher — Ultra Modern Edition
# =========================================

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

# =========================================
# THEMES
# =========================================

LIGHT_THEME = {
    "bg": "#f1f5f9",
    "card": "#ffffff",
    "text": "#0f172a",
    "entry": "#f8fafc",
    "accent": "#2563eb",
    "accent_hover": "#1d4ed8",
    "border": "#cbd5e1",
    "success": "#16a34a"
}

DARK_THEME = {
    "bg": "#0f172a",
    "card": "#1e293b",
    "text": "#f8fafc",
    "entry": "#334155",
    "accent": "#3b82f6",
    "accent_hover": "#2563eb",
    "border": "#475569",
    "success": "#22c55e"
}

theme = DARK_THEME

# =========================================
# ROOT
# =========================================

root = tk.Tk()
root.title("CaesarCipher")
root.state("zoomed")
root.configure(bg=theme["bg"])

# =========================================
# FONTS
# =========================================

TITLE_FONT = ("Segoe UI", 28, "bold")
SUBTITLE_FONT = ("Segoe UI", 12)
LABEL_FONT = ("Segoe UI", 12, "bold")
TEXT_FONT = ("Consolas", 13)
BUTTON_FONT = ("Segoe UI", 12, "bold")

# =========================================
# SCROLLABLE AREA
# =========================================

main_canvas = tk.Canvas(
    root,
    bg=theme["bg"],
    highlightthickness=0
)

scrollbar = tk.Scrollbar(
    root,
    orient="vertical",
    command=main_canvas.yview
)

scrollable_frame = tk.Frame(
    main_canvas,
    bg=theme["bg"]
)

scrollable_frame.bind(
    "<Configure>",
    lambda e: main_canvas.configure(
        scrollregion=main_canvas.bbox("all")
    )
)

main_canvas.create_window(
    (0, 0),
    window=scrollable_frame,
    anchor="nw"
)

main_canvas.configure(
    yscrollcommand=scrollbar.set,
    yscrollincrement=2
)

main_canvas.pack(
    side="left",
    fill="both",
    expand=True
)

scrollbar.pack(
    side="right",
    fill="y"
)

# =========================================
# CENTERED CONTAINER
# =========================================

container = tk.Frame(
    scrollable_frame,
    bg=theme["bg"]
)

container.pack(
    fill="both",
    expand=True,
    pady=30
)

# =========================================
# SMOOTH SCROLL
# =========================================

def _on_mousewheel(event):

    delta = int(-1 * (event.delta / 120))

    main_canvas.yview_scroll(
        delta,
        "units"
    )

main_canvas.bind_all(
    "<MouseWheel>",
    _on_mousewheel
)

# =========================================
# CAESAR CIPHER
# =========================================

def caesar_cipher(text, shift, decrypt=False):

    if decrypt:
        shift = -shift

    ru_lower = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    ru_upper = ru_lower.upper()

    en_lower = 'abcdefghijklmnopqrstuvwxyz'
    en_upper = en_lower.upper()

    result = ""

    for char in text:

        if char in en_lower:
            idx = en_lower.index(char)
            result += en_lower[(idx + shift) % 26]

        elif char in en_upper:
            idx = en_upper.index(char)
            result += en_upper[(idx + shift) % 26]

        elif char in ru_lower:
            idx = ru_lower.index(char)
            result += ru_lower[(idx + shift) % 32]

        elif char in ru_upper:
            idx = ru_upper.index(char)
            result += ru_upper[(idx + shift) % 32]

        else:
            result += char

    return result

# =========================================
# FUNCTIONS
# =========================================

def process_text(decrypt=False):

    text = input_box.get("1.0", tk.END).strip()

    try:
        shift = int(shift_entry.get())

        if shift < 1 or shift > 25:
            raise ValueError

    except:
        messagebox.showerror(
            "Ошибка",
            "Ключ должен быть числом от 1 до 25"
        )
        return

    result = caesar_cipher(text, shift, decrypt)

    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, result)

    status_label.config(
        text="✓ Операция успешно завершена",
        fg=theme["success"]
    )

def encrypt_text():
    process_text(False)

def decrypt_text():
    process_text(True)

def clear_fields():

    input_box.delete("1.0", tk.END)
    output_box.delete("1.0", tk.END)
    shift_entry.delete(0, tk.END)

    status_label.config(
        text="✓ Поля очищены",
        fg=theme["success"]
    )

def load_file():

    path = filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt")]
    )

    if path:

        try:

            with open(path, "r", encoding="utf-8") as file:
                content = file.read()

            input_box.delete("1.0", tk.END)
            input_box.insert(tk.END, content)

            status_label.config(
                text="✓ Файл успешно загружен",
                fg=theme["success"]
            )

        except Exception as e:

            messagebox.showerror(
                "Ошибка",
                str(e)
            )

def save_file():

    path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")]
    )

    if path:

        try:

            with open(path, "w", encoding="utf-8") as file:
                file.write(output_box.get("1.0", tk.END))

            status_label.config(
                text="✓ Файл сохранён",
                fg=theme["success"]
            )

        except Exception as e:

            messagebox.showerror(
                "Ошибка",
                str(e)
            )

def toggle_theme():

    global theme

    if theme == DARK_THEME:
        theme = LIGHT_THEME
    else:
        theme = DARK_THEME

    apply_theme()

# =========================================
# APPLY THEME
# =========================================

def apply_theme():

    root.configure(bg=theme["bg"])

    main_canvas.configure(
        bg=theme["bg"]
    )

    scrollable_frame.configure(
        bg=theme["bg"]
    )

    container.configure(
        bg=theme["bg"]
    )

    scrollbar.configure(
        bg=theme["card"],
        troughcolor=theme["bg"],
        activebackground=theme["accent"]
    )

    frames = [
        header_frame,
        input_frame,
        control_frame,
        output_frame,
        bottom_frame
    ]

    for frame in frames:

        frame.configure(
            bg=theme["card"],
            highlightbackground=theme["border"],
            highlightthickness=1
        )

    labels = [
        title_label,
        subtitle_label,
        input_label,
        output_label,
        shift_label
    ]

    for label in labels:

        label.configure(
            bg=theme["card"],
            fg=theme["text"]
        )

    status_label.configure(
        bg=theme["card"],
        fg=theme["success"]
    )

    for box in [input_box, output_box]:

        box.configure(
            bg=theme["entry"],
            fg=theme["text"],
            insertbackground=theme["accent"],
            selectbackground=theme["accent"],
            relief="flat",
            bd=10
        )

    shift_entry.configure(
        bg=theme["entry"],
        fg=theme["text"],
        insertbackground=theme["accent"],
        relief="flat",
        bd=8
    )

    for btn in buttons:

        btn.configure(
            bg=theme["accent"],
            fg="white",
            activebackground=theme["accent_hover"],
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=18,
            pady=12,
            cursor="hand2"
        )

# =========================================
# HEADER
# =========================================

header_frame = tk.Frame(container)

header_frame.pack(
    fill="x",
    padx=120,
    pady=(0, 24)
)

title_label = tk.Label(
    header_frame,
    text="CaesarCipher",
    font=TITLE_FONT
)

title_label.pack(pady=(22, 5))

subtitle_label = tk.Label(
    header_frame,
    text="Шифрование и дешифрование текста методом Цезаря",
    font=SUBTITLE_FONT
)

subtitle_label.pack(pady=(0, 20))

# =========================================
# INPUT FRAME
# =========================================

input_frame = tk.Frame(container)

input_frame.pack(
    fill="both",
    padx=120,
    pady=(0, 12)
)

input_label = tk.Label(
    input_frame,
    text="Исходный текст",
    font=LABEL_FONT
)

input_label.pack(anchor="w", padx=20, pady=(18, 8))

input_box = ScrolledText(
    input_frame,
    height=10,
    wrap="word",
    undo=True,
    font=TEXT_FONT
)

input_box.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=(0, 20)
)
# Smooth scrolling optimization
# =========================================
# CONTROL FRAME
# =========================================

control_frame = tk.Frame(container)

control_frame.pack(
    fill="both",
    padx=120,
    pady=(0, 12)
)

shift_label = tk.Label(
    control_frame,
    text="Ключ сдвига:",
    font=LABEL_FONT
)

shift_label.grid(row=0, column=0, padx=20, pady=20)

shift_entry = tk.Entry(
    control_frame,
    width=10,
    font=TEXT_FONT
)

shift_entry.grid(row=0, column=1)

encrypt_btn = tk.Button(
    control_frame,
    text="🔒 Зашифровать",
    font=BUTTON_FONT,
    command=encrypt_text
)

encrypt_btn.grid(row=0, column=2, padx=10)

decrypt_btn = tk.Button(
    control_frame,
    text="🔓 Дешифровать",
    font=BUTTON_FONT,
    command=decrypt_text
)

decrypt_btn.grid(row=0, column=3, padx=10)

clear_btn = tk.Button(
    control_frame,
    text="🗑 Очистить",
    font=BUTTON_FONT,
    command=clear_fields
)

clear_btn.grid(row=0, column=4, padx=10)
# UI optimization
# =========================================
# OUTPUT FRAME
# =========================================

output_frame = tk.Frame(container)

output_frame.pack(
    fill="both",
    padx=120,
    pady=(0, 12)
)

output_label = tk.Label(
    output_frame,
    text="Результат",
    font=LABEL_FONT
)

output_label.pack(anchor="w", padx=20, pady=(18, 8))

output_box = ScrolledText(
    output_frame,
    height=10,
    wrap="word",
    undo=True,
    font=TEXT_FONT
)

output_box.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=(0, 20)
)

# =========================================
# BOTTOM FRAME
# =========================================

bottom_frame = tk.Frame(container)

bottom_frame.pack(
    fill="both",
    padx=120,
    pady=(0, 20)
)

load_btn = tk.Button(
    bottom_frame,
    text="📂 Загрузить файл",
    font=BUTTON_FONT,
    command=load_file
)

load_btn.grid(row=0, column=0, padx=15, pady=20)

save_btn = tk.Button(
    bottom_frame,
    text="💾 Сохранить",
    font=BUTTON_FONT,
    command=save_file
)

save_btn.grid(row=0, column=1, padx=15)

theme_btn = tk.Button(
    bottom_frame,
    text="🌙 Сменить тему",
    font=BUTTON_FONT,
    command=toggle_theme
)

theme_btn.grid(row=0, column=2, padx=15)

status_label = tk.Label(
    bottom_frame,
    text="✓ Готово к работе",
    font=("Segoe UI", 11, "bold")
)

status_label.grid(row=0, column=3, padx=25)

# =========================================
# BUTTONS LIST
# =========================================

buttons = [
    encrypt_btn,
    decrypt_btn,
    clear_btn,
    load_btn,
    save_btn,
    theme_btn
]

# =========================================
# ENABLE NATIVE SHORTCUTS
# ИСПРАВЛЕНО: заменён весь блок
# =========================================

def bind_shortcuts(widget):
    widget.bind("<Control-c>", lambda e: (widget.event_generate("<<Copy>>"), "break"))
    widget.bind("<Control-v>", lambda e: (widget.event_generate("<<Paste>>"), "break"))
    widget.bind("<Control-x>", lambda e: (widget.event_generate("<<Cut>>"), "break"))
    widget.bind("<Control-z>", lambda e: (widget.event_generate("<<Undo>>"), "break"))
    widget.bind("<Control-y>", lambda e: (widget.event_generate("<<Redo>>"), "break"))
    widget.bind("<Control-a>", lambda e: (
        widget.tag_add("sel", "1.0", "end") if hasattr(widget, 'tag_add')
        else widget.select_range(0, tk.END),
        "break"
    ))

bind_shortcuts(input_box)
bind_shortcuts(output_box)

# Для однострочного поля shift_entry — отдельная обработка
shift_entry.bind("<Control-a>", lambda e: (
    shift_entry.select_range(0, tk.END),
    shift_entry.icursor(tk.END),
    "break"
))
shift_entry.bind("<Control-c>", lambda e: shift_entry.event_generate("<<Copy>>"))
shift_entry.bind("<Control-v>", lambda e: shift_entry.event_generate("<<Paste>>"))
shift_entry.bind("<Control-x>", lambda e: shift_entry.event_generate("<<Cut>>"))

# =========================================
# APPLY THEME
# =========================================

apply_theme()

# =========================================
# START
# =========================================

root.mainloop()