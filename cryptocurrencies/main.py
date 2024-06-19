import tkinter as tk
from tkinter import filedialog, messagebox
import os
import pandas as pd
import requests

class CryptoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Crypto Info Generator")
        self.root.geometry("400x200")

        self.upload_button = tk.Button(root, text="Upload File", command=self.upload_file)
        self.upload_button.pack(pady=10)

        self.filename_label = tk.Label(root, text="No file selected")
        self.filename_label.pack(pady=5)

        self.name_entry = tk.Entry(root, width=50)
        self.name_entry.pack(pady=10)
        self.name_entry.insert(0, "Enter output Excel file name")

        self.save_button = tk.Button(root, text="Save File", command=self.save_file)
        self.save_button.pack(pady=10)

        self.filepath = ""
        self.symbols = []

    def upload_file(self):
        self.filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if self.filepath:
            self.filename_label.config(text=os.path.basename(self.filepath))
            with open(self.filepath, 'r') as file:
                self.symbols = file.read().strip().split()
            messagebox.showinfo("File Uploaded", "Symbols loaded successfully")

    def save_file(self):
        if not self.filepath:
            messagebox.showerror("Error", "Please upload a file first")
            return
        
        output_dir = filedialog.askdirectory(initialdir=os.path.expanduser('~/Downloads'))
        if not output_dir:
            return

        output_filename = self.name_entry.get()
        if not output_filename.endswith('.xlsx'):
            output_filename += '.xlsx'
        
        output_path = os.path.join(output_dir, output_filename)
        
        crypto_data = self.fetch_crypto_data(self.symbols)
        if crypto_data:
            df = pd.DataFrame(crypto_data)
            df.to_excel(output_path, index=False)
            messagebox.showinfo("Success", f"File saved successfully at {output_path}")
        else:
            messagebox.showerror("Error", "Failed to fetch cryptocurrency data")

    def fetch_crypto_data(self, symbols):
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "ids": ",".join(symbols)
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            crypto_data = []
            for item in data:
                crypto_data.append({
                    "Name": item.get("name"),
                    "Symbol": item.get("symbol"),
                    "Current Price": item.get("current_price"),
                    "Market Cap": item.get("market_cap"),
                    "Total Volume": item.get("total_volume"),
                    "Price Change (24h)": item.get("price_change_percentage_24h")
                })
            return crypto_data
        else:
            return None

if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoApp(root)
    root.mainloop()
