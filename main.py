import os
import time
from ecdsa import SECP256k1, SigningKey
import string
import subprocess

def clear_screen():
    # Farklı işletim sistemleri için ekran temizleme
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    try:
        # Figlet ile başlık oluşturma
        banner = subprocess.check_output(['figlet', 'CryptoCurve'], universal_newlines=True)
        print(banner)
        print("=" * 50)
        time.sleep(1)
    except:
        # Eğer figlet kurulu değilse basit bir başlık
        print("===== CryptoCurve =====")

# 1. Anahtar üretimi
def generate_keys():
    sk = SigningKey.generate(curve=SECP256k1)  # Özel anahtar
    vk = sk.get_verifying_key()  # Halka anahtarı (public key)
    return sk, vk

# 2. Her harf için benzersiz bir sayı
def letter_to_number(letter):
    return string.ascii_uppercase.index(letter)  # A=0, B=1, C=2, ...

def number_to_letter(number):
    return string.ascii_uppercase[number % 26]

# 3. Eliptik eğri ile şifreleme
def encrypt_message(message, public_key):
    encrypted_message = []
    # Anahtarın x koordinatını al
    key_value = int.from_bytes(public_key.to_string(), byteorder='big')
    
    for letter in message.upper():
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
        print("\n--- Ana Menü ---")
        print("1. Şifreleme Yap")
        print("2. Şifre Çözme Yap")
        print("3. Çıkış")
        choice = input("Yapmak istediğiniz işlemi seçin (1/2/3): ")

        if choice == '1':
            # Anahtarları oluştur
            private_key, public_key = generate_keys()

            # Mesaj al
            original_message = input("Şifrelenecek mesajı girin: ")
            print("Orijinal Mesaj:", original_message)

            # Şifreleme
            encrypted_message = encrypt_message(original_message, public_key)
            print("Şifreli Mesaj:", encrypted_message)
            print("Şifreleme Anahtarı:", int.from_bytes(public_key.to_string(), byteorder='big'))

        elif choice == '2':
            # Şifreli mesaj al
            encrypted_message = input("Çözülecek şifreli mesajı girin: ")
            
            # Şifreleme anahtarını al
            try:
                encryption_key = int(input("Şifreleme anahtarını girin: "))
            except ValueError:
                print("Geçersiz anahtar. Lütfen sayısal bir değer girin.")
                time.sleep(2)
                continue

            # Şifreyi çözme
            decrypted_message = decrypt_message(encrypted_message, encryption_key)
            print("Çözülmüş Mesaj:", decrypted_message)

        elif choice == '3':
            print("Programdan çıkılıyor...")
            break  # Çıkış yap

        else:
            print("Geçersiz seçim. Lütfen tekrar deneyin.")
            time.sleep(2)
            continue

        # Ana menüye dönmek istiyor musunuz?
        input("\nDevam etmek için Enter'a basın...")
        
# Programı başlat
if __name__ == "__main__":
    clear_screen()
    print_banner()
    main_menu()
