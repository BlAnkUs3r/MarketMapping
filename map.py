import tkinter as tk
from tkintermapview import TkinterMapView

def draw_route():
    start_address = entry_start.get()
    end_address = entry_end.get()

    # Clear existing markers by removing all items on the Canvas widget
    canvas.delete("marker")
    canvas.delete("line")  # Clear existing lines

    # Set the markers and labels for start and end points
    map_widget.set_address(start_address, marker=True)
    map_widget.set_address(end_address, marker=True)

    # Add labels for start and end points using the Canvas widget
    x_start, y_start = map_widget.get_position_from_address(start_address)
    x_end, y_end = map_widget.get_position_from_address(end_address)

    canvas.create_text(x_start, y_start - 10, text="Start", fill="red", font=("Arial", 12))
    canvas.create_text(x_end, y_end - 10, text="End", fill="blue", font=("Arial", 12))

    # Draw a line between start and end points
    canvas.create_line(x_start, y_start, x_end, y_end, fill="green", width=2, tags="line")

root_tk = tk.Tk()
root_tk.geometry("800x600")
root_tk.title("Route Drawing")

# Map
map_widget = TkinterMapView(root_tk, width=600, height=400, corner_radius=0)
map_widget.pack(fill="both", expand=True)

# Google URL
map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&h1=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

# Entry for specifying starting and ending addresses
label_start = tk.Label(root_tk, text="Start Address:")
label_start.pack()
entry_start = tk.Entry(root_tk)
entry_start.pack()

label_end = tk.Label(root_tk, text="End Address:")
label_end.pack()
entry_end = tk.Entry(root_tk)
entry_end.pack()

# Button to draw the route
draw_button = tk.Button(root_tk, text="Draw Route", command=draw_route)
draw_button.pack()

# Create a Canvas widget to add labels, markers, and lines
canvas = tk.Canvas(root_tk)
canvas.pack()

root_tk.mainloop()
