import tkinter as tk
import math
import colorsys
from PIL import ImageGrab, Image,ImageTk
import pyautogui

current_hue = 0
current_saturation = 1
current_value = 1
#hex_entry = 1

def capture_screen_area():
    global img, photo, scaled_img
    # Take a screenshot using pyautogui
    screenshot = pyautogui.screenshot()
    screenshot.save('screenshot.png')

    # Open the saved screenshot
    img = Image.open('screenshot.png')

    # Define the size to which you want to scale
    scale_width = 800
    scale_height = int((scale_width / img.width) * img.height)  # Keep the aspect ratio

    # Resize the image using LANCZOS filter for high-quality downsampling
    scaled_img = img.resize((scale_width, scale_height), Image.LANCZOS)

    # Convert the resized image for Tkinter
    photo = ImageTk.PhotoImage(scaled_img)

    # Update canvas size and display the image
    capture_canvas.config(width=scale_width, height=scale_height)
    capture_canvas.create_image(0, 0, image=photo, anchor='nw')




def pick_color(event):
    # Calculate the corresponding position on the original image
    original_x = int(event.x * (img.width / scaled_img.width))
    original_y = int(event.y * (img.height / scaled_img.height))

    # Get the RGB value of the pixel on the original image
    rgb = img.getpixel((original_x, original_y))
    update_color_display_from_rgb(*rgb)


def update_color_display_from_rgb(r, g, b):
    color = '#{:02x}{:02x}{:02x}'.format(r, g, b)
    color_display.config(bg=color)
    # Update RGB entry fields if needed

def update_color_display():
    try:
        r = int(r_entry.get())
        g = int(g_entry.get())
        b = int(b_entry.get())
        color = '#{:02x}{:02x}{:02x}'.format(r, g, b)
        color_display.config(bg=color)
    except ValueError:
        pass  # Ignore invalid input

# Create the main window
root = tk.Tk()
root.title('Color Picker')



# Display for showing the selected color

# Function to draw the color wheel
def draw_color_wheel(canvas, center, radius):
    for i in range(360):
        r, g, b = colorsys.hsv_to_rgb(i/360, 1, 1)
        color = '#{:02x}{:02x}{:02x}'.format(int(r*255), int(g*255), int(b*255))
        x0 = center + radius * math.cos(math.radians(i))
        y0 = center + radius * math.sin(math.radians(i))
        x1 = center + radius * math.cos(math.radians(i+1))
        y1 = center + radius * math.sin(math.radians(i+1))
        canvas.create_line(x0, y0, x1, y1, fill=color, width=2)

# Function to draw the saturation-value square
def draw_sv_square(canvas, hue, top_left, size):
    for i in range(size):
        for j in range(size):
            saturation = i / size
            value = 1 - j / size
            r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
            color = '#{:02x}{:02x}{:02x}'.format(int(r*255), int(g*255), int(b*255))
            canvas.create_rectangle(top_left[0]+i, top_left[1]+j, top_left[0]+i+1, top_left[1]+j+1, outline=color, fill=color)

# Event handler for clicking on the color wheel
def on_color_wheel_click(event):
    x, y = event.x - 200, event.y - 200
    hue = math.atan2(y, x) / (2 * math.pi)
    hue = hue % 1
    draw_sv_square(sv_canvas, hue, (0, 0), 100)

# Event handler for clicking on the SV square
def on_sv_square_click(event):
    # Placeholder for SV square click handling
    pass

def update_color_display_from_hsv():
    global current_hue, current_saturation, current_value
    r, g, b = colorsys.hsv_to_rgb(current_hue, current_saturation, current_value)
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    update_color_display_from_rgb(r, g, b)

def on_color_wheel_click(event):
    global current_hue
    x, y = event.x - 200, event.y - 200
    current_hue = math.atan2(y, x) / (2 * math.pi) % 1
    draw_sv_square(sv_canvas, current_hue, (0, 0), 100)
    update_color_display_from_hsv()

def on_sv_square_click(event):
    global current_saturation, current_value
    current_saturation = event.x / 100
    current_value = 1 - event.y / 100
    update_color_display_from_hsv()
    
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))



def on_hex_entry_change(event=None):
    if len(hex_entry.get()) == 7:  # Check for complete hex input
        try:
            rgb_color = hex_to_rgb(hex_entry.get())
            update_color_display_from_rgb(*rgb_color)
        except ValueError:
            pass  # Invalid hex input, ignore




# Modify update_color_display_from_rgb to also update hex entry


def update_color_display_from_rgb(r, g, b):
    # Convert to integer and clamp the values between 0 and 255
    r, g, b = max(0, min(255, int(r))), max(0, min(255, int(g))), max(0, min(255, int(b)))
    
    # Update the color display
    color = '#{:02x}{:02x}{:02x}'.format(r, g, b)
    color_display.config(bg=color)

    # Update the RGB entry fields
    r_entry.delete(0, tk.END)
    r_entry.insert(0, str(r))
    g_entry.delete(0, tk.END)
    g_entry.insert(0, str(g))
    b_entry.delete(0, tk.END)
    b_entry.insert(0, str(b))

    # Update the hex entry field
    hex_entry.delete(0, tk.END)
    hex_entry.insert(0, color)


def output_color():
    if hex_entry.get() and len(hex_entry.get()) == 7:  # Check for valid hex input
        try:
            rgb_color = hex_to_rgb(hex_entry.get())
            update_color_display_from_rgb(*rgb_color)
        except ValueError:
            pass  # Invalid hex input, ignore
    else:
        # Use RGB values, defaulting to 0 if empty
        r = r_entry.get() or '0'
        g = g_entry.get() or '0'
        b = b_entry.get() or '0'
        update_color_display_from_rgb(r, g, b)



hex_entry = tk.Entry(root, width=10)
hex_entry.pack()

# Bind the event handler to the hex entry field
#hex_entry.bind("<FocusOut>", on_hex_entry_change)  # This triggers when the user clicks or tabs out of the entry field
# Bind the event handler to the hex entry field
hex_entry.bind("<KeyRelease>", on_hex_entry_change)

# Create a canvas for the color wheel
color_wheel_canvas = tk.Canvas(root, width=400, height=400)
color_wheel_canvas.pack()
draw_color_wheel(color_wheel_canvas, 200, 100)

# Create a canvas for the SV square
sv_canvas = tk.Canvas(root, width=100, height=100)
sv_canvas.pack()

# Bind events to the color wheel and SV square
color_wheel_canvas.bind("<Button-1>", on_color_wheel_click)
sv_canvas.bind("<Button-1>", on_sv_square_click)

# Display for showing the selected color
color_display = tk.Label(root, width=20, height=10, bg='white')
color_display.pack()

# RGB value input fields
r_entry = tk.Entry(root, width=10)
g_entry = tk.Entry(root, width=10)
b_entry = tk.Entry(root, width=10)
r_entry.pack()
g_entry.pack()
b_entry.pack()


# Update the button command
output_button = tk.Button(root, text="Output Color", command=output_color)
output_button.pack()

# Button to capture the screen area
capture_button = tk.Button(root, text="Capture Screen", command=capture_screen_area)
capture_button.pack()

# Canvas for displaying the captured area (placeholder)


capture_canvas = tk.Canvas(root)
capture_canvas.pack()
capture_canvas.bind("<Button-1>", pick_color)

root.mainloop()
