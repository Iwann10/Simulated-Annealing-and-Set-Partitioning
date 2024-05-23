import tkinter as tk
from tkinter import ttk
import subprocess

# Function to run the SimAnneal.py script
def run_simulated_annealing():
    script_path = r"D:\PUK\Honiers\ITRI 671\Coding\SimAnneal.py"
    subprocess.Popen(["python", script_path])

# Function to run the SetPartitioning.py script
def run_set_partitioning():
    script_path = r"D:\PUK\Honiers\ITRI 671\Coding\SetPartitioning.py"
    subprocess.Popen(["python", script_path])

# Main window setup
root = tk.Tk()
root.title("Solutions to TSP and VRP")
root.geometry("300x200")

# Heading label
heading_label = ttk.Label(root, text="Solutions to TSP and VRP", font=("Helvetica", 16))
heading_label.pack(pady=10)

# Simulated Annealing button
sa_button = ttk.Button(root, text="Simulated Annealing", command=run_simulated_annealing)
sa_button.pack(pady=10)

# Set Partitioning button
sp_button = ttk.Button(root, text="Set Partitioning", command=run_set_partitioning)
sp_button.pack(pady=10)

# Start the main loop
root.mainloop()
