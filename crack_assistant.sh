#!/bin/bash

# Domyślna ścieżka do słownika na maszynach Kali Linux oraz TryHackMe
WORDLIST="/usr/share/wordlists/rockyou.txt"

# 1. Sprawdzenie, czy użytkownik podał plik z hashem jako argument
if [ -z "$1" ]; then
    echo "Użycie: $0 <plik_z_hashem.txt>"
    exit 1
fi

HASH_FILE=$1

# 2. Sprawdzenie, czy wskazany plik fizycznie istnieje w systemie
if [ ! -f "$HASH_FILE" ]; then
    echo "[-] Błąd: Plik $HASH_FILE nie istnieje."
    exit 1
fi

# 3. Pobranie samego hasha z pliku i usunięcie z niego spacji oraz znaków nowej linii
HASH_STRING=$(tr -d '[:space:]' < "$HASH_FILE")
LENGTH=${#HASH_STRING}

echo "[*] Analiza hasha z pliku: $HASH_FILE"
echo "[*] Długość hasha: $LENGTH znaków"

FORMAT=""

# 4. Logika automatycznego dopasowania formatu Johna na podstawie długości tekstu
case $LENGTH in
    32)
        FORMAT="raw-md5"
        ;;
    40)
        FORMAT="raw-sha1"
        ;;
    64)
        FORMAT="raw-sha256"
        ;;
    128)
        # Rozstrzygnięcie specyficznego dla laboratoriów formatu Whirlpool
        echo "[?] Hash ma 128 znaków. Wybierz odpowiedni format:"
        echo "1) raw-whirlpool"
        echo "2) raw-sha512"
        read -p "Twój wybór (1 lub 2): " choice
        if [ "$choice" == "1" ]; then
            FORMAT="raw-whirlpool"
        else
            FORMAT="raw-sha512"
        fi
        ;;
    *)
        # Dodatkowa weryfikacja dla formatów systemowych typu Crypt
        if [[ "$HASH_STRING" == \$1\$* ]]; then
            FORMAT="md5crypt"
        elif [[ "$HASH_STRING" == \$5\$* ]]; then
            FORMAT="sha256crypt"
        elif [[ "$HASH_STRING" == \$6\$* ]]; then
            FORMAT="sha512crypt"
        else
            echo "[-] Nie rozpoznano formatu automatycznie."
            read -p "Wpisz format ręcznie (np. raw-md5): " FORMAT
        fi
        ;;
esac

# 5. Uruchomienie narzędzia John the Ripper
if [ -n "$FORMAT" ]; then
    echo "[+] Wybrany format dla John: $FORMAT"
    echo "[*] Uruchamianie John the Ripper ze słownikiem rockyou.txt..."
    
    # Wywołanie głównego procesu łamania
    john --format=$FORMAT --wordlist=$WORDLIST "$HASH_FILE"
    
    # Automatyczne wyświetlenie odszyfrowanego hasła w konsoli
    echo -e "\n[*] Sprawdzanie i wyświetlanie wyniku końcowego:"
    john --show --format=$FORMAT "$HASH_FILE"
fi
