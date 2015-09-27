import numpy as np
from FlaskWebProject.audio_detector import mod
from sklearn.ensemble import RandomForestClassifier
import logging
from FlaskWebProject import app
import os
import pickle


def extract_one(signal, rate):
    
    
    sample_rate = rate/64.0
    nsample = np.floor(len(signal)/64.0)
    nmod = int(np.floor(nsample/2.0)+1)
    
    hz_spec = mod.hz_spec(signal, rate)
    hz_mod = mod.linear_mod(hz_spec, nsample)
    hz_logmod = mod.log_mod(hz_mod, nmod)
    
    return hz_logmod.flatten().tolist()



def run_detector(signal, sample_rate):
    
    app.logger.info('Extracting features')

    if len(signal) < int(sample_rate*1):
        signal = np.append(signal, np.zeros(int(sample_rate*1) - len(signal)))

    hz_logmod = extract_one(signal, sample_rate)

    a = 'FlaskWebProject'
    b = 'audio_detector'
    c = 'Forest'
    file_name = 'InsectForest.pkl'

    file_with_path = os.path.join(a, b, c, file_name)

    with open(file_with_path, 'rb') as f:
        forest = pickle.load(f)

    probabilities = forest.predict_proba(hz_logmod)

    return probabilities