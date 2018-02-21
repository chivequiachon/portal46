from cryptography.fernet import Fernet

from django.conf import settings


def encode(text):
  cipher = Fernet(settings.FERNET_CIPHER_KEY)
  
  # Convert text to byte
  byte_text = str.encode(text)
  
  # Encrypt
  byte_encrypted_text = cipher.encrypt(byte_text)
  
  # convert encrypted byte text to simple string
  encrypted_text = byte_encrypted_text.decode()
  
  return encrypted_text
  

def decode(text):
  cipher = Fernet(settings.FERNET_CIPHER_KEY)
  
  # Convert text to byte
  byte_text = str.encode(text)
  
  # Encrypt
  byte_decrypted_text = cipher.decrypt(byte_text)
  
  # Convert decrypted byte text to simple string
  decrypted_text = byte_decrypted_text.decode()
  
  return decrypted_text
