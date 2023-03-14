from tkinter import *
import tkinter.filedialog as filedialog
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

class FileEncryptionGUI:
    def __init__(self, master):

        # Define colors 
        bg_color = "#f3f3f3"
        accent_color = "#4fb99f"

        self.master = master
        self.master.title("PyLock")
        self.master.configure(bg=bg_color)

        # Initialize variables
        self.selected_file = None
        self.key = ""

        # Title Label
        self.title_label = Label(
            master, 
            text="PyLock", 
            font=("Helvetica", 28, "bold"), 
            fg=accent_color,
            bg=bg_color,
            pady=20
        )
        self.title_label.pack()

        # File Selector Elements
        self.file_frame = Frame(master, bg=bg_color)
        self.file_frame.pack(pady=(10, 20))

        self.select_file_label = Label(
            self.file_frame, 
            text="Select a file to encrypt/decrypt:", 
            bg=bg_color, 
            fg="#333333",
            font=("Helvetica", 14),
            padx=20,
            pady=10
        )
        self.select_file_label.pack(side=LEFT)

        self.file_button = Button(
            self.file_frame, 
            text="Browse Files", 
            command=self.browse_files,
            bg=accent_color,
            fg="#FFFFFF",
            font=("Helvetica", 12),
            padx=15
        )
        self.file_button.pack(side=LEFT, padx=10)

        self.status_label = Label(
            master, 
            text="", 
            fg="red",
            bg=bg_color,
            font=("Helvetica", 12)
        )
        self.status_label.pack(pady=(0,10))

        # Encryption Elements
        self.encryption_frame = Frame(master, bg=bg_color)
        self.encryption_frame.pack(pady=10)

        self.generate_button = Button(
            self.encryption_frame,
            text="Generate Key",
            command=self.generate_key,
            bg=accent_color,
            fg="#FFFFFF",
            font=("Helvetica", 12),
            padx=15
        )
        self.generate_button.grid(row=0, column=0, pady=10, padx=10)

        self.key_entry_label = Label(
            self.encryption_frame, 
            text="Enter encryption key:", 
            bg=bg_color, 
            fg="#333333",
            font=("Helvetica", 14),
        )
        self.key_entry_label.grid(row=0, column=1, padx=10)

        self.key_entry = Entry(
            self.encryption_frame, 
            width=30,
            font=("Helvetica", 12),
            highlightbackground=accent_color, 
            highlightthickness=2
        )
        self.key_entry.grid(row=0, column=2)

        self.encrypt_button = Button(
            master, 
            text="Encrypt", 
            state=DISABLED,
            command=self.encrypt_file,
            bg=accent_color,
            fg="#FFFFFF",
            font=("Helvetica", 12),
            padx=15
        )
        self.encrypt_button.pack(side=LEFT, padx=(50,5), pady=10)

        self.decrypt_button = Button(
            master, 
            text="Decrypt", 
            state=DISABLED,
            command=self.decrypt_file,
            bg=accent_color,
            fg="#FFFFFF",
            font=("Helvetica", 12),
            padx=15
        )
        self.decrypt_button.pack(side=LEFT, pady=10)

    def browse_files(self):
        self.selected_file = filedialog.askopenfilename(initialdir="/", title="Select a file", filetypes=[("All Files", "*.*")])
        if self.selected_file:
            self.status_label.config(text=f"Selected file: {self.selected_file}")
            self.enable_buttons()
        else:
            self.status_label.config(text="No file selected.")
            self.disable_buttons()

    def enable_buttons(self):
        self.encrypt_button.config(state=NORMAL)
        self.decrypt_button.config(state=NORMAL)

    def disable_buttons(self):
        self.encrypt_button.config(state=DISABLED)
        self.decrypt_button.config(state=DISABLED)


    def generate_key(self):
        self.key = get_random_bytes(32)
        self.key_entry.delete(0, END)
        self.key_entry.insert(0, self.key.hex())

    def pad_file(self, data):
        # Pad file in order to make it cipher block size compliant
        padded_data = data
        padding_length = AES.block_size - (len(data) % AES.block_size)
        for i in range(padding_length):
            padded_data += bytes([padding_length])

        return padded_data

    def unpad_file(self, padded_data):
        # Remove padding from file
        padding_length = padded_data[-1]

        return padded_data[:-padding_length]

    def encrypt_file(self):
        try:
            if not self.key:
                raise ValueError("No key set.")

            if not self.selected_file:
                raise ValueError("File not selected.")

            with open(self.selected_file, "rb") as f:
                data = f.read()

            # Encrypt the file data
            cipher = AES.new(self.key, AES.MODE_CBC)
            encrypted_data = cipher.iv + cipher.encrypt(self.pad_file(data))

            # Write encrypted data to new file
            with open(self.selected_file+".enc", 'wb') as f:
                f.write(encrypted_data)

            self.status_label.config(text="File encrypted.")

        except Exception as e:
            self.status_label.config(text="Error: "+str(e))

    def decrypt_file(self):
        try:
            with open(self.selected_file, "rb") as f:
                data = f.read()

            # Get original file extension
            file_extension = self.selected_file.split(".")[-2]
            
            # Decrypt the file data
            iv = data[:16]
            cipher_data = data[16:]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            decrypted_data = self.unpad_file(cipher.decrypt(cipher_data))
            
            # Write decrypted data to new file with original file extension
            with open(f"{self.selected_file[:-len(file_extension)-1]}decrypted.{file_extension}", 'wb') as f:
                f.write(decrypted_data)
                
            self.status_label.config(text="File decrypted.")

        except Exception as e:
            self.status_label.config(text="Error: "+str(e))




# create GUI
root = Tk()
gui = FileEncryptionGUI(root)
root.mainloop()