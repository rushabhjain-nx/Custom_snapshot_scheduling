
from cryptography.fernet import Fernet
from django.conf import settings

# Initialize the cipher suite using the encryption key from settings
cipher_suite = Fernet(settings.ENCRYPTION_KEY.encode())


def encrypt_text(plain_text):
    """Encrypts a plain text string."""
    encoded_text = plain_text.encode('utf-8')
    encrypted_text = cipher_suite.encrypt(encoded_text)
    return encrypted_text.decode('utf-8')

def decrypt_text(encrypted_text):
    """Decrypts an encrypted string."""
    decoded_encrypted_text = encrypted_text.encode('utf-8')
    decrypted_text = cipher_suite.decrypt(decoded_encrypted_text)
    return decrypted_text.decode('utf-8')