import numpy as np 
from sklearn.svm import SVC 
from sklearn.metrics import accuracy_score
import pandas as pd 
import matplotlib.pyplot as plt 


# reading the data 
data = np.asarray(pd.read_csv('svc.csv', header=None))
# Assign the features to the variable X, and the labels to the variable y. 
X = data[:,0:2]
y = data[:,2]

model =  SVC(kernel='rbf', gamma=27)
model.fit(X, y)
y_pred = model.predict(X)
acc = accuracy_score(y, y_pred)

print(acc)