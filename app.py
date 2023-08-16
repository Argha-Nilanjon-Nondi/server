from flask import Flask, jsonify, request, send_file
from lib.cryptographic import load_key,decrypt_file
from lib.denoise import remove_all_noise

import base64
import json

app = Flask(__name__)
loaded_private_key = load_key('private_key.pem')

@app.route('/api/upload', methods=['POST'])
def upload():
  request_data=json.loads(request.json)
  file_name = request_data["file_name"]
  file_content=request_data["file_content"]
  
  encrypted_content=base64.b64decode(file_content.encode())
  decrypted_content=decrypt_file(encrypted_content,loaded_private_key)
  
  decrypted_file=open(file_name,"wb")
  decrypted_file.write(decrypted_content)
  decrypted_file.close()
  
  new_filepath=remove_all_noise(file_name)
  
  return send_file(new_filepath,as_attachment=False)

if __name__ == '__main__':
    app.run(debug=True)
