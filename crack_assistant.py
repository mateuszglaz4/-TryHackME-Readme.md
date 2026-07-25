#!/usr/bin/env python3
import sys
import os
import subprocess

# Domyślna ścieżka do słownika na systemach takich jak Kali Linux czy maszyny TryHackMe
WORDLIST_PATH = "/usr/share/wordlists/rockyou.txt"

def analyze_and_crack(file_path):
    # 1. Sprawdzenie czy plik z hashem w ogóle istnieje
    if not os.path.exists(file_path):
        print(f"[-] Błąd: Plik '{file_path}' nie istnieje.")
        return

    # 2. Odczyt hasha i oczyszczenie go ze zbędnych spacji czy znaków nowej linii
    with open(file_path, 'r') as f:
        hash_string = f.read().strip()

    length = len(hash_string)
    print(f"[*] Analiza hasha z pliku: {file_path}")
    print(f"[*] Długość hasha: {length} znaków")

    jtr_format = ""

    # 3. Logika automatycznego dobierania formatu dla John the Ripper
    if length == 32:
        jtr_format = "raw-md5"
    elif length == 40:
        jtr_format = "raw-sha1"
    elif length == 64:
        jtr_format = "raw-sha256"
    elif length == 128:
        # Obsługa specyficznych przypadków z laboratoriów (Whirlpool vs SHA-512)
        print("[?] Hash ma 128 znaków. Wybierz odpowiedni format:")
        print("1) raw-whirlpool (np. zaawansowane zadania THM)")
        print("2) raw-sha512 (standardowy SHA-512)")
        choice = input("Wybór (1 lub 2): ").strip()
        jtr_format = "raw-whirlpool" if choice == "1" else "raw-sha512"
    elif hash_string.startswith("$1$"):
        jtr_format = "md5crypt"
    elif hash_string.startswith("$5$"):
        jtr_format = "sha256crypt"
    elif hash_string.startswith("$6$"):
        jtr_format = "sha512crypt"
    else:
        print("[-] Nie udało się automatycznie dopasować formatu.")
        jtr_format = input("Wpisz format ręcznie (np. raw-md5): ").strip()

    # 4. Uruchomienie procesu łamania, jeśli format został ustalony
    if jtr_format:
        print(f"[+] Wybrany format dla John: {jtr_format}")
        print("[*] Uruchamianie John the Ripper ze słownikiem rockyou.txt...")
        
        # Budowanie komendy systemowej
        cmd = [
            "john",
            f"--format={jtr_format}",
            f"--wordlist={WORDLIST_PATH}",
            file_path
        ]
        
        try:
            # Subprocess.run wykonuje komendę bezpośrednio w systemie Linux
            subprocess.run(cmd, check=True)
            
            # Automatyczne wyświetlenie odszyfrowanego hasła po zakończeniu działania
            print("\n[*] Sprawdzanie i wyświetlanie wyniku końcowego:")
            show_cmd = ["john", "--show", f"--format={jtr_format}", file_path]
            subprocess.run(show_cmd)
            
        except subprocess.CalledProcessError as e:
            print(f"[-] Wystąpił błąd podczas pracy programu John: {e}")
        except FileNotFoundError:
            print("[-] Błąd: Program 'john' nie jest zainstalowany w tym systemie.")

if __name__ == "__main__":
    # Sprawdzenie czy użytkownik podał nazwę pliku jako argument (np. python3 script.py hash.txt)
    if len(sys.argv) < 2:
        print(f"Użycie: python3 {sys.argv[0]} <plik_z_hashem.txt>")
        sys.exit(1)
        
    analyze_and_crack(sys.argv[1])
