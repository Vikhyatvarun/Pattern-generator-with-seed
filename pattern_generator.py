import random
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button, IntVar, StringVar, OptionMenu, Checkbutton, Menu, DISABLED, NORMAL, messagebox

def toggle_dot_color_option():
    """Enable or disable dot color selection based on the colorful dots option."""
    if colorful_dots_option.get():
        dot_color_menu.configure(state=DISABLED)
    else:
        dot_color_menu.configure(state=NORMAL)

def toggle_line_color_option():
    """Enable or disable line color selection based on the colorful lines option."""
    if colorful_lines_option.get():
        line_color_menu.configure(state=DISABLED)
    else:
        line_color_menu.configure(state=NORMAL)

def apply_placeholder_to_seed(event):
    """Apply the placeholder text to the seed input box if it's empty."""
    if not seed_input.get():
        seed_input.insert(0, "Random number")
        seed_input.config(fg="grey")

def remove_placeholder_from_seed(event):
    """Remove the placeholder text when the user focuses on the seed input box."""
    if seed_input.get() == "Random number":
        seed_input.delete(0, "end")
        seed_input.config(fg="black")

def apply_placeholder(event):
    """Apply the placeholder text to the dots input box if it's empty."""
    if not num_dots_input.get():
        num_dots_input.insert(0, "1-50")
        num_dots_input.config(fg="grey")

def remove_placeholder(event):
    """Remove the placeholder text when the user focuses on the dots input box."""
    if num_dots_input.get() == "1-50":
        num_dots_input.delete(0, "end")
        num_dots_input.config(fg="black")

def add_color_dot_to_menu(menu, variable, colors):
    """Add a colored dot next to each color name in the drop-down menu."""
    menu["menu"].delete(0, "end")  # Clear the current menu
    for color_name, color_code in colors:
        menu["menu"].add_command(
            label=f"● {color_name}",  # Add a colored dot next to the name
            command=lambda value=color_name: variable.set(value),
        )

def generate_pattern():
    try:
        # Get user inputs from the GUI
        seed = seed_input.get()
        
        # Generate a random seed silently if the input box is blank
        if seed == "Random number" or not seed.strip():
            seed = str(random.randint(0, 10**8))  # Random numeric seed
        
        # Validate number of dots input
        num_points = num_dots_input.get()
        if num_points == "1-50" or not num_points.strip():
            raise ValueError("You must enter a number between 1 and 50.")
        num_points = int(num_points)
        
        if num_points < 1 or num_points > 50:
            raise ValueError("The number of dots must be between 1 and 50.")
        
        dot_is_colorful = colorful_dots_option.get()
        line_is_colorful = colorful_lines_option.get()

        # Generate colors for dots and lines
        if dot_is_colorful:
            dot_colors = [f"#{random.randint(0, 0xFFFFFF):06x}" for _ in range(num_points)]
            dot_color = "Colorful"
        else:
            dot_colors = [dot_color_input.get()] * num_points
            dot_color = dot_color_input.get()

        if line_is_colorful:
            line_colors = [f"#{random.randint(0, 0xFFFFFF):06x}" for _ in range(num_points)]
            line_color = "Colorful"
        else:
            line_colors = [line_color_input.get()] * num_points
            line_color = line_color_input.get()

        # Set the random seed
        random.seed(seed)

        # Generate random points
        points = [(random.uniform(0, 1), random.uniform(0, 1)) for _ in range(num_points)]

        # Create the plot
        plt.figure(figsize=(8, 8))
        for i, point in enumerate(points):
            # Plot the dots
            plt.scatter(*point, color=dot_colors[i])
            plt.text(*point, f"{i}", fontsize=8, ha='right', color=dot_colors[i])

        # Connect the dots with lines
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                plt.plot([points[i][0], points[j][0]], [points[i][1], points[j][1]], color=line_colors[i], linewidth=0.7)

        # Add centered information at the bottom of the image
        info_text = f"Seed: {seed} | Number of Dots: {num_points} | Color of Dots: {dot_color} | Color of Lines: {line_color}"
        plt.figtext(0.5, 0.01, info_text, wrap=True, horizontalalignment='center', fontsize=10, color="black")

        # Customize the plot
        plt.title("Unique Pattern from Seed")
        plt.axis("off")
        plt.show()

    except ValueError as e:
        # Show an error message if input is invalid
        messagebox.showerror("Invalid Input", str(e))

# Colors for the dropdown menus
colors = [
    ("Red", "#FF0000"),
    ("Green", "#008000"),
    ("Blue", "#0000FF"),
    ("Yellow", "#FFFF00"),
    ("Purple", "#800080"),
    ("Black", "#000000"),
]

# Create the GUI
root = Tk()
root.title("Pattern Generator")

# Seed input with placeholder
Label(root, text="Enter Seed: ", anchor="w", width=15).grid(row=0, column=0)
seed_input = Entry(root, width=25)
seed_input.grid(row=0, column=1)
seed_input.insert(0, "Random number")
seed_input.config(fg="grey")  # Set placeholder style
seed_input.bind("<FocusIn>", remove_placeholder_from_seed)
seed_input.bind("<FocusOut>", apply_placeholder_to_seed)

# Number of dots input with placeholder
Label(root, text="Number of Dots: ", anchor="w", width=15).grid(row=1, column=0)
num_dots_input = Entry(root, width=25)
num_dots_input.grid(row=1, column=1)
num_dots_input.insert(0, "20")  # Set default value
num_dots_input.config(fg="black")

# Dot color selection
Label(root, text="Dot Color: ", anchor="w", width=15).grid(row=2, column=0)
dot_color_input = StringVar(root)
dot_color_input.set("Blue")  # Default value
dot_color_menu = OptionMenu(root, dot_color_input, *["Red", "Green", "Blue", "Yellow", "Purple", "Black"])
dot_color_menu.grid(row=2, column=1)

# Add actual color dots
add_color_dot_to_menu(dot_color_menu, dot_color_input, colors)

# Colorful dots toggle (below dot color selection)
Label(root, text="Colorful Dots: ", anchor="w", width=15).grid(row=3, column=0)
colorful_dots_option = IntVar()
Checkbutton(root, text="Enable", variable=colorful_dots_option, command=toggle_dot_color_option).grid(row=3, column=1)

# Line color selection
Label(root, text="Line Color: ", anchor="w", width=15).grid(row=4, column=0)
line_color_input = StringVar(root)
line_color_input.set("Black")  # Default value
line_color_menu = OptionMenu(root, line_color_input, *["Red", "Green", "Blue", "Yellow", "Purple", "Black"])
line_color_menu.grid(row=4, column=1)

# Add actual color dots
add_color_dot_to_menu(line_color_menu, line_color_input, colors)

# Colorful lines toggle
Label(root, text="Colorful Lines: ", anchor="w", width=15).grid(row=5, column=0)
colorful_lines_option = IntVar()
Checkbutton(root, text="Enable", variable=colorful_lines_option, command=toggle_line_color_option).grid(row=5, column=1)

# Generate button
generate_button = Button(root, text="Generate Pattern", command=generate_pattern)
generate_button.grid(row=6, column=0, columnspan=2)

# Run the GUI
root.mainloop()