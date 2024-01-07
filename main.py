import os
import psutil
import time
import subprocess
import customtkinter as ctk
import keyboard

# Dichiarazioni globali
new_chat_message = ""
told_its_open = False
user_confirmed = False
personal_path = r'C:\Users\prosp\OneDrive\Minecraft\Dati Minecraft\logs\latest.log'

# Configurazione UI
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("chron_theme.json")

app = ctk.CTk()
app.geometry('500x300')
app.title('PyTerminalCraft')
app.iconbitmap('icon.ico')
app.resizable(False, False)

if os.path.exists(personal_path):
    default_mc_path = personal_path
else:
    default_mc_path = os.path.join(os.environ['APPDATA'], 'Roaming', '.minecraft')
    
print("The path is:", default_mc_path)

# Funzioni
def confirm():
    global user_confirmed
    print('User confirmed')
    user_confirmed = True

    # Nascondi la finestra e contenuti
    #app.iconify()
    app.geometry('0x0')
    app.overrideredirect(True)
    #log_dir.forget()
    #confirm_but.forget()


def read_log():
    try:
        default_mc_path = os.path.normpath(log_dir.get())
        with open(default_mc_path, 'r', encoding='latin-1') as log_file:
            lines = log_file.readlines()

            for line in reversed(lines):
                if '[Render thread/INFO]: [CHAT]' in line:
                    return line.split('[Render thread/INFO]: [CHAT] ')[1].strip()
    except FileNotFoundError:
        return None

def is_minecraft_running():
    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        if 'java' in process.info['name'].lower() and 'minecraft' in ' '.join(process.info['cmdline']).lower():
            return True
    return False

def read_mc_chat():
    global new_chat_message
    global told_its_open

    if is_minecraft_running():

        if told_its_open is False:
            print('Minecraft docked!')
            told_its_open = True

        if user_confirmed is True:
            chat_message = read_log()

            if chat_message != new_chat_message:
                new_chat_message = chat_message

                only_text = chat_message.split('> ', 1)[-1]

                # Esegui il comando usando subprocess
                subprocess.run(only_text, shell=True)

                # os.system(only_text)

                # if only_text == "notepad":
                #     os.system('notepad.exe')


    # Richiama nuovamente la funzione dopo un certo periodo
    app.after(200, read_mc_chat)

# Elementi UI
log_dir = ctk.CTkEntry(app, width=450)
log_dir.pack(padx=10, pady=10)
log_dir.insert(0, default_mc_path)

confirm_but = ctk.CTkButton(app, text='Confirm', width=30, command=confirm)
confirm_but.pack(padx=10, pady=10)


# Avvia la funzione di lettura nel thread principale di tkinter
read_mc_chat()

# Function to prevent window from being closed
def on_closing():
    print("Window close button clicked, but preventing window from closing.")

# Bind the protocol method to the on_closing function
#app.protocol("WM_DELETE_WINDOW", on_closing)

# Funzione chiamata quando viene premuta la combinazione di tasti di emergenza
def emergency_hotkey():
    app.geometry('500x300')
    app.deiconify()
    app.overrideredirect(False)
    app.lift()
    app.focus_force()

# Show Window
keyboard.add_hotkey('altgr+l', emergency_hotkey)

# Inizia il loop di tkinter
app.mainloop()
