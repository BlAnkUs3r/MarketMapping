import os
import customtkinter
from PIL import ImageTk
from tkinter import Label, IntVar
import subprocess

#current directory
current_directory = os.getcwd()

# custom color
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("dark-blue")

# Title Name
root = customtkinter.CTk()
root.geometry("320x480")
root.title("Market Mapping")

# path to logo
root.iconpath = ImageTk.PhotoImage(file=os.path.join(current_directory, "shoppingcart.png"))
root.wm_iconbitmap()
root.iconphoto(False, root.iconpath)

# close UI
def closeWindow():
   root.destroy()

# opens map.py
def openMainpage():
    # Specify the path to the map.py script here
    main_script_path = os.path.join(current_directory, "mainpage.py")
    
    # Close the current UI window
    root.destroy()
    try:
        # Start the map.py script and wait for it to complete
        subprocess.run(["python", main_script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running mainpage.py: {e}")


# registration process
def register():
    username = entry1.get()
    password = entry2.get()

    # Store the username and password
    with open("userPass.txt", "a") as file:
        file.write(f"Username: {username}, Password: {password}\n")
        # NOW REGISTERED
    print(f"Registered: Username - {username}, Password - {password} now stored in database")

# login process
def login():
    entered_username = entry1.get()
    entered_password = entry2.get()
    error_label.config(text="")  # Clear any previous error message

    # runs through file to check for authentication
    with open("userPass.txt", "r") as file:
        for line in file:
            parts = line.strip().split(', ')
            username = parts[0].split(': ')[1]
            password = parts[1].split(': ')[1]

            # check if username and password matches
            if username == entered_username and password == entered_password:
                print(f"Logged In: Username - {username}, Password - {password}")

                # Check if "Remember Me" is checked
                if remember_me.get() == 1:
                    save_credentials(entered_username, entered_password)

                # Open map.py
                openMainpage()
                return  # Exit the function when a match is found

    error_label.config(text="Login Failed: Invalid username or password", fg="red")

# Function to save credentials to a file
def save_credentials(username, password):
    with open("remembered_credentials.txt", "w") as file:
        file.write(f"Username: {username}\n")
        file.write(f"Password: {password}\n")

# Function to load saved credentials
def load_credentials():
    try:
        with open("remembered_credentials.txt", "r") as file:
            lines = file.readlines()
            if len(lines) == 2:
                saved_username = lines[0].strip().split(': ')[1]
                saved_password = lines[1].strip().split(': ')[1]
                entry1.insert(0, saved_username)
                entry2.insert(0, saved_password)
                remember_me.set(1)  # Check the "Remember Me" checkbox
    except FileNotFoundError:
        pass

# master frame
frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

# text
title_label = customtkinter.CTkLabel(master=frame, text="Market Mapping", font=("Roboto", 24))
title_label.pack(pady=12, padx=10)

label = customtkinter.CTkLabel(master=frame, text="Log In", font=("Roboto", 18))
label.pack(pady=12, padx=10)

entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="Username")
entry1.pack(pady=12, padx=10)

entry2 = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show="*")
entry2.pack(pady=12, padx=10)

# Load saved credentials
remember_me = IntVar()
load_credentials()

error_label = Label(master=frame, text="", font=("Roboto", 12), fg="red")
error_label.pack(pady=5, padx=10)

register_button = customtkinter.CTkButton(master=frame, text="Register", command=register)
register_button.pack(pady=12, padx=10)

login_button = customtkinter.CTkButton(master=frame, text="Login", command=login)
login_button.pack(pady=12, padx=10)

checkbox = customtkinter.CTkCheckBox(master=frame, text="Remember Me", variable=remember_me)
checkbox.pack(pady=12, padx=10)

root.mainloop()
