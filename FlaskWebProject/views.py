"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import Flask, render_template, request, redirect
from werkzeug import secure_filename
from FlaskWebProject import app

from FlaskWebProject.audio_detector import detector
import os
import logging

# not natively included on Azure
from scipy.io import wavfile
import wave
import numpy as np
import sys

# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['wav'])



logs = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    )
    

logs.setFormatter(formatter)
app.logger.addHandler(logs)
app.logger.setLevel(logging.DEBUG)



@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Upload a File'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About'
    )

@app.route('/record')
def record():
    return render_template(
        'record.html',
        title='Record Sound'
    )

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

			
# Route that will process the file upload
@app.route('/results', methods=['POST'])
def upload():

    try:
        # Get the name of the uploaded file
        app.logger.info('Checking file')
        file = request.files['file']
        # Check if the file is one of the allowed types/extensions

        if file and allowed_file(file.filename.lower()):
            app.logger.info('File is valid')
            
            filename = secure_filename(file.filename)
            
            app.logger.info('Start processing')
            result_list = process_audio_file(file, filename)

            app.logger.info(result_list)
            # return result
            return render_template(
                'results.html', 
                title='Results',
                year=datetime.now().year,
                result=result_list
            )

        else:
            app.logger.warning('File not found or not a wav file')
            return render_template(
                'results.html',
                title='Results',
                year=datetime.now().year,
                result=[0]
            )
    except Exception as e:
        app.logger.warning('Some thing wrong with the server')

        return render_template(
            'results.html',
            title='Results',
            year=datetime.now().year,
            result=[str(e)]
        )



def process_audio_file(file, file_name):
    """"Loads a wav file and runs a dummy detector on it"""
    #read file
    app.logger.info('Reading file')

    wav_reader = wave.open(file,'r')
    nchannels = wav_reader.getnchannels()
    sampwidth = wav_reader.getsampwidth()
    nframes = wav_reader.getnframes()
    data = wav_reader.readframes(nframes) 
    sampling_rate = wav_reader.getframerate()
    audio_samples = _wav2array(nchannels, sampwidth, data)

    wav_reader.close()

    if nchannels > 1:
        mono = np.mean(audio_samples, axis=1)
    else:
        mono = np.array(audio_samples).T.tolist()[0]

    file_duration = audio_samples.shape[0] / float(sampling_rate)

    app.logger.info('Start classification')
    predictions = detector.run_detector(mono, sampling_rate)
    
    
    probs = []
    probabilities = predictions[0]
    for i in range (len(probabilities)):
        probs.append(str(round(probabilities[i], 2)))

    app.logger.info('Got results')


    summary = []
    summary.append(os.path.basename(file_name))
    summary.append(str(round(file_duration, 2)))
    summary.append(str(sampling_rate))

    app.logger.info('Ready to show results')

    result = summary+probs
 
    return result



def _wav2array(nchannels, sampwidth, data):
    """data must be the string containing the bytes from the wav file."""
    num_samples, remainder = divmod(len(data), sampwidth * nchannels)
    if remainder > 0:
        app.logger.info('The length of data is not a multiple of '
                         'sampwidth * num_channels.')
        raise ValueError('The length of data is not a multiple of '
                         'sampwidth * num_channels.')
    if sampwidth > 4:
        app.logger.info("sampwidth must not be greater than 4.")
        raise ValueError("sampwidth must not be greater than 4.")

    if sampwidth == 3:
        a = np.empty((num_samples, nchannels, 4), dtype=np.uint8)
        raw_bytes = np.fromstring(data, dtype=np.uint8)
        a[:, :, :sampwidth] = raw_bytes.reshape(-1, nchannels, sampwidth)
        a[:, :, sampwidth:] = (a[:, :, sampwidth - 1:sampwidth] >> 7) * 255
        result = a.view('<i4').reshape(a.shape[:-1])
    else:
        # 8 bit samples are stored as unsigned ints; others as signed ints.
        dt_char = 'u' if sampwidth == 1 else 'i'
        a = np.fromstring(data, dtype='<%s%d' % (dt_char, sampwidth))
        result = a.reshape(-1, nchannels)
    return result

            
   


