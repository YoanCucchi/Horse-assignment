import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

def update_widgets_visibility(*args):
	if edit_mode.get() == "Cavalier":
		day_label.grid(row=3, column=0)
		day_options.grid(row=3, column=1, sticky="nsew")
		slot_label.grid(row=4, column=0)
		slot_options.grid(row=4, column=1, sticky="nsew")
	else:
		day_label.grid_forget()
		day_options.grid_forget()
		slot_label.grid_forget()
		slot_options.grid_forget()

def create_file_if_not_exists(file):
	if not os.path.exists(file):
		with open(file, 'w') as f:
			pass

def read_file(file):
	with open(file, 'r') as f:
		content = f.readlines()
	content = [x.strip().split(',') for x in content if x.strip()]
	return content

def write_file(file, data):
	with open(file, 'w') as f:
		for line in data:
			f.write(','.join(line) + '\n')

def update_age_size_options(*args):
	if edit_mode.get() == "Cheval":
		age_size_options['values'] = ("Petit", "Moyen", "Moyen/Grand", "Grand")
	else:
		age_size_options['values'] = ("Petit", "Moyen", "Moyen/Grand", "Grand")

def add_entry():
	name = name_entry.get()
	age_size = age_size_var.get()

	if edit_mode.get() == "Cheval":
		if not name or not age_size:
			messagebox.showwarning("Erreur", "Veuillez remplir tous les champs.")
			return
	else:
		day = day_var.get()
		slot = slot_var.get()
		if not name or not age_size or not day or not slot:
			messagebox.showwarning("Erreur", "Veuillez remplir tous les champs.")
			return

	data = chevaux_data if edit_mode.get() == "Cheval" else cavaliers_data

	for line in data:
		if line[0] == name:
			if edit_mode.get() == "Cheval":
				if line[1:] == [age_size]:
					messagebox.showwarning("Erreur", f"{name} existe déjà avec les mêmes informations.")
					return
				else:
					line[1:] = [age_size]
					messagebox.showinfo("Mise à jour", f"Les informations pour {name} ont été mises à jour.")
					break
			else:
				if line[1:] == [age_size, day, slot]:
					messagebox.showwarning("Erreur", f"{name} existe déjà avec les mêmes informations.")
					return
				else:
					line[1:] = [age_size, day, slot]
					messagebox.showinfo("Mise à jour", f"Les informations pour {name} ont été mises à jour.")
					break
	else:
		if edit_mode.get() == "Cheval":
			data.append([name, age_size])
		else:
			data.append([name, age_size, day, slot])
		messagebox.showinfo("Ajout", f"{name} a été ajouté avec succès.")

	write_file(chevaux_file if edit_mode.get() == "Cheval" else cavaliers_file, data)


app = tk.Tk()
app.title("Éditeur Cheval/Cavalier")

# Configuration des lignes et colonnes pour qu'elles s'étendent proportionnellement
for i in range(6):
	app.grid_rowconfigure(i, weight=1)

for j in range(2):
	app.grid_columnconfigure(j, weight=1)

edit_mode = tk.StringVar()
edit_mode.set("Cheval")
edit_mode.trace("w", update_age_size_options)
edit_mode.trace("w", update_widgets_visibility)

chevaux_file = "chevaux.txt"
cavaliers_file = "cavaliers.txt"

# Créer les fichiers s'ils n'existent pas
create_file_if_not_exists(chevaux_file)
create_file_if_not_exists(cavaliers_file)

chevaux_data = read_file(chevaux_file)
cavaliers_data = read_file(cavaliers_file)

tk.Label(app, text="Mode d'édition :").grid(row=0, column=0)
tk.OptionMenu(app, edit_mode, "Cheval", "Cavalier").grid(row=0, column=1)

tk.Label(app, text="Nom :").grid(row=1, column=0)
name_entry = tk.Entry(app)
name_entry.grid(row=1, column=1, sticky="nsew")

tk.Label(app, text="Âge/Taille :").grid(row=2, column=0)
age_size_var = tk.StringVar()
age_size_options = ttk.Combobox(app, textvariable=age_size_var, state="readonly")
age_size_options.grid(row=2, column=1, sticky="nsew")
update_age_size_options()

day_label = tk.Label(app, text="Jour :")
tk.Label(app, text="Jour :").grid(row=3, column=0)
day_var = tk.StringVar()
day_options = ttk.Combobox(app, textvariable=day_var, state="readonly", values=("Mercredi", "Samedi"))
day_options.grid(row=3, column=1, sticky="nsew")

slot_label = tk.Label(app, text="Créneau :")  # Ajout de la variable slot_label
tk.Label(app, text="Créneau :").grid(row=4, column=0)
slot_var = tk.StringVar()
slot_options = ttk.Combobox(app, textvariable=slot_var, state="readonly", values=("10H Céline", "10H Julien", "11H15 Céline", "11H15 Julien", "14H Céline", "14H Julien", "15H15 Céline", "15H15 Julien", "16H30 Céline", "16H30 Julien"))
slot_options.grid(row=4, column=1, sticky="nsew")

tk.Button(app, text="Ajouter/Mettre à jour", command=add_entry).grid(row=5, column=0, columnspan=2, sticky="nsew")
update_widgets_visibility()
app.mainloop()
