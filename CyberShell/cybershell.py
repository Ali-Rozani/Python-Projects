import os
import sys
import subprocess
import winreg
import time
import pygame
from pathlib import Path
from colorama import Fore, init
from pyfiglet import figlet_format

# Initialize color output
init(autoreset=True)  # Import pygame for sound playback

def play_startup_sound():
    pygame.mixer.init()
    pygame.mixer.music.load("computer-startup-264414.mp3")  # Ensure this file is in the same directory
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue  # Wait for sound to finish playing

# Play the startup sound
play_startup_sound()

# Display loading animation
def loading_animation():
    print(Fore.GREEN + "Initializing CyberShell...")
    for i in range(21):
        bar = "[" + "=" * i + " " * (20 - i) + "]"
        sys.stdout.write(f"\r{Fore.GREEN}{bar} ({i * 5}%)")
        sys.stdout.flush()
        time.sleep(0.1)
    print("\n" + Fore.GREEN + "CyberShell Ready!\n")

# Detect installed applications
def detect_apps():
    print(Fore.GREEN + "Scanning for installed applications...\n")
    app_paths = {}

    # Search in common locations
    search_dirs = [
        "C:\\Program Files",
        "C:\\Program Files (x86)",
        os.path.expanduser("~\\AppData\\Local"),
        "C:\\Windows\\System32"
    ]

    for directory in search_dirs:
        for path in Path(directory).rglob("*.exe"):
            app_name = path.stem
            app_paths[app_name] = str(path)

    # Scan the Windows Registry for installed software
    reg_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]

    for reg_path in reg_paths:
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
                for i in range(winreg.QueryInfoKey(key)[0]):
                    try:
                        subkey = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey) as subkey_handle:
                            display_name, _ = winreg.QueryValueEx(subkey_handle, "DisplayName")
                            install_location, _ = winreg.QueryValueEx(subkey_handle, "InstallLocation")
                            if install_location:
                                exe_files = list(Path(install_location).rglob("*.exe"))
                                if exe_files:
                                    app_paths[display_name] = str(exe_files[0])
                    except FileNotFoundError:
                        continue
        except FileNotFoundError:
            continue

    return app_paths

# Launch an application
def launch_app(app_name, app_path):
    print(Fore.GREEN + f"Launching {app_name}...\n")
    subprocess.Popen(app_path, shell=True)

# Main function
def main():
    os.system("cls" if os.name == "nt" else "clear")
    
    # Show CyberShell ASCII banner
    print(Fore.GREEN + figlet_format("CyberShell", font="doom"))

    loading_animation()

    apps = detect_apps()
    if not apps:
        print(Fore.RED + "No applications found.")
        return

    # Display detected applications
    app_list = list(apps.keys())
    for idx, app_name in enumerate(app_list, start=1):
        print(Fore.GREEN + f"{idx}. {app_name}")

    # User selection loop
    while True:
        choice = input(Fore.GREEN + "\nEnter number to open (q to quit): " + Fore.RESET)
        if choice.lower() == "q":
            print(Fore.GREEN + "Exiting CyberShell.")
            break
        elif choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(app_list):
                launch_app(app_list[choice - 1], apps[app_list[choice - 1]])
            else:
                print(Fore.RED + "Invalid selection. Try again.")

if __name__ == "__main__":
    main()