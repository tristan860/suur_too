import tkinter as tk
from tkinter import messagebox
import csv

class InvoiceApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Arvete Haldamine")

        # Teenuste andmete hoidmine
        self.services = []

        # Arvete andmete hoidmine
        self.invoices = []

        # Kasutajaliides
        self.create_gui()

    def create_gui(self):
        # Teenuste haldamine
        tk.Label(self.master, text="Teenused").grid(row=0, column=0, padx=10, pady=10)
        self.services_listbox = tk.Listbox(self.master, selectmode=tk.SINGLE)
        self.services_listbox.grid(row=0, column=1, padx=10, pady=10)

        tk.Button(self.master, text="Lisa Teenus", command=self.add_service).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(self.master, text="Muuda Teenust", command=self.edit_service).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(self.master, text="Kustuta Teenus", command=self.delete_service).grid(row=1, column=2, padx=10, pady=10)

        # Arvete haldamine
        tk.Label(self.master, text="Arved").grid(row=2, column=0, padx=10, pady=10)
        self.invoices_listbox = tk.Listbox(self.master, selectmode=tk.SINGLE)
        self.invoices_listbox.grid(row=2, column=1, padx=10, pady=10)

        tk.Button(self.master, text="Koosta Arve", command=self.create_invoice).grid(row=3, column=0, padx=10, pady=10)
        tk.Button(self.master, text="Muuda Arvet", command=self.edit_invoice).grid(row=3, column=1, padx=10, pady=10)
        tk.Button(self.master, text="Kustuta Arve", command=self.delete_invoice).grid(row=3, column=2, padx=10, pady=10)

        # Lae teenused ja arved failist
        self.load_data()

    def add_service(self):
        # Looge dialoog teenuse lisamiseks
        service_dialog = ServiceDialog(self.master)
        self.master.wait_window(service_dialog.top)

        # Lisa teenus teenuste nimekirja
        if service_dialog.result:
            self.services.append((service_dialog.result[0], float(service_dialog.result[1])))
            self.services_listbox.insert(tk.END, service_dialog.result[0])
            self.save_data()

    def edit_service(self):
        # Kontrolli, kas on valitud teenus
        selected_index = self.services_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Hoiatus", "Palun vali teenus, mida muuta.")
            return

        # Hangi valitud teenuse andmed
        selected_service = self.services[selected_index[0]]

        # Looge dialoog teenuse muutmiseks
        service_dialog = ServiceDialog(self.master, data=selected_service)
        self.master.wait_window(service_dialog.top)

        # Uuenda teenuse andmeid
        if service_dialog.result:
            self.services[selected_index[0]] = (service_dialog.result[0], float(service_dialog.result[1]))
            self.services_listbox.delete(selected_index[0])
            self.services_listbox.insert(selected_index[0], service_dialog.result[0])
            self.save_data()

    def delete_service(self):
        # Kontrolli, kas on valitud teenus
        selected_index = self.services_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Hoiatus", "Palun vali teenus, mida kustutada.")
            return

        # Kustuta teenus teenuste nimekirjast
        del_service = self.services.pop(selected_index[0])
        self.services_listbox.delete(selected_index[0])
        messagebox.showinfo("Teenus Kustutatud", f"Teenuse '{del_service[0]}' on edukalt kustutatud.")
        self.save_data()

    def create_invoice(self):
        # Kontrolli, kas on valitud teenused arve loomiseks
        selected_services_index = self.services_listbox.curselection()
        if not selected_services_index:
            messagebox.showwarning("Hoiatus", "Palun vali teenused, mida arvele lisada.")
            return

        # Hangi valitud teenuste andmed ja muuda hindade tüüp float-ks
        selected_services = [(service[0], float(service[1])) for service in [self.services[index] for index in selected_services_index]]

        # Kalkuleeri arve summa
        total_amount = sum([service[1] for service in selected_services])

        # Looge arve
        invoice_number = len(self.invoices) + 1
        invoice = (invoice_number, selected_services, total_amount)
        self.invoices.append(invoice)
        self.invoices_listbox.insert(tk.END, f"Arve {invoice_number}")
        self.save_data()

    def edit_invoice(self):
        # Kontrolli, kas on valitud arve
        selected_index = self.invoices_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Hoiatus", "Palun vali arve, mida muuta.")
            return

        # Hangi valitud arve andmed
        selected_invoice = self.invoices[selected_index[0]]

        # Looge dialoog arve muutmiseks
        invoice_dialog = InvoiceDialog(self.master, services=self.services, data=selected_invoice)
        self.master.wait_window(invoice_dialog.top)

        # Uuenda arve andmeid
        if invoice_dialog.result:
            self.invoices[selected_index[0]] = invoice_dialog.result
            self.invoices_listbox.delete(selected_index[0])
            self.invoices_listbox.insert(selected_index[0], f"Arve {invoice_dialog.result[0]}")
            self.save_data()

    def delete_invoice(self):
        # Kontrolli, kas on valitud arve
        selected_index = self.invoices_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Hoiatus", "Palun vali arve, mida kustutada.")
            return

        # Kustuta arve arvete nimekirjast
        del_invoice = self.invoices.pop(selected_index[0])
        self.invoices_listbox.delete(selected_index[0])
        messagebox.showinfo("Arve Kustutatud", f"Arve {del_invoice[0]} on edukalt kustutatud.")
        self.save_data()

    def save_data(self):
        # Salvesta teenused ja arved faili (CSV-vormingus)
        with open("services.csv", mode="w", newline="") as services_file:
            services_writer = csv.writer(services_file)
            services_writer.writerows(self.services)

        with open("invoices.csv", mode="w", newline="") as invoices_file:
            invoices_writer = csv.writer(invoices_file)
            invoices_writer.writerows(self.invoices)

    def load_data(self):
        # Lae teenused failist
        try:
            with open("services.csv", mode="r") as services_file:
                services_reader = csv.reader(services_file)
                self.services = [(row[0], float(row[1])) for row in services_reader]
                for service in self.services:
                    self.services_listbox.insert(tk.END, service[0])
        except FileNotFoundError:
            pass

        # Lae arved failist
        try:
            with open("invoices.csv", mode="r") as invoices_file:
                invoices_reader = csv.reader(invoices_file)
                self.invoices = [(int(row[0]), [(s[0], float(s[1])) for s in eval(row[1])], float(row[2])) for row in invoices_reader]
                for invoice in self.invoices:
                    self.invoices_listbox.insert(tk.END, f"Arve {invoice[0]}")
        except FileNotFoundError:
            pass

class ServiceDialog:
    def __init__(self, parent, data=None):
        self.top = tk.Toplevel(parent)
        self.top.title("Teenuse Lisamine")

        # Teenuse andmed (nimi, hind)
        self.name_var = tk.StringVar()
        self.price_var = tk.DoubleVar()  # Muuda see DoubleVar-iks

        # Kui muudetakse olemasolevat teenust, täida väljad olemasolevate andmetega
        if data:
            self.top.title("Teenuse Muutmine")
            self.name_var.set(data[0])
            self.price_var.set(float(data[1]))  # Muuda hind float-ks

        # Kasutajaliides
        tk.Label(self.top, text="Teenuse Nimi:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(self.top, textvariable=self.name_var).grid(row=0, column=1, padx=10, pady=10)
        tk.Label(self.top, text="Teenuse Hind:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(self.top, textvariable=self.price_var).grid(row=1, column=1, padx=10, pady=10)

        tk.Button(self.top, text="Salvesta", command=self.save).grid(row=2, column=0, columnspan=2, pady=10)

        self.result = None

    def save(self):
        # Kontrolli, kas mõlemad väljad on täidetud
        if not self.name_var.get() or not self.price_var.get():
            messagebox.showwarning("Hoiatus", "Palun täida kõik väljad enne salvestamist.")
            return

        # Salvesta teenuse andmed
        self.result = (self.name_var.get(), self.price_var.get())  # Jäta hind DoubleVar-iks
        self.top.destroy()

class InvoiceDialog:
    def __init__(self, parent, services, data=None):
        self.top = tk.Toplevel(parent)
        self.top.title("Arve Muutmine")

        # Teenused ja valitud teenused
        self.services = services
        self.selected_services = []

        # Arve andmed (number, teenused, summa)
        self.number_var = tk.StringVar()
        self.number_var.set("Automaatne")
        self.total_amount_var = tk.StringVar()

        # Kontrolli, kas muudetakse olemasolevat arvet
        if data:
            self.top.title("Arve Muutmine")
            self.number_var.set(data[0])
            self.selected_services = data[1]
            self.total_amount_var.set(data[2])

        # Kasutajaliides
        tk.Label(self.top, text="Arve Number:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(self.top, textvariable=self.number_var, state=tk.DISABLED).grid(row=0, column=1, padx=10, pady=10)
        tk.Label(self.top, text="Vali Teenused:").grid(row=1, column=0, padx=10, pady=10)
        self.services_listbox = tk.Listbox(self.top, selectmode=tk.MULTIPLE, height=5)
        self.services_listbox.grid(row=1, column=1, padx=10, pady=10)

        # Lae teenused listboxi
        for service in self.services:
            self.services_listbox.insert(tk.END, service[0])

        tk.Label(self.top, text="Arve Summa:").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(self.top, textvariable=self.total_amount_var, state=tk.DISABLED).grid(row=2, column=1, padx=10, pady=10)

        tk.Button(self.top, text="Arvuta Summa", command=self.calculate_total).grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(self.top, text="Salvesta", command=self.save).grid(row=4, column=0, columnspan=2, pady=10)

        # Vali teenused, kui muudetakse olemasolevat arvet
        for index, service in enumerate(self.services):
            if service in self.selected_services:
                self.services_listbox.select_set(index)

    def calculate_total(self):
        # Kalkuleeri valitud teenuste summa
        selected_indices = self.services_listbox.curselection()
        selected_services = [self.services[index] for index in selected_indices]

        try:
            # Muuda teenuste hindu ujukomaarvudeks enne summeerimist
            total_amount = sum([float(service[1]) for service in selected_services])
        except ValueError:
            messagebox.showwarning("Hoiatus", "Teenuste hindade muutmine numbrilisteks väärtusteks ebaõnnestus.")
            return

        # Näita arve summat
        self.total_amount_var.set(total_amount)

    def save(self):
        # Kontrolli, kas teenused on valitud
        selected_indices = self.services_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Hoiatus", "Palun vali teenused, mida arvele lisada.")
            return

        # Hangi valitud teenuste andmed
        selected_services = [self.services[index] for index in selected_indices]

        # Kalkuleeri arve summa
        total_amount = sum([service[1] for service in selected_services])

        # Salvesta arve andmed
        if self.number_var.get() == "Automaatne":
            invoice_number = len(app.invoices) + 1
        else:
            invoice_number = int(self.number_var.get())

        self.result = (invoice_number, selected_services, total_amount)
        self.top.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = InvoiceApp(root)
    root.mainloop()
