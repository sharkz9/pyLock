# PyLock File Encryption GUI

PyLock is a Python file encryption graphical user interface (GUI) that allows you to encrypt and decrypt files using the Advanced Encryption Standard (AES) algorithm.

## Installation

To use PyLock, you will need to have Python 3.x and the following packages installed:

-   `tkinter`
-   `pycryptodome`

You can install the required packages by running the following command:

Copy code

`pip install tkinter pycryptodome` 

## Usage

To use PyLock, simply run the `pylock.py` file using Python:

`python pylock.py` 

Once the GUI is running, you can select a file to encrypt or decrypt by clicking the "Browse Files" button and selecting a file from your file system.

To encrypt a file, click the "Generate Key" button to generate a random encryption key, enter the key into the "Enter encryption key" field, and click the "Encrypt" button. The encrypted file will be saved with the extension `.enc` in the same directory as the original file.

To decrypt a file, select the encrypted file, enter the encryption key into the "Enter encryption key" field, and click the "Decrypt" button. The decrypted file will be saved in the same directory as the encrypted file with the extension `.dec`.
