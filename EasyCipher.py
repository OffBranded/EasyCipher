import string
import time
import os

def clean_input(text):
    return ''.join([c for c in text if c in string.ascii_letters + " ,.\n"])

def vigenere_cipher(text, key, encrypt=True):
    result = []
    key = key.lower()
    key_index = 0
    for char in text:
        if char.lower() in string.ascii_lowercase:
            shift = ord(key[key_index % len(key)]) - ord('a')
            if not encrypt:
                shift = -shift
            base = ord('A') if char.isupper() else ord('a')
            result.append(chr((ord(char) - base + shift) % 26 + base))
            key_index += 1
        else:
            result.append(char)
    return ''.join(result)

def caesar_decrypt(text, shift):
    result = []
    for char in text:
        if char.lower() in string.ascii_lowercase:
            base = ord('A') if char.isupper() else ord('a')
            result.append(chr((ord(char) - base - shift) % 26 + base))
        else:
            result.append(char)
    return ''.join(result)

def caesar_cipher(text, shift, encrypt=True):
    result = []
    for char in text:
        if char.lower() in string.ascii_lowercase:
            if not encrypt:
                shift = -shift
            base = ord('A') if char.isupper() else ord('a')
            result.append(chr((ord(char) - base + shift) % 26 + base))
        else:
            result.append(char)
    return ''.join(result)

def display_progress(current, total):
    percent = int((current / total) * 100)
    bar = "#" * (percent // 2) + "-" * (50 - percent // 2)
    print(f"Progress: [{bar}] {percent}% ({current}/{total})", end="\r")

def count_words(text):
    return len(text.split())

def create_key_info(key):
    return key[0].upper(), len(key[1]), key[2].upper()

def ask_yes_no(prompt):
    while True:
        response = input(f"{prompt} [Y/N]: ").strip().lower()
        if response in ["y", "n"]:
            return response == "y"
        print("Please enter Y or N.")

def process_cipher(text, key_parts, action):
    words = text.split()
    total_words = len(words)

    first, second, third = create_key_info(key_parts)
    current_word = 0
    result_text = text

    for word in words:
        if action == 'encrypt':
            result_text = vigenere_cipher(result_text, key_parts[0])
            result_text = caesar_cipher(result_text, second)
            result_text = vigenere_cipher(result_text, key_parts[2])
        else:
            result_text = vigenere_cipher(result_text, key_parts[2], encrypt=False)
            result_text = caesar_decrypt(result_text, second)
            result_text = vigenere_cipher(result_text, key_parts[0], encrypt=False)

        current_word += 1
        display_progress(current_word, total_words)
        delay = 0.05 + len(word) * 0.01
        time.sleep(delay)

    print("\n")
    return result_text

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def set_window_title(title):
    os.system(f'title {title}' if os.name == 'nt' else f'echo -n -e "\033]0;{title}\007"')

def main():
    set_window_title("EasyCipher  I  by off01")  # Change the window title here
    clear()
    print("\nSelect an option:")
    print("[1] Cipher")
    print("[2] Decipher")
    print("[3] Exit")

    while True:
        action = input("Selection: ").strip()
        if action == "1":
            action_type = "encrypt"
            break
        elif action == "2":
            action_type = "decrypt"
            break
        elif action == "3":
            print("\nGoodbye!\n")
            exit()
        else:
            print("Invalid option. Please enter 1, 2, or 3.")

    while True:
        key_input = input("\nEnter key (3 words, letters only): ").strip()
        key_parts = key_input.split()
        if len(key_parts) == 3 and all(part.isalpha() for part in key_parts):
            break
        print("Invalid key. Try again.")

    print(f"Key: {key_input}")

    if action_type == "encrypt":
        raw_text = input("\nEnter text to cypher: ")
    else:
        encrypted_text = input("\nEnter text to decypher: ")

    text = clean_input(raw_text if action_type == "encrypt" else encrypted_text)
    print(f"\nText: {text}")

    if not ask_yes_no("\nProceed?"):
        print("\nReturning to menu...\n")
        main()  # This line will return to the menu if user chooses "N"
        return

    final_text = process_cipher(text, key_parts, action_type)

    print("Final result:")
    print(final_text.strip())

    print("\nWhat would you like to do next?")
    print("[1] Menu")
    print("[2] Exit")

    while True:
        next_action = input("Selection: ").strip()
        if next_action == "2":
            print("\nGoodbye!\n")
            break
        elif next_action == "1":
            main()
            break
        else:
            print("\nInvalid option. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
