import fast_file_encryption as ffe
from pathlib import Path
original_file = Path('img.png')
encryptor = ffe.Encryptor(ffe.read_public_key(Path('public_key.pem')))
encrypted_file = Path('encrypted_file')
#encryptor.copy_encrypted(original_file, encrypted_file)
#encrypted_file = Path('encrypted_file')
#decryptor = ffe.Decryptor(ffe.read_private_key(Path('private_key.pem')))
#data=decryptor.load_decrypted(encrypted_file)
#open("a.png","wb").write(data)