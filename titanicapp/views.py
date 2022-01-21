from django.http import HttpResponse
from django.shortcuts import render
import numpy as np
import pandas as pd
import os
from sklearn.linear_model import LogisticRegression
import csv
# Create your views here.


# def pred(val):
#     Data = [val]
#     y_pred = clf.predict(Data)
#     return y_pred


def index(request):
    data_train = pd.read_csv("titanicapp/static/data/train.csv")
    data_train.drop(['Name', 'Age', 'Ticket', 'Fare',
                    'Cabin'], inplace=True, axis=1)
    data_train.Embarked = data_train.Embarked.fillna('S')
    genderMap = {'male': 0, 'female': 1}
    data_train.Sex = data_train.Sex.map(genderMap)
    embarkedMap = {'S': 0, 'C': 1, 'Q': 2}
    data_train.Embarked = data_train.Embarked.map(embarkedMap)
    X_train = data_train.drop(['PassengerId', 'Survived'], axis=1)
    Y_train = data_train.Survived

    clf = LogisticRegression(random_state=0)
    clf.fit(X_train, Y_train)
    print("alis mangukiya")
    accuracy = round(clf.score(X_train, Y_train)*100, 2)
    print("Accurecy is : " + str(accuracy) + "%")
    status = 0

    if request.method == "POST":
        pclass = request.POST.get("pclass")
        gender = request.POST.get("gender")
        sib = request.POST.get("sib")
        par = request.POST.get("par")
        emb = request.POST.get("emb")
        
        y_pred = clf.predict([[pclass, gender, sib, par, emb]])
        print(y_pred)
        if y_pred[0] == 1:
            status=1
        else:
            print("Not Survived")
            status = -1
    return render(request,'index.html',{'status':status})
 