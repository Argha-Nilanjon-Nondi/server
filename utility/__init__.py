import random

def filename_generator(filename,text="",ext="wav"):
    rn = random.randint(1, 1000000)
    new_filename=(filename.split(".")[0])+"_"+str(rn)+"_"+text+"."+ext
    return new_filename