from cryptography.fernet import Fernet

# Generate a new key
key = Fernet.generate_key()

# Print the key (you should store this securely)
print(key.decode())
