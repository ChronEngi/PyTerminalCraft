# PyTerminalCraft. ChronEngi project on GitHub.
# Allows reading Minecraft chat, via reading the Minecraft Java 'latest.log'.
# It recognizes messages and translates them into terminal commands.
# Keep in mind that the code will read chat messages from any player. I do NOT recommend using it in multiplayer.




import os                       # Library for accessing system information such as the Minecraft Java path location and execute the command.
import psutil                   # Library to access tasks and see if Minecraft Java is running.
import customtkinter as UI      # Library to inilialize a modern graphical user interface.

# Dichiarazioni globali
new_chat_message = ""
told_its_open = False
user_confirmed = False
personal_path = r'C:\Users\prosp\OneDrive\Minecraft\Dati Minecraft\logs\latest.log'
mc_status = False

# Configurazione UI
UI.set_appearance_mode("Dark")
UI.set_default_color_theme("resources/chron_theme.json")

app = UI.CTk()
app.geometry('500x300')
app.title('PyTerminalCraft')
app.iconbitmap('resources/icon.ico')
app.resizable(False, False)

if os.path.exists(personal_path):
    default_mc_path = personal_path
else:
    default_mc_path = os.path.join(os.environ['APPDATA'], 'Roaming', r'.minecraft\logs\latest.log')
    
# print("The path is:", default_mc_path)

# Funzioni
def confirm():
    global user_confirmed
    print('\nUser confirmed\n' + 'Path: ' + log_dir.get() + '\nExecute every ' + delay_value.get() + 'ms\n')
    user_confirmed = True
    app.overrideredirect(True)
    app.geometry('0x0')


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
    global mc_status
    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        if 'java' in process.info['name'].lower() and 'minecraft' in ' '.join(process.info['cmdline']).lower():
            mc_status = True
            return True
    mc_status = False
    return False

def read_mc_chat():
    global new_chat_message
    global told_its_open

    # if is_minecraft_running():
    if mc_status is True:

        if told_its_open is False:
            print('Minecraft Java is running!')
            told_its_open = True

        if user_confirmed is True:
            chat_message = read_log()

            if chat_message != new_chat_message:
                new_chat_message = chat_message

                only_text = chat_message.split('> ', 1)[-1]

                print('\nCommand: ' + only_text)

                # Esegui il comando usando
                os.system(only_text)

    # Richiama nuovamente la funzione dopo un certo periodo
    app.after(delay_value.get(), read_mc_chat)

# Elementi UI
log_dir_title = UI.CTkLabel(app, text='Minecraft log path')
log_dir_title.pack(padx=10, pady=3)

log_dir = UI.CTkEntry(app, width=450)
log_dir.pack(padx=10, pady=3)
log_dir.insert(0, default_mc_path)

delay_value_title = UI.CTkLabel(app, text='Check every (ms)')
delay_value_title.pack(padx=10, pady=3)

delay_value = UI.CTkEntry(app, width=150)
delay_value.pack(padx=10, pady=3)
delay_value.insert(0, 1000)

confirm_but = UI.CTkButton(app, text='Confirm', width=30, command=confirm)
confirm_but.pack(padx=10, pady=40)

git_credits = UI.CTkLabel(app, text='By ChronEngi on GitHub')
git_credits.place(relx=0.5, rely=1.0, anchor='s')

is_minecraft_running()
# Inizia il loop di tkinter
# if user_confirmed is True:
read_mc_chat()

app.mainloop()