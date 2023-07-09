from flask import Flask, jsonify, request
from lib.cryptographic import load_key,decrypt_file
import base64
import json


from IPython import display as disp
import torch
import torchaudio
from denoiser import pretrained
from denoiser.dsp import convert_audio
from scipy.io import wavfile
import numpy as np
import random


def remove_all_noise(filename):
    model = pretrained.dns64().cuda()
    wav, sr = torchaudio.load(filename)
    wav = convert_audio(wav.cuda(), sr, model.sample_rate, model.chin)
    with torch.no_grad():
         denoised = model(wav[None])[0]
         data=denoised.data.cpu().numpy()
         data=np.squeeze(data)
         new_filename=filename_generator(filename,text="denoised")
         wavfile.write(new_filename,model.sample_rate,data)
         return new_filename

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
  
  remove_all_noise(file_name)
  
  return "lol"

if __name__ == '__main__':
    app.run(debug=True)
