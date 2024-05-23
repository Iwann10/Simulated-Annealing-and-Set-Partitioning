import tkinter as tk
from tkinter import ttk
import random
import math
import threading
import pickle
from PIL import Image, ImageTk, ImageDraw

# Load coordinates and distance matrix
with open('coordinates.pkl', 'rb') as f:
    coordinates = pickle.load(f)

with open('distance_matrix.pkl', 'rb') as f:
    distance_matrix = pickle.load(f)

# Load the map image
map_img_path = "D:/PUK/Honiers/ITRI 671/Coding/MapForTSP.png"
map_img = Image.open(map_img_path)

# Resize the map image to fit within the GUI window while maintaining aspect ratio
max_width, max_height = 1000, 800
map_img.thumbnail((max_width, max_height), Image.LANCZOS)
map_img_width, map_img_height = map_img.size

# Map scale: 5 km per cm
km_per_cm = 5
cm_per_pixel = 0.026458333  # 1 inch / 96 dpi * 2.54 cm/inch
km_per_pixel = km_per_cm * cm_per_pixel

# Reference point on the map (latitude, longitude)
ref_lat, ref_lon = coordinates[0]

# Adjusting the map center to move the first location
# 2.5 cm up and 1 cm to the left
ref_x = int(map_img_width // 2 - 1 / cm_per_pixel)
ref_y = int(map_img_height // 2 - 2.5 / cm_per_pixel)

# Convert coordinates to pixel positions
def coord_to_pixel(lat, lon):
    # Assuming a simple linear transformation for this example
    lat_scale = 111.32  # kilometers per degree latitude
    lon_scale = 111.32 * math.cos(math.radians(ref_lat))  # kilometers per degree longitude

    dx = (lon - ref_lon) * lon_scale
    dy = (lat - ref_lat) * lat_scale

    pixel_x = int(ref_x + dx / km_per_pixel)
    pixel_y = int(ref_y - dy / km_per_pixel)  # Invert y-axis for image coordinates
    return pixel_x, pixel_y

# Default stopping temperature
STOPPING_TEMPERATURE = 1
stop_event = threading.Event()

def simulated_annealing(distance_matrix, initial_temp, stopping_temp, temp_decay):
    def calculate_total_distance(path):
        return sum(distance_matrix[path[i-1]][path[i]] for i in range(len(path)))

    def get_neighbor(path):
        a, b = random.sample(range(len(path)), 2)
        path[a], path[b] = path[b], path[a]
        return path

    num_cities = len(distance_matrix)
    current_path = list(range(num_cities))
    random.shuffle(current_path)
    current_distance = calculate_total_distance(current_path)
    best_path = list(current_path)
    best_distance = current_distance

    temp = initial_temp

    while temp > stopping_temp and not stop_event.is_set():
        new_path = get_neighbor(list(current_path))
        new_distance = calculate_total_distance(new_path)

        if new_distance < current_distance or random.random() < math.exp((current_distance - new_distance) / temp):
            current_path = new_path
            previous_distance = current_distance
            current_distance = new_distance

            if new_distance < best_distance:
                best_path = new_path
                best_distance = new_distance

        temp *= temp_decay  # Gradually reduce the temperature
        yield best_path, best_distance, current_distance, previous_distance, temp

# Function to handle the start of the simulated annealing process in a separate thread
def start_simulated_annealing_thread():
    initial_temp = float(initial_temp_entry.get())
    temp_decay = float(temp_decay_entry.get())
    stop_event.clear()
    thread = threading.Thread(target=run_simulated_annealing, args=(initial_temp, temp_decay))
    thread.start()

# Function to handle stopping the simulated annealing process
def stop_simulated_annealing():
    stop_event.set()

def run_simulated_annealing(initial_temp, temp_decay):
    for best_path, best_distance, current_distance, previous_distance, temp in simulated_annealing(distance_matrix, initial_temp, STOPPING_TEMPERATURE, temp_decay):
        if stop_event.is_set():
            break
        result_label.config(text=f"Best Distance: {best_distance:.2f} meters\nCurrent Distance: {current_distance:.2f} meters\nPrevious Distance: {previous_distance:.2f} meters\nCurrent Temp: {temp:.2f}")
        update_plot(best_path, distance_matrix)
        root.update_idletasks()

# Function to update the plot
def update_plot(path, distance_matrix):
    img_copy = map_img.copy()
    draw = ImageDraw.Draw(img_copy)
    
    for i in range(len(path)):
        x1, y1 = coord_to_pixel(coordinates[path[i]][0], coordinates[path[i]][1])
        x2, y2 = coord_to_pixel(coordinates[path[(i+1) % len(path)]][0], coordinates[path[(i+1) % len(path)]][1])
        draw.line((x1, y1, x2, y2), fill="green", width=2)  # Draw lines between points
        draw.ellipse((x1-3, y1-3, x1+3, y1+3), fill="red", outline="red")  # Draw points
        draw.text((x1, y1), f"Loc {path[i]}", fill="white")

    img_tk = ImageTk.PhotoImage(img_copy)
    map_label.config(image=img_tk)
    map_label.image = img_tk

# Create the main window
root = tk.Tk()
root.title("Simulated Annealing")
root.geometry("1200x800")

# Input for initial temperature
ttk.Label(root, text="Initial Temperature:").pack(pady=5)
initial_temp_entry = ttk.Entry(root)
initial_temp_entry.pack(pady=5)

# Input for cooling rate
ttk.Label(root, text="Cooling Rate:").pack(pady=5)
temp_decay_entry = ttk.Entry(root)
temp_decay_entry.pack(pady=5)

# Start button
start_button = ttk.Button(root, text="Start Simulated Annealing", command=start_simulated_annealing_thread)
start_button.pack(pady=5)

# Stop button
stop_button = ttk.Button(root, text="Stop Simulated Annealing", command=stop_simulated_annealing)
stop_button.pack(pady=5)

# Result label
result_label = ttk.Label(root, text="", font=("Helvetica", 14))
result_label.pack(pady=20)

# Map label for displaying the image
map_label = ttk.Label(root)
map_label.pack(pady=20)

# Display the initial map with the first point
def display_initial_map():
    img_copy = map_img.copy()
    draw = ImageDraw.Draw(img_copy)
    
    x, y = coord_to_pixel(coordinates[0][0], coordinates[0][1])
    draw.ellipse((x-3, y-3, x+3, y+3), fill="red", outline="red")  # Draw initial point
    draw.text((x, y), "Loc 0", fill="white")

    img_tk = ImageTk.PhotoImage(img_copy)
    map_label.config(image=img_tk)
    map_label.image = img_tk

display_initial_map()

# Start the main loop
root.mainloop()
