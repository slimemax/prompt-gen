import tkinter as tk
import pyperclip
import pyautogui
import time
import threading
import xml.etree.ElementTree as ET
import os  # Import os for directory scanning

# Global variable to control the running state of the auto-typing thread
is_typing = False

# Function to scan directory for XML files and update dropdown
def scan_directory_for_xml():
    xml_files = [file for file in os.listdir('.') if file.endswith('.xml')]
    if not xml_files:
        display_alert("No XML files found in the current directory.", "warning")
    return xml_files

# Function to load categories from the selected XML file
def load_categories_from_xml(file_path):
    categories = {}
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        for category in root.findall('category'):
            category_name = category.get('name')
            words = [word.text for word in category.findall('word')]
            categories[category_name] = words
            
    except ET.ParseError as e:
        display_alert(f"Error parsing XML: {e}", "error")
    except FileNotFoundError:
        display_alert(f"File not found: {file_path}", "error")
        
    return categories

# Function to update category buttons based on selected XML file
def update_categories():
    selected_file = xml_file_var.get()
    if selected_file:
        categories = load_categories_from_xml(selected_file)
        create_category_buttons(categories)
        display_alert(f"Loaded categories from {selected_file}", "info")
    else:
        display_alert("Please select an XML file to load categories.", "warning")

# Function to create category buttons dynamically
def create_category_buttons(categories):
    for widget in category_frame_left.winfo_children():
        widget.destroy()
    for widget in category_frame_right.winfo_children():
        widget.destroy()

    half_index = len(categories) // 2
    categories_list = list(categories.items())

    # Add buttons to the bottom left
    for category, words in categories_list[:half_index]:
        frame = tk.LabelFrame(category_frame_left, text=category, padx=5, pady=5)
        frame.pack(padx=10, pady=5, fill="x")

        for word in words:
            button = tk.Button(frame, text=word, command=lambda w=word: add_to_prompt(w))
            button.pack(side="left", padx=5, pady=5)

    # Add buttons to the bottom right
    for category, words in categories_list[half_index:]:
        frame = tk.LabelFrame(category_frame_right, text=category, padx=5, pady=5)
        frame.pack(padx=10, pady=5, fill="x")

        for word in words:
            button = tk.Button(frame, text=word, command=lambda w=word: add_to_prompt(w))
            button.pack(side="left", padx=5, pady=5)

# Function to add the selected word to the text field
def add_to_prompt(word):
    current_text = prompt_text.get("1.0", tk.END).strip()
    
    if auto_comma_var.get():
        # Check if the word is "more" and handle accordingly
        if word == "more":
            new_text = current_text + ", " + word if current_text else word
        else:
            if current_text.endswith("more"):
                new_text = current_text + " " + word  # Add space instead of comma after "more"
            else:
                new_text = current_text + ", " + word if current_text else word
    else:
        new_text = current_text + " " + word if current_text else word

    prompt_text.delete("1.0", tk.END)
    prompt_text.insert(tk.END, new_text)

# Function to display alerts in the scrollable alerts box
def display_alert(message, message_type="info"):
    if message_type == "info":
        color = "blue"
    elif message_type == "warning":
        color = "orange"
    elif message_type == "error":
        color = "red"
    else:
        color = "black"
    
    # Insert the message with the specified color
    alerts_textbox.insert(tk.END, message + "\n", color)
    alerts_textbox.see(tk.END)  # Scroll to the latest alert

# Function to copy the prompt to clipboard
def copy_to_clipboard():
    current_text = prompt_text.get("1.0", tk.END).strip()
    if current_text:
        pyperclip.copy(current_text)
        display_alert("Prompt copied to clipboard successfully!", "info")
    else:
        display_alert("The prompt field is empty. Please add some words.", "warning")

# Function to clear the prompt text field
def clear_prompt():
    prompt_text.delete("1.0", tk.END)
    display_alert("Prompt cleared.", "info")

# Function to auto type the text in a separate thread
def auto_type():
    global is_typing
    if is_typing:
        display_alert("Typing already in progress. Please wait or click Abort.", "warning")
        return

    is_typing = True
    current_text = prompt_text.get("1.0", tk.END).strip()
    try:
        delay = int(time_entry.get()) / 1000  # Convert milliseconds to seconds for the initial delay
        if current_text:
            display_alert(f"Auto-typing with {delay * 1000} ms initial delay...", "info")
            auto_type_button.config(bg="yellow")  # Change button color to indicate running state

            # Start a new thread for typing
            typing_thread = threading.Thread(target=perform_typing, args=(current_text, delay))
            typing_thread.start()
        else:
            display_alert("The prompt field is empty. Please add some words.", "warning")
    except ValueError:
        display_alert("Invalid time interval! Please enter a number.", "error")

# Function to perform typing
def perform_typing(text, initial_delay):
    global is_typing
    try:
        time.sleep(initial_delay)
        for char in text:
            if not is_typing:
                display_alert("Auto-typing aborted.", "warning")
                auto_type_button.config(bg=original_button_color)  # Reset button color
                return
            pyautogui.write(char, interval=0.01)  # Type with minimal delay for 100+ WPM speed
        pyautogui.press("enter")
        display_alert("Auto-typing complete!", "info")
    finally:
        is_typing = False
        auto_type_button.config(bg=original_button_color)  # Reset button color

# Function to abort typing
def abort_typing():
    global is_typing
    is_typing = False

# Create the main application window
root = tk.Tk()
root.title("Visual Descriptor Prompt Builder")

# Variable to track the state of the Auto Comma checkbox
auto_comma_var = tk.BooleanVar(value=True)

# Configure the grid layout for 2x2
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)

# Top left: Text box with buttons and Auto Comma checkbox
prompt_frame = tk.Frame(root)
prompt_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)

prompt_label = tk.Label(prompt_frame, text="Build your prompt here:")
prompt_label.pack(anchor="w")

prompt_text = tk.Text(prompt_frame, height=4, width=60)
prompt_text.pack(side="left", padx=5, pady=5)

scrollbar = tk.Scrollbar(prompt_frame, command=prompt_text.yview)
scrollbar.pack(side="left", fill="y")
prompt_text.config(yscrollcommand=scrollbar.set)

# Action buttons and Auto Comma checkbox
button_frame = tk.Frame(prompt_frame)
button_frame.pack(pady=5)

copy_button = tk.Button(button_frame, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.pack(side="left", padx=10)

clear_button = tk.Button(button_frame, text="Clear", command=clear_prompt)
clear_button.pack(side="left", padx=10)

# Auto Comma Checkbox
auto_comma_checkbox = tk.Checkbutton(button_frame, text="Auto Comma", variable=auto_comma_var)
auto_comma_checkbox.pack(side="left", padx=10)

# Time interval entry and Auto Type button
time_entry = tk.Entry(button_frame, width=5)
time_entry.insert(0, "100")  # Default to 100 milliseconds initial delay
time_entry.pack(side="left", padx=5)
time_entry_label = tk.Label(button_frame, text="ms")
time_entry_label.pack(side="left")

auto_type_button = tk.Button(button_frame, text="Auto Type", command=auto_type)
auto_type_button.pack(side="left", padx=10)

# Save the original button color for resetting later
original_button_color = auto_type_button.cget("bg")

# Abort button
abort_button = tk.Button(button_frame, text="Abort", command=abort_typing, bg="red")
abort_button.pack(side="left", padx=10)

# Top right: Alerts box with scrollable text area
alerts_frame = tk.Frame(root, relief="sunken", borderwidth=1)
alerts_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)

alerts_label = tk.Label(alerts_frame, text="Alerts:", anchor="w")
alerts_label.pack(fill="x")

alerts_scrollbar = tk.Scrollbar(alerts_frame)
alerts_scrollbar.pack(side="right", fill="y")

alerts_textbox = tk.Text(alerts_frame, height=10, wrap="word", yscrollcommand=alerts_scrollbar.set)
alerts_textbox.pack(expand=True, fill="both")

alerts_scrollbar.config(command=alerts_textbox.yview)

# Tag configurations for text colors
alerts_textbox.tag_configure("info", foreground="blue")
alerts_textbox.tag_configure("warning", foreground="orange")
alerts_textbox.tag_configure("error", foreground="red")

# Dropdown menu for XML files
xml_file_var = tk.StringVar()
xml_file_var.set("Select XML File")

xml_files = scan_directory_for_xml()
xml_dropdown = tk.OptionMenu(root, xml_file_var, *xml_files)
xml_dropdown.grid(row=1, column=0, pady=10, sticky="ew")
load_button = tk.Button(root, text="Load XML", command=update_categories)
load_button.grid(row=1, column=1, pady=10)

# Bottom left: First half of category buttons
category_frame_left = tk.Frame(root)
category_frame_left.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)

# Bottom right: Second half of category buttons
category_frame_right = tk.Frame(root)
category_frame_right.grid(row=2, column=1, sticky="nsew", padx=10, pady=5)

# Run the application
root.mainloop()

