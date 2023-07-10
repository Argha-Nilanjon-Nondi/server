from IPython import display as disp
import torch
import torchaudio
from denoiser import pretrained
from denoiser.dsp import convert_audio
from scipy.io import wavfile
import numpy as np
import random

def remove_all_noise(filename):
    model = pretrained.dns64().cpu()
    wav, sr = torchaudio.load(filename)
    wav = convert_audio(wav.cpu(), sr, model.sample_rate, model.chin)
    with torch.no_grad():
         denoised = model(wav[None])[0]
         data=denoised.data.cpu().numpy()
         data=np.squeeze(data)
         new_filename=filename_generator(filename,text="denoised")
         wavfile.write(new_filename,model.sample_rate,data)
         return new_filename