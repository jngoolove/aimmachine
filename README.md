# Screen Color Picker Application

This Python-based application provides a unique and interactive way to pick colors from any area on your computer screen. Utilizing a blend of Python's Tkinter and PIL libraries, it offers a simple and intuitive user interface that allows users to capture a part of their screen, display it within the application, and click on the image to extract and display RGB color values. This tool is perfect for designers, developers, or anyone in need of an easy way to determine and use colors from their screen.

## Key Features

- **Screen Capture:** Easily capture any part of your screen.
- **Interactive Color Picking:** Click on the captured screen portion displayed in the application to pick colors.
- **RGB and Hexadecimal Support:** Displays color values in both RGB and hexadecimal formats.
- **Resize Captured Images:** Captured screen images are automatically resized to fit within the application window, maintaining the aspect ratio.
- **Easy-to-Use Interface:** Simple and straightforward user interface, built with Tkinter.
- **Change the screenshot size to fit your window at:
# Define the size to which you want to scale
    scale_width = 800
    scale_height = int((scale_width / img.width) * img.height)  # Keep the aspect ratio

## Technologies Used

- Python 3
- Tkinter for the GUI
- Pillow (PIL Fork) for image processing
- PyAutoGUI for screen capture functionality

## Installation

Ensure you have Python installed on your system. Clone or download this repository, navigate to the directory, and install the required dependencies:

```bash
pip install pillow pyautogui
