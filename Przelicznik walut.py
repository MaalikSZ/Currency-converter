import tkinter as tk
import requests
from tkinter import ttk
from tkinter import messagebox

class CurrencyConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Przelicznik walut")

        self.currency_data = self.get_currency_data()

        self.from_currency_var = tk.StringVar()
        self.from_currency_var.set("USD")

        self.to_currency_var = tk.StringVar()
        self.to_currency_var.set("EUR")

        self.amount_var = tk.StringVar()

        self.result_var = tk.StringVar()

        self.from_currency_label = tk.Label(self, text="Przelicz z waluty:")
        self.from_currency_label.pack()
        self.from_currency_option = ttk.Combobox(self, textvariable=self.from_currency_var, values=list(self.currency_data.keys()), state="readonly")
        self.from_currency_option.pack(pady=5)

        self.to_currency_label = tk.Label(self, text="na walutę:")
        self.to_currency_label.pack()
        self.to_currency_option = ttk.Combobox(self, textvariable=self.to_currency_var, values=list(self.currency_data.keys()), state="readonly")
        self.to_currency_option.pack(pady=5)

        self.amount_label = tk.Label(self, text="Podaj kwotę do przeliczenia:")
        self.amount_label.pack()
        self.amount_entry = tk.Entry(self, textvariable=self.amount_var)
        self.amount_entry.pack(pady=5)

        self.convert_button = tk.Button(self, text="Przelicz", command=self.convert_currency)
        self.convert_button.pack(pady=5)

        self.result_label = tk.Label(self, text="Wynik:")
        self.result_label.pack()
        self.result_value = tk.Label(self, textvariable=self.result_var, font=("Arial", 14, "bold"))
        self.result_value.pack()

        self.refresh_button = tk.Button(self, text="Odśwież", command=self.refresh_currency_data)
        self.refresh_button.pack(pady=5)

        self.style = ttk.Style(self)
        self.style.configure("TLabel", font=("Arial", 12))

        self.configure(bg="#F0F0F0")

        self.amount_entry.focus()

        self.add_copyright_label()

    def get_currency_data(self):
        try:
            response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
            data = response.json()
            return data["rates"]
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Nie udało się pobrać danych waluty:\n{e}")
            self.quit()

    def refresh_currency_data(self):
        try:
            self.currency_data = self.get_currency_data()
            self.from_currency_option["values"] = list(self.currency_data.keys())
            self.to_currency_option["values"] = list(self.currency_data.keys())
            self.result_var.set("")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Nie udało się odświeżyć danych waluty:\n{e}")

    def convert_currency(self):
        from_currency = self.from_currency_var.get()
        to_currency = self.to_currency_var.get()
        amount = self.amount_var.get()

        if not amount:
            messagebox.showwarning("Uwaga", "Wprowadź prawidłową kwotę.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showwarning("Uwaga", "Wprowadź prawidłową kwotę numeryczną.")
            return

        if from_currency != "USD":
            amount = amount / self.currency_data[from_currency]

        result = round(amount * self.currency_data[to_currency], 2)
        self.result_var.set(f"{result:,}")

        self.amount_entry.delete(0, tk.END)

    def add_copyright_label(self):
        copyright_text = "© 2023 Szymon Wasik."
        copyright_label = tk.Label(self, text=copyright_text, font=("Arial", 10), fg="gray")
        copyright_label.pack(side="bottom", pady=5)

if __name__ == "__main__":
    app = CurrencyConverterApp()
    app.mainloop()