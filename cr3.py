from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

file=open("public_key.pem","rb")
public_key = file.read()

data=open("img.png","rb").read()
file.close()

cipher = AES.new(key, AES.MODE_CBC, iv)
paddeddata = Padding.pad(data, 16)
encrypteddata = cipher.encrypt(paddeddata)
        
  