"""PyTerminalCraft. ChronEngi project on GitHub.
Allows reading Minecraft chat, via reading the Minecraft Java 'latest.log'.
It recognizes messages and translates them into terminal commands."""

import ctypes                   # Library, low-level operations to modify terminal settings.
import os                       # Library to get paths and execute the command.
import psutil                   # Library to access tasks and see if Minecraft Java is running.
import customtkinter as UI      # Library to inilialize a modern graphical user interface.


# Global variables - Settings
personal_path = r'C:\Users\prosp\OneDrive\Minecraft\Dati Minecraft\logs\latest.log'
exe_every = 1000

# Global variables - internal
mc_status = False
user_confirmed_settings = False
user_confirmed_responsib = False
new_chat_message = ''
default_mc_path = ''
told_its_open = False
disclaimer_text = '⚠️ DISCLAIMER ⚠️ \nThe author is not responsible for any \nissues arising from the usage.'
multiplayer_warning = 'Remember you are in multiplayer. The creator is not responsible for damage done by you or any other person.'
warning_told = False
chat_indicators = [
    '[main/INFO]: [CHAT]',                      # Modded version like Optifine and Forge
    '[Render thread/INFO]: [CHAT]',             # New Minecraft versions
    '[Client thread/INFO]: [CHAT]'              # Old Minecraft versions
]

# Terminal name
ctypes.windll.kernel32.SetConsoleTitleW('PyTerminalCraft')

# Clear terminal at start
os.system('cls')

# Change terminal color text
print('\033[96mStarting...\n')

# UI config - Theme
UI.set_appearance_mode("Dark")
UI.set_default_color_theme("resources/chron_theme.json")

# UI config - Window
app = UI.CTk()
app.geometry('500x400')
app.title('PyTerminalCraft')
app.iconbitmap('resources/icon.ico')
app.resizable(False, False)

# Consider "personal_path" only if your path is different from the classic one
if os.path.exists(personal_path):
    default_mc_path = personal_path
else:
    default_mc_path = os.path.join(os.environ['APPDATA'], 'Roaming', r'.minecraft\logs\latest.log')
    
# UI - Confirm that you know your responsibilities
def confirm_responsib():
    global user_confirmed_responsib
    global confirm_responsib_but

    # UI - Shows up the settings screen
    # MC path (title)
    log_dir_title.pack(padx=10, pady=3)

    # MC path (entry)
    log_dir.pack(padx=10, pady=3)
    log_dir.insert(0, default_mc_path)

    # Execution delay (title)
    delay_value_title.pack(padx=10, pady=3)

    # Execution delay (entry)
    delay_value.pack(padx=10, pady=3)
    delay_value.insert(0, exe_every)

    # Confirm settings button
    confirm_settings_but.pack(padx=10, pady=80)

    # Hide responsib button and disclaimer
    confirm_responsib_but.place_forget()
    disclaimer.pack_forget()

    # Output
    print('User confirmed the responsibilities\n')

# UI - Confirm settings
def confirm_settings():
    global user_confirmed_settings
    global exe_every

    # Get the delay value from the entry
    exe_every = delay_value.get()

    # Internal variable
    user_confirmed_settings = True

    # Hide the window
    app.overrideredirect(True)
    app.geometry('0x0')

    # Output
    print('Settings confirmed\n' + 'Path: ' + log_dir.get() + '\nExecute every ' + delay_value.get() + 'ms\n')


# Reads the chat from the file "latest.log"
def read_log():
    global warning_told
    global default_mc_path
    
    try:
        # Get the default Minecraft log path from the UI input
        default_mc_path = os.path.normpath(log_dir.get())
        
        # Opens the Minecraft log file in read mode with Latin-1 encoding
        with open(default_mc_path, 'r', encoding='latin-1') as log_file:

            # Reads all lines from the log file
            lines = log_file.readlines()

            # Iterates through the lines in reverse order (from the end of the file)
            for line in reversed(lines):

                # Checks if the line contains at least one of the chat message indicators
                if any(indicator in line for indicator in chat_indicators):

                    # Finds the actual indicator in the list that matches the line
                    for indicator in chat_indicators:
                        if indicator in line:
                            # Extracts the chat message and removes leading/trailing whitespaces
                            return line.split(indicator + ' ')[1].strip()
                        
                # Check if the line contains the word "Connecting"
                if "Connecting" in line and warning_told is False:
                    warning_told = True
                    msg(multiplayer_warning, 'WARNING CHRON-000', 0x30)
                    return

    except FileNotFoundError as e:
        print(e)
        msg('Exception while reading a message!', 'ERROR CHRON-001', 0x10)
        return None


# Checks if Minecraft Java is currently running
def is_minecraft_running():
    global mc_status

    # Iterate through all running processes with details like PID, name, and command line
    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        
        # Check if the process name contains 'java' and the command line contains 'minecraft'
        if 'java' in process.info['name'].lower() and 'minecraft' in ' '.join(process.info['cmdline']).lower():
            
            # Set the global variable mc_status to True indicating that Minecraft is running
            mc_status = True
            return

    # If no matching process is found, set mc_status to False and return False
    mc_status = False
    return


# Continuously reads the Minecraft chat and executes commands in the terminal
def read_mc_chat():
    global user_confirmed_settings
    global new_chat_message
    global told_its_open

    # Check if Minecraft is currently running
    if mc_status is True:

        # Check if the user has confirmed settings
        if user_confirmed_settings is True:

            try:
                # Read the latest chat message from the Minecraft log
                chat_message = read_log()

                # Check if there is a new chat message and it is not None
                if chat_message is not None and chat_message != new_chat_message:
                    new_chat_message = chat_message

                    # Extract the text portion of the chat message (excluding the player name)
                    only_text = chat_message.split('> ', 1)[-1]

                    # Print the command to be executed in the terminal
                    print('\nCommand: ' + only_text)

                    # Execute the command using the OS library
                    os.system(only_text)
            except Exception as e:
                print(e)
                msg('Exception while formatting or executing text.\nTry typing "echo fix" in Minecraft chat and reopen the program!', 'ERROR CHRON-002', 0x10)
                exit()
        

    # Schedule the function to be called again after a certain delay
    app.after(exe_every, read_mc_chat)

# Send an error/info message
def msg(msg_title, msg_info, msg_type):

    # Generate the window
    ctypes.windll.user32.MessageBoxW(0, msg_title, msg_info, msg_type)

    # Set as first window
    ctypes.windll.user32.SetWindowPos(ctypes.windll.kernel32.GetConsoleWindow(), -1, 0, 0, 0, 0, 0x3 | 0x10)
    return

# UI Elements
log_dir_title = UI.CTkLabel(app, text='Minecraft log path')
log_dir = UI.CTkEntry(app, width=450)

# Execution delay (title) & (entry)
delay_value_title = UI.CTkLabel(app, text='Check every (ms)')
delay_value = UI.CTkEntry(app, width=150)

# Confirm settings (button)
confirm_settings_but = UI.CTkButton(app, text='Confirm', width=30, command=confirm_settings)

# Disclaimer label with a warning message
disclaimer = UI.CTkLabel(app, text=disclaimer_text, font=('Helvetica', 14, 'bold'))
disclaimer.pack(padx=10, pady=10, )

# Button to confirm user responsibilities
confirm_responsib_but = UI.CTkButton(app, text='I know', width=30, command=confirm_responsib)
confirm_responsib_but.place(relx=0.5, rely=0.5, anchor='s')

# Label indicating the author and source on GitHub
git_credits = UI.CTkLabel(app, text='By ChronEngi on GitHub')
git_credits.place(relx=0.5, rely=1.0, anchor='s')

# Check if Minecraft is running and continuously read the chat
is_minecraft_running()

#   If mc is not running, send an error
if mc_status is False:
    msg('Minecraft Java is not running!', 'ERROR CHRON-000', 0x10)
    exit()

# read the chat line
read_mc_chat()

if __name__ == "__main__":
    app.mainloop()

# Add a newline at the end of the file
