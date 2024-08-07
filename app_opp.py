"""app_opp.py"""

import tkinter as tk
from tkinter import messagebox
import requests
import json
import os

class JsonPlaceholderFetcher:
    def __init__(self, root):
        self.root = root
        self.root.title("JSON Placeholder Fetcher")

        self.create_widgets()
    
    def create_widgets(self):
        tk.Label(self.root, text="Enter ID:").grid(row=0, column=0, padx=10, pady=10)
        self.entry = tk.Entry(self.root)
        self.entry.grid(row=0, column=1, padx=10, pady=10)

        fetch_button = tk.Button(self.root, text="Fetch Data", command=self.fetch_data)
        fetch_button.grid(row=0, column=2, padx=10, pady=10)

        self.text_area = tk.Text(self.root, width=50, height=20)
        self.text_area.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        self.save_button = tk.Button(self.root, text="Save Data", command=self.save_data, state=tk.DISABLED)
        self.save_button.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
    
    def fetch_data(self):
        user_id = self.entry.get()
        if not user_id.isdigit():
            messagebox.showerror("Invalid Input", "Please enter a valid numeric ID.")
            return

        try:
            response = requests.get(f"https://jsonplaceholder.typicode.com/todos/{user_id}")
            response.raise_for_status()
            data = response.json()
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, json.dumps(data, indent=4))
            self.save_button.config(state=tk.NORMAL)
        except requests.RequestException as e:
            messagebox.showerror("Error", f"Failed to fetch data: {e}")
    
    def save_data(self):
        data = self.text_area.get(1.0, tk.END).strip()
        if data:
            folder_path = './json_files'
            file_name = f'todo_{self.entry.get()}.json'
            os.makedirs(folder_path, exist_ok=True)
            file_path = os.path.join(folder_path, file_name)
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(data)
                messagebox.showinfo("Success", f"Data saved to {file_path}")
            except IOError as e:
                messagebox.showerror("Error", f"Failed to save data: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = JsonPlaceholderFetcher(root)
    root.mainloop()
