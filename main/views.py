from django.shortcuts import render, redirect
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import default_storage
from django.contrib import messages
import pyrebase
import os

config = {
    "apiKey": "AIzaSyDwkE1dLqXvucSg8ieVIiYDg0K28511Ggo",
    "authDomain": "ar-demo-808a4.firebaseapp.com",
    "databaseURL": "https://ar-demo-808a4-default-rtdb.firebaseio.com",
    "projectId": "ar-demo-808a4",
    "storageBucket": "ar-demo-808a4.appspot.com",
    "messagingSenderId": "563500268331",
    "appId": "1:563500268331:web:bb5ac286723ce2cb7d236e",
    "measurementId": "G-GJFCWBHQHW"
}   

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()



def main(request):
    if request.method == 'POST':
        file = request.FILES['file']
        file_save = default_storage.save(file.name, file)
        storage.child("files/" + file.name).put("media/" + file.name)
        delete = default_storage.delete(file.name)
        messages.success(request, "File upload in Firebase Storage successful")
        return redirect('main')
    else:
        return render(request, 'main.html')

#def getfile(request):
#    if request.method == 'GET':
#        file = 