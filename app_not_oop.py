"""app_not_oop.py"""

import tkinter as tk
from tkinter import messagebox
import requests
import json
import os

def fetch_data():
    user_id = entry.get()
    if not user_id.isdigit():
        messagebox.showerror("Invalid Input", "Please enter a valid numeric ID.")
        return

    try:
        response = requests.get(f"https://jsonplaceholder.typicode.com/todos/{user_id}")
        response.raise_for_status()
        data = response.json()
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, json.dumps(data, indent=4))
        save_button.config(state=tk.NORMAL)
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch data: {e}")

def save_data():
    data = text_area.get(1.0, tk.END).strip()
    if data:
        folder_path = './json_files'
        file_name = f'todo_{entry.get()}.json'
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, file_name)
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(data)
            messagebox.showinfo("Success", f"Data saved to {file_path}")
        except IOError as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")

root = tk.Tk()
root.title("JSON Placeholder Fetcher")

tk.Label(root, text="Enter ID:").grid(row=0, column=0, padx=10, pady=10)
entry = tk.Entry(root)
entry.grid(row=0, column=1, padx=10, pady=10)

fetch_button = tk.Button(root, text="Fetch Data", command=fetch_data)
fetch_button.grid(row=0, column=2, padx=10, pady=10)

text_area = tk.Text(root, width=50, height=20)
text_area.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

save_button = tk.Button(root, text="Save Data", command=save_data, state=tk.DISABLED)
save_button.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()
