import tkinter as tk
from tkinter import messagebox
import random
import string
import secrets

def create_word_inputs():
    try:
        count = int(word_count_entry.get())
    except:
        messagebox.showerror("Error", "Enter a valid number of words!")
        return

    for widget in word_frame.winfo_children():
        widget.destroy()

    global word_entries
    word_entries = []

    for i in range(count):
        tk.Label(word_frame, text=f"Word {i+1}:").pack()
        entry = tk.Entry(word_frame)
        entry.pack()
        word_entries.append(entry)

def clean_word(word):
    return word.replace(" ", "").capitalize()  # remove spaces

def mix_words(words):
    mixed = ""
    for word in words:
        if len(word) > 2:
            split = random.randint(1, len(word)-1)
            mixed += word[:split]
            mixed = mixed[::-1]  # slight twist
            mixed += word[split:]
        else:
            mixed += word
    return mixed

def generate_password():
    try:
        length = int(length_entry.get())
    except:
        messagebox.showerror("Error", "Enter valid password length!")
        return

    if length < 6:
        messagebox.showerror("Error", "Length should be at least 6!")
        return

    words = []
    for entry in word_entries:
        word = entry.get().strip().replace(" ", "")
        if not word:
            messagebox.showerror("Error", "Fill all word fields!")
            return
        words.append(word.capitalize())

    # Step 1: Slight clean split (NOT messy)
    structured_words = []
    for word in words:
        if len(word) > 4:
            split = len(word) // 2
            structured_words.append(word[:split])
            structured_words.append(word[split:])
        else:
            structured_words.append(word)

    # Step 2: Insert number + symbol BETWEEN words
    number = str(random.randint(10, 99)) if var_digits.get() else ""
    special = random.choice("!@#$%") if var_symbols.get() else ""

    password = ""

    for i, part in enumerate(structured_words):
        password += part
        if i == 0 and number:   # insert after first part
            password += number
        if i == 1 and special:  # insert after second part
            password += special

    # Step 3: Fill remaining length (light, not messy)
    remaining = length - len(password)

    if remaining > 0:
        characters = ""
        if var_lower.get():
            characters += string.ascii_lowercase
        if var_upper.get():
            characters += string.ascii_uppercase

        if not characters:
            characters = string.ascii_lowercase

        for _ in range(remaining):
            password += secrets.choice(characters)

    output_var.set(password[:length])
    
def copy_to_clipboard():
    password = output_var.get()
    if not password:
        messagebox.showwarning("Warning", "No password to copy!")
        return

    root.clipboard_clear()
    root.clipboard_append(password)
    root.update()
    messagebox.showinfo("Copied", "Password copied to clipboard!")

# GUI setup
root = tk.Tk()
root.title("Advanced Password Generator")
root.geometry("400x600")

tk.Label(root, text="Password Length:").pack()
length_entry = tk.Entry(root)
length_entry.pack()

tk.Label(root, text="How many words do you want?").pack()
word_count_entry = tk.Entry(root)
word_count_entry.pack()

tk.Button(root, text="Create Word Fields", command=create_word_inputs).pack(pady=5)

word_frame = tk.Frame(root)
word_frame.pack()

tk.Label(root, text="Select Character Types:").pack(pady=5)

var_upper = tk.IntVar()
var_lower = tk.IntVar()
var_digits = tk.IntVar()
var_symbols = tk.IntVar()

tk.Checkbutton(root, text="Uppercase (A-Z)", variable=var_upper).pack()
tk.Checkbutton(root, text="Lowercase (a-z)", variable=var_lower).pack()
tk.Checkbutton(root, text="Numbers (0-9)", variable=var_digits).pack()
tk.Checkbutton(root, text="Symbols (only one)", variable=var_symbols).pack()

tk.Button(root, text="Generate Password", command=generate_password).pack(pady=10)

output_var = tk.StringVar()
tk.Entry(root, textvariable=output_var, width=30).pack(pady=5)

tk.Button(root, text="Copy Password 📋", command=copy_to_clipboard).pack(pady=5)

root.mainloop()