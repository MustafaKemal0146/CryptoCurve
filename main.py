import os
import time
from ecdsa import SECP256k1, SigningKey
import string
import subprocess
import unidecode
from termcolor import colored

def clear_screen():
    # Farklı işletim sistemleri için ekran temizleme
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    try:
        # Figlet ile başlık oluşturma
        banner = subprocess.check_output(['figlet', 'CryptoCurve'], universal_newlines=True)
        print(colored(banner, 'green'))
        print(colored("=" * 50, 'green'))
        time.sleep(1)
    except:
        # Eğer figlet kurulu değilse basit bir başlık
        print(colored("===== CryptoCurve =====", 'green'))

# 1. Anahtar üretimi
def generate_keys():
    sk = SigningKey.generate(curve=SECP256k1)  # Özel anahtar
    vk = sk.get_verifying_key()  # Halka anahtarı (public key)
    return sk, vk

# 2. Her harf için benzersiz bir sayı
def letter_to_number(letter):
    # Türkçe karakterleri ASCII'ye çevir
    letter = unidecode.unidecode(letter.upper())
    return string.ascii_uppercase.index(letter)  # A=0, B=1, C=2, ...

def number_to_letter(number):
    return string.ascii_uppercase[number % 26]

# 3. Eliptik eğri ile şifreleme
def encrypt_message(message, public_key):
    encrypted_message = []
    # Anahtarın x koordinatını al
    key_value = int.from_bytes(public_key.to_string(), byteorder='big')
    
    # Türkçe karakterleri ASCII'ye çevir
    message = unidecode.unidecode(message.upper())
    
    for letter in message:
        if letter.isalpha():
            num = letter_to_number(letter)
            encrypted_num = (num + key_value) % 26  # Eliptik eğri üzerindeişlem
            encrypted_message.append(number_to_letter(encrypted_num))
        else:
            encrypted_message.append(letter)  # Boşluklar veya özel karakterler olduğu gibi bırakılır
    return ''.join(encrypted_message)

# 4. Şifreyi çözme
def decrypt_message(encrypted_message, encryption_key):
    decrypted_message = []
    
    for letter in encrypted_message.upper():
        if letter.isalpha():
            encrypted_num = letter_to_number(letter)
            decrypted_num = (encrypted_num - encryption_key) % 26
            decrypted_message.append(number_to_letter(decrypted_num))
        else:
            decrypted_message.append(letter)  # Boşluklar veya özel karakterler olduğu gibi bırakılır
    return ''.join(decrypted_message)

# Kullanıcıdan işlem seçmesini istemek
def main_menu():
    while True:
        clear_screen()
        print_banner()
        print(colored("\n--- Ana Menü ---", 'green'))
        print(colored("1. Şifreleme Yap", 'green'))
        print(colored("2. Şifre Çözme Yap", 'green'))
        print(colored("3. Çıkış", 'green'))
        choice = input(colored("Yapmak istediğiniz işlemi seçin (1/2/3): ", 'green'))

        if choice == '1':
            # Anahtarları oluştur
            private_key, public_key = generate_keys()

            # Mesaj al
            original_message = input("Şifrelenecek mesajı girin: ")
            print(colored("Orijinal Mesaj:", 'green'), original_message)

            # Şifreleme
            encrypted_message = encrypt_message(original_message, public_key)
            print(colored("Şifreli Mesaj:", 'green'), encrypted_message)
            print(colored("Şifreleme Anahtarı:", 'green'), int.from_bytes(public_key.to_string(), byteorder='big'))

        elif choice == '2':
            # Şifreli mesaj al
            encrypted_message = input("Çözülecek şifreli mesajı girin: ")
            
            # Şifreleme anahtarını al
            try:
                encryption_key = int(input("Şifreleme anahtarını girin: "))
            except ValueError:
                print(colored("Geçersiz anahtar. Lütfen sayısal bir değer girin.", 'red'))
                time.sleep(2)
                continue

            # Şifreyi çözme
            decrypted_message = decrypt_message(encrypted_message, encryption_key)
            print(colored("Çözülmüş Mesaj:", 'green'), decrypted_message)

        elif choice == '3':
            print(colored("Programdan çıkılıyor...", 'green'))
            break  # Çıkış yap

        else:
            print(colored("Geçersiz seçim. Lütfen tekrar deneyin.", 'red'))
            time.sleep(2)
            continue

        # Ana menüye dönmek istiyor musunuz?
        input(colored("\nDevam etmek için Enter'a basın...", 'green'))
        
# Programı başlat
if __name__ == "__main__":
    clear_screen()
    print_banner()
    main_menu()
