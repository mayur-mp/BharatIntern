# -*- coding: utf-8 -*-
"""Task1 Titanic_Survival_Prediction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1TpzsJeKZUERJPjSUUhhEaj9aF-RR1KE7

**Data Set information:**

survival-Survival	0 = No, 1 = Yes

pclass	-Ticket class	1 = 1st, 2 = 2nd, 3 = 3rd
sex     -Sex
Age   	-Age in years
sibsp 	-# of siblings / spouses aboard the Titanic
parch	  -# of parents / children aboard the Titanic
ticket	-Ticket number
fare	  -Passenger fare
cabin	  -Cabin number
embarked -	Port of Embarkation	C = Cherbourg, Q = Queenstown, S = Southampton

import the necessary libs
"""

from gettext import install
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

"""Data Collection/loading and processing."""

titanic_data = pd.read_csv('/content/train.csv')

titanic_data.head()

titanic_data.shape

titanic_data.info()

titanic_data.isnull().sum()



#remove missing/null values
titanic_data = titanic_data.drop(columns='Cabin', axis=1)

#replacing missing values with mean number
titanic_data['Age'].fillna(titanic_data['Age'].mean(), inplace=True)

titanic_data.info()

titanic_data.isnull().sum()

#lets fix embarked
print(titanic_data['Embarked'].mode())

print(titanic_data['Embarked'].mode()[0])

#replace the mode value with the missing value
titanic_data['Embarked'].fillna(titanic_data['Embarked'].mode()[0], inplace=True)

titanic_data.isnull().sum()

"""Analysing the data"""

titanic_data.describe()

#how many survived?
titanic_data['Survived'].value_counts()

#visualizing data
sns.set()

sns.countplot(titanic_data['Survived'])

titanic_data['Sex'].value_counts()

# count plot for "Sex" column
sns.countplot(titanic_data['Sex'])

# Analysing Gender wise survivors
sns.countplot(x='Sex', hue='Survived', data=titanic_data)

# count plot for "Pclass" column
sns.countplot(x='Pclass', data=titanic_data)

sns.countplot(x='Pclass', hue='Survived', data=titanic_data)

"""Encode categorical columns/data"""

titanic_data['Sex'].value_counts()

titanic_data['Embarked'].value_counts()

titanic_data.replace({'Sex':{'male':0,'female':1}, 'Embarked':{'S':0,'C':1,'Q':2}}, inplace=True)

X = titanic_data.drop(columns = ['PassengerId','Name','Ticket','Survived'],axis=1)
Y = titanic_data['Survived']

print(X)

print(Y)

"""Split the data into test data and train data"""

X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size=0.2, random_state=2)

print(X.shape, X_train.shape,X_test.shape)

"""Logistical regression and model training"""

model = LogisticRegression()

#use the train data on logisticregression model
model.fit(X_train, Y_train)

"""evaluating and testing the model"""

X_train_prediction = model.predict(X_train)

print(X_train_prediction)

training_data_accuracy = accuracy_score(Y_train, X_train_prediction)
print('Accuracy score of training data : ', training_data_accuracy)

#check accuracy of test data
X_test_prediction = model.predict(X_test)

print(X_test_prediction)

test_data_accuracy = accuracy_score(Y_test, X_test_prediction)
print('Accuracy score of test data:', test_data_accuracy)

#ends...but
import joblib
joblib.dump(model, 'logistic_regression_model.pkl')


import subprocess
import os
from pyngrok import ngrok
#setup ngrok with authtoken

ngrok.set_auth_token("2hrNpxxoFWnJKciS1S9d2ihenMz_7KTQBY5FkTPhLETQdn48E")

#running flask app
os.system("nohup python -m flask run --no-reload &")

#opening ngrok tunnel to the flask app uding http protocol
proc = subprocess.Popen(["ngrok", "http", "5000"])

#Retrive ngrok's public url here
public_url = ngrok.connect(addr="5000", proto="http")
print("Public URL:", public_url)

from flask import Flask, request, jsonify
import joblib
from pyngrok import ngrok
from IPython.display import display, HTML

# Load the trained model
model = joblib.load('logistic_regression_model.pkl')

app = Flask(__name__)

@app.route('/')
def home():
    # HTML form to take inputs
    html_form = """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Titanic Survival Prediction</title>
    <style>
        body {
            background-color: black;
            color: white;
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 20px;
        }
        #predictionForm {
            display: inline-block;
            text-align: left;
        }
        img {
            max-width: 100%;
            height: auto;
        }
    </style>
</head>
<body>
    <h2>Titanic Survival Prediction</h2>
    <form id="predictionForm" method="post" action="/predict">
        <label for="pclass">Pclass:</label>
        <input type="text" id="pclass" name="pclass"><br><br>

        <label for="sex">Sex (0 for male, 1 for female):</label>
        <input type="text" id="sex" name="sex"><br><br>

        <label for="age">Age:</label>
        <input type="text" id="age" name="age"><br><br>

        <label for="sibsp">SibSp:</label>
        <input type="text" id="sibsp" name="sibsp"><br><br>

        <label for="parch">Parch:</label>
        <input type="text" id="parch" name="parch"><br><br>

        <label for="fare">Fare:</label>
        <input type="text" id="fare" name="fare"><br><br>

        <label for="embarked">Embarked (0 for S, 1 for C, 2 for Q):</label>
        <input type="text" id="embarked" name="embarked"><br><br>

        <button type="button" onclick="predictSurvival()">Predict</button>
    </form>

    <p id="predictionResult"></p>

    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/fd/RMS_Titanic_3.jpg/800px-RMS_Titanic_3.jpg" alt="Titanic Image">

    <script>
        function predictSurvival() {
            var xhr = new XMLHttpRequest();
            var url = "/predict";
            var data = new FormData(document.getElementById("predictionForm")); // Changed to FormData

            xhr.open("POST", url, true);
            xhr.onreadystatechange = function () {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    var response = JSON.parse(xhr.responseText);
                    document.getElementById("predictionResult").innerHTML = "Survival Prediction: " + response.prediction;
                }
            };
            xhr.send(data);
        }
    </script>
</body>
</html>

    """
    return html_form

@app.route('/predict', methods=['POST'])
def predict():
    # Access form data
    pclass = request.form['pclass']
    sex = request.form['sex']
    age = request.form['age']
    sibsp = request.form['sibsp']
    parch = request.form['parch']
    fare = request.form['fare']
    embarked = request.form['embarked']

    # Convert data to appropriate types
    pclass = int(pclass)
    sex = int(sex)
    age = float(age)
    sibsp = int(sibsp)
    parch = int(parch)
    fare = float(fare)
    embarked = int(embarked)

    # Make prediction
    features = [[pclass, sex, age, sibsp, parch, fare, embarked]]
    prediction = model.predict(features)[0]

    return jsonify({'prediction': int(prediction)})

def run_flask_app():
    # Run Flask app on port 5000
    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)

# Start ngrok tunnel
public_url = ngrok.connect(addr="5000", proto="http")
print("Public URL:", public_url)

# Display ngrok tunnel URL
display(HTML(f"<h2>Open this link in your browser to access the application:</h2><p>{public_url}</p>"))

try:
    # Keep the Flask app running
    run_flask_app()
except KeyboardInterrupt:
    # Shutdown ngrok and Flask app
    ngrok.kill()

