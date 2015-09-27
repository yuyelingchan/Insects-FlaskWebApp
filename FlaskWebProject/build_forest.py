import pickle
from sklearn.ensemble import RandomForestClassifier
import csv
import numpy
import os



def forest():

    a = 'FlaskWebProject'
    b = 'audio_detector'
    c = 'Forest'
    file_name = 'InsectForest.pkl'

    csv_name = os.path.join(a, b, 'insects.csv')
    csv_file = open(csv_name,'r') 
    file_reader = csv.reader(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        
    x = []
    y = []

    for row in file_reader:

            
        if row[0] == "Cicadidae(cicada)":
            li = row[1:]
            logmod = []
            for i in range(len(li)):
                logmod.append(float(li[i]))
                
            x.append(logmod)
            y.append(0)
            
        elif row[0] == "Tettigoniidae(bush cricket)":
            li = row[1:]
            logmod = []
            for i in range(len(li)):
                logmod.append(float(li[i]))
                
            x.append(logmod)
            y.append(1)
            
        elif row[0] == "Gryllidae(cricket)":
            li = row[1:]
            logmod = []
            for i in range(len(li)):
                logmod.append(float(li[i]))
                
            x.append(logmod)
            y.append(2)
            
        elif row[0] == "Acrididae(grasshopper)":
            li = row[1:]
            logmod = []
            for i in range(len(li)):
                logmod.append(float(li[i]))
                
            x.append(logmod)
            y.append(3)
            
        elif row[0] == "Gryllotalpidae(mole cricket)":
            li = row[1:]
            logmod = []
            for i in range(len(li)):
                logmod.append(float(li[i]))
            
            x.append(logmod)
            y.append(4)
        
        elif row[0] == "No Insect":
            li = row[1:]
            logmod = []
            for i in range(len(li)):
                logmod.append(float(li[i]))
            
            x.append(logmod)
            y.append(5)
            
            
    forest = RandomForestClassifier(n_estimators=60, min_samples_split=1, max_depth=16)

    forest.fit(x, y)


    file_with_path = os.path.join(a, b, c, file_name)
    with open(file_with_path, 'wb') as f:
        pickle.dump(forest,f)
    

