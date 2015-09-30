Simple demo Flask web application for uploading audio file, processing it, and returning results. 

For more details on how to set up on Azure Web Apps consult the following Google Doc:
https://docs.google.com/document/d/1c6eP99_YQOO-P9uHyUuCyRJ2SBLKmy1bGyX2zHn5jfY/edit?usp=sharing



The web pages send wav files to the server, the sever returns a list of data which contains: file name, duration, sample rate and porbabilities of each class.

The wav file can either be uploaded from local file system or recorded by the web browser. The recording page makes use of getUserMedia API, this API is currently not supported by IE and Safari, and all browsers on iOS devices (iphone, iPad, iPod). 


The external libraries used are: numpy, scipy, scikit_learn and matplotlib


Other python modules:

1. build_forest.py

	This python code runs every time when the web app starts running. It reads a csv file (insects.csv) which contains data of a tranning set (logmod of insect sound samples) and builds a random forest with scikit_learn. Then is saves the trained random forest as a pickle file (InsectForest.pkl) in the Forest folder. 


2. detector.py
	
	Processes and classifies the wav file, then returns the probabilities of each class. 

2. mfcc.py

	Contains functions for calculating MFCC. Here we only use the one which calulate the frequency spectrum of a wav.

3. mod.py

	contains functions for calculating logmod of a wav. 