from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
from cryptography.hazmat.primitives.padding import PKCS7
 
h=[]

def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def save_key_to_file(key, filename):
  
    key_file=open(filename, "wb")
    
    if("public" in filename):
      binary_data=key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo)
      key_file.write(binary_data)

    if("private" in filename):
      binary_data=key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption())
      key_file.write(binary_data)
  
    key_file.close()

def load_key(filename):
    key_file=open(filename, "rb")
    if("public" in filename):
       print("hi lol")
       key = serialization.load_pem_public_key(
           key_file.read(),
           backend=default_backend()
          )
    if("private" in filename):
         key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    key_file.close()
    return key


def encrypt_file(input_file, public_key):
    """
     Generate encrypted data 
   
    Args:
        input_file (string): Path of the file
        public_key (_RSAPublicKey object): object from loaded_public_key
        
    Return:
          bytes :encrypted data of input file
     
    """
  
    chunk_size = 245 #bytes 
    final_chunk=b""
    
    with open(input_file,"rb") as file:
         while True:
            chunk = file.read(chunk_size)
            if(len(chunk)==0):
               break
            encrypted_chunk=public_key.encrypt(
                          chunk,padding.PKCS1v15())
            final_chunk+=encrypted_chunk
            
    encrypted_file=open("encrypted_content","ab")      
    encrypted_file.write(final_chunk)
    encrypted_file.close()
    file.close()
    
    return True

def decrypt_file(encrypted_file,private_key):
    
    chunk_size=256
    final_chunk=b""
  
    with open(encrypted_file,"rb") as encrypted_file:
       while True:
         chunk = encrypted_file.read(chunk_size)
         if not chunk:
            break
         else:
            decrypted_chunk = private_key.decrypt(
                              chunk,
                              padding.PKCS1v15()
                                )
            final_chunk+=decrypted_chunk
            
    
    decrypted_file=open("a9hhh9.png","ab")
    decrypted_file.write(final_chunk)
    encrypted_file.close()
    decrypted_file.close()

# Generate the key pair
#private_key, public_key = generate_key_pair()

#save_key_to_file(private_key, 'private_key.pem')
#save_key_to_file(public_key, 'public_key.pem')

# Load the keys from files
loaded_private_key = load_key('private_key.pem')
loaded_public_key =  load_key('public_key.pem')
print(loaded_public_key)
# Encrypt and decrypt a file
input_file = "006.jpg"
encrypted_file = 'encrypted.txt'
decrypted_file = 'decrypted.txt'

print(encrypt_file(input_file, loaded_public_key))
#decrypt_file(encrypted_file, decrypted_file, loaded_private_key)
decrypt_file("encrypted_content",loaded_private_key)
print("File encryption and decryption completed.")
