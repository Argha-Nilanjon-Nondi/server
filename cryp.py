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
  
    chunk_size = 16 #bytes Adjust the chunk size as per your requirement
    
    
    symmetric_key = os.urandom(32)
    cbc=os.urandom(16)
    h.append(cbc)
    encrypted_file=open("encrypted_content","ab")
    
    print("algk s ",algorithms.AES.block_size)
    
    cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(cbc), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = PKCS7(algorithms.AES.block_size).padder()
    
    with open(input_file,"rb") as file:
         while True:
            chunk = file.read(chunk_size)
            if len(chunk)<chunk_size:
              chunk = padder.update(chunk)
            if(len(chunk)==0):
               break
            encrypted_chunk=encryptor.update(chunk)
            encrypted_file.write(encrypted_chunk)
         final_chunk = encryptor.finalize()
         encrypted_file.write(final_chunk)

    
    encrypted_key = public_key.encrypt(
        symmetric_key,padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
    )
    
    
    encrypted_key_file=open("encrypted_key","wb")
    encrypted_key_file.write(encrypted_key)
    encrypted_key_file.close()
    encrypted_file.close()
    file.close()
    
    return True

def decrypt_file(encrypted_file,encrypted_key_file,private_key):
    
    chunk_size=16
    encrypted_key_file=open(encrypted_key_file,"rb")
    encrypted_key=encrypted_key_file.read()
    encrypted_key_file.close()
    
    
    decrypted_file=open("a99.png","ab")
    
    cbc=h[0]
        
    symmetric_key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                     algorithm=hashes.SHA256(),
                     label=None)
    )
    
    cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(cbc), backend=default_backend())
    
    decryptor = cipher.decryptor()
    
    with open(encrypted_file,"rb") as encrypted_file:
       while True:
         chunk = encrypted_file.read(chunk_size)
         if not chunk:
            break
         else:
            decrypted_chunk = decryptor.update(chunk)
            decrypted_file.write(decrypted_chunk)
       final_chunk = decryptor.finalize()
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

# Encrypt and decrypt a file
input_file = "img2.png"
encrypted_file = 'encrypted.txt'
decrypted_file = 'decrypted.txt'

print(encrypt_file(input_file, loaded_public_key))
#decrypt_file(encrypted_file, decrypted_file, loaded_private_key)
decrypt_file("encrypted_content","encrypted_key",loaded_private_key)
print("File encryption and decryption completed.")
