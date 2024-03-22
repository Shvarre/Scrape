import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import html
from datetime import datetime
from urllib.parse import urlparse
import os

def afspil_lyd():
    for _ in range(5):
        os.system('aplay /usr/share/sounds/speech-dispatcher/test.wav')  # Erstat med stien til din foretrukne alarmlyd

def hent_indhold(source):
    if urlparse(source).scheme in ('http', 'https'):
        try:
            response = requests.get(source)
            soup = BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            messagebox.showerror("Fejl", str(e))
            return None
    else:
        try:
            with open(source, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'html.parser')
        except FileNotFoundError:
            messagebox.showerror("Fejl", "Filen blev ikke fundet.")
            return None

    dd_tag = soup.find('dd', class_='col-9')
    return html.unescape(dd_tag.text.strip()) if dd_tag else None

def overvaag_kilde():
    if overvaag_kilde.running:
        current_content = hent_indhold(kilde_entry.get())
        if current_content is not None:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            output_felt.insert(tk.END, f"{timestamp}: {current_content}\n")
            
            if overvaag_kilde.initialized and current_content != overvaag_kilde.previous_content:
                afspil_lyd()
                messagebox.showinfo("Ændring Detekteret", "Indholdet har ændret sig!")
            
            overvaag_kilde.previous_content = current_content
        
        overvaag_kilde.initialized = True
        root.after(30000, overvaag_kilde)  # Check hver 30 sekunder
    else:
        status_label.config(text="Status: Stoppet")

def start_overvaagning():
    overvaag_kilde.running = True
    status_label.config(text="Status: Kører")
    overvaag_kilde()

def stop_overvaagning():
    overvaag_kilde.running = False
    status_label.config(text="Status: Stoppet")

overvaag_kilde.previous_content = None
overvaag_kilde.initialized = False
overvaag_kilde.running = False

root = tk.Tk()
root.title("Kilde Overvågning")

kilde_label = tk.Label(root, text="URL eller Fil Sti:")
kilde_label.pack()
kilde_entry = tk.Entry(root)
kilde_entry.pack()

start_button = tk.Button(root, text="Start Overvågning", command=start_overvaagning)
start_button.pack()

stop_button = tk.Button(root, text="Stop Overvågning", command=stop_overvaagning)
stop_button.pack()

output_label = tk.Label(root, text="Aktuelt Indhold og Tidspunkter for Check:")
output_label.pack()
output_felt = ScrolledText(root, height=10)
output_felt.pack()

status_label = tk.Label(root, text="Status: Ikke startet")
status_label.pack()

root.mainloop()
