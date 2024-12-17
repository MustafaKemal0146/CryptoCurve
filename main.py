from ecdsa import SECP256k1, SigningKey
import string

# 1. Anahtar üretimi
def generate_keys():
    sk = SigningKey.generate(curve=SECP256k1)  # Özel anahtar
    vk = sk.verifying_key  # Halka anahtarı (public key)
    return sk, vk

# 2. Her harf için benzersiz bir sayı
def letter_to_number(letter):
    return string.ascii_uppercase.index(letter)  # A=0, B=1, C=2, ...

def number_to_letter(number):
    return string.ascii_uppercase[number]

# 3. Eliptik eğri ile şifreleme
def encrypt_message(message, public_key):
    encrypted_message = []
    for letter in message.upper():
        if letter.isalpha():
            num = letter_to_number(letter)
            encrypted_num = (num + public_key.pubkey.pointQ.x()) % 26  # Eliptik eğri üzerinde işlem
            encrypted_message.append(number_to_letter(encrypted_num))
        else:
            encrypted_message.append(letter)  # Boşluklar veya özel karakterler olduğu gibi bırakılır
    return ''.join(encrypted_message)

# 4. Şifreyi çözme
def decrypt_message(encrypted_message, private_key):
    decrypted_message = []
    for letter in encrypted_message.upper():
        if letter.isalpha():
            encrypted_num = letter_to_number(letter)
            decrypted_num = (encrypted_num - private_key.privkey.secretMultiplier()) % 26
            decrypted_message.append(number_to_letter(decrypted_num))
        else:
            decrypted_message.append(letter)  # Boşluklar veya özel karakterler olduğu gibi bırakılır
    return ''.join(decrypted_message)

# Test kodu
if __name__ == "__main__":
    # Anahtarları oluştur
    private_key, public_key = generate_keys()

    # Mesaj
    original_message = "HELLO WORLD"
    print("Orijinal Mesaj:", original_message)

    # Şifreleme
    encrypted_message = encrypt_message(original_message, public_key)
    print("Şifreli Mesaj:", encrypted_message)

    # Şifreyi çözme
    decrypted_message = decrypt_message(encrypted_message, private_key)
    print("Çözülmüş Mesaj:", decrypted_message)
