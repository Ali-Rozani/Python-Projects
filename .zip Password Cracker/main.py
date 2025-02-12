import pyzipper
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import itertools
import string
import time
import os

class ZipPasswordCracker:
    def __init__(self):
        self.chars = string.ascii_letters + string.digits + string.punctuation
        self.max_length = 6
        self.is_cracking = False

    def generate_passwords(self):
        for length in range(1, self.max_length + 1):
            for combo in itertools.product(self.chars, repeat=length):
                yield ''.join(combo)

    def crack_password(self, zip_path, status_label, output_text):
        self.is_cracking = True
        start_time = time.time()
        attempts = 0

        # Remove quotes from the file path
        zip_path = zip_path.strip('"')

        try:
            for password in self.generate_passwords():
                if not self.is_cracking:
                    break

                attempts += 1
                try:
                    with pyzipper.AESZipFile(zip_path) as zf:
                        zf.extractall(pwd=password.encode())
                        
                        end_time = time.time()
                        output_text.insert(tk.END, f"Password found: {password}\n")
                        output_text.insert(tk.END, f"Time taken: {end_time - start_time:.2f} seconds\n")
                        output_text.insert(tk.END, f"Attempts: {attempts}\n")
                        
                        status_label.config(text="Password cracked!", fg="green")
                        return True
                
                except (RuntimeError, pyzipper.BadZipFile, KeyError):
                    output_text.insert(tk.END, f"Attempt {attempts}: {password} failed\n")
                
                if attempts % 1000 == 0:
                    output_text.see(tk.END)
                    status_label.config(text=f"Attempts: {attempts}")
                    time.sleep(0.01)  # Prevent GUI freezing

        except FileNotFoundError:
            output_text.insert(tk.END, f"Error: File not found - {zip_path}\n")
            status_label.config(text="Error: File not found", fg="red")
        
        except PermissionError:
            output_text.insert(tk.END, f"Error: Permission denied\n")
            status_label.config(text="Error: Permission denied", fg="red")
        
        output_text.insert(tk.END, "Password not cracked.\n")
        status_label.config(text="Password not found", fg="red")
        return False

    def start_cracking(self, zip_path, status_label, output_text, stop_button):
        def crack():
            if self.crack_password(zip_path, status_label, output_text):
                messagebox.showinfo("Success", "Password cracking successful!")
            else:
                messagebox.showinfo("Failed", "Password cracking failed.")
            stop_button.config(state=tk.DISABLED)

        threading.Thread(target=crack, daemon=True).start()

    def stop_cracking(self):
        self.is_cracking = False

def browse_file(entry):
    filename = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, filename)

def main():
    root = tk.Tk()
    root.title("Zip Password Cracker")
    root.geometry("600x500")
    root.configure(bg="black")

    cracker = ZipPasswordCracker()

    style = ttk.Style()
    style.configure("TLabel", background="black", foreground="green", font=("Courier", 12))
    style.configure("TButton", background="black", foreground="green", font=("Courier", 12))
    style.configure("TEntry", background="black", foreground="green", font=("Courier", 12))

    zip_file_label = ttk.Label(root, text="Zip File:")
    zip_file_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    zip_file_entry = ttk.Entry(root, width=40)
    zip_file_entry.grid(row=0, column=1, padx=10, pady=10)

    zip_file_button = ttk.Button(root, text="Browse", command=lambda: browse_file(zip_file_entry))
    zip_file_button.grid(row=0, column=2, padx=10, pady=10)

    status_label = ttk.Label(root, text="Ready", foreground="green")
    status_label.grid(row=1, column=0, columnspan=3, pady=10)

    output_text = scrolledtext.ScrolledText(root, width=70, height=15, bg="black", fg="green", font=("Courier", 12))
    output_text.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    button_frame = ttk.Frame(root)
    button_frame.grid(row=3, column=0, columnspan=3, pady=10)

    start_button = ttk.Button(button_frame, text="Start Cracking", 
                               command=lambda: cracker.start_cracking(
                                   zip_file_entry.get(), 
                                   status_label, 
                                   output_text, 
                                   stop_button
                               ))
    start_button.pack(side=tk.LEFT, padx=5)

    stop_button = ttk.Button(button_frame, text="Stop Cracking", 
                              command=cracker.stop_cracking, 
                              state=tk.DISABLED)
    stop_button.pack(side=tk.LEFT, padx=5)

    root.mainloop()

if __name__ == "__main__":
    main()