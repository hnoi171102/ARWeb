from django.shortcuts import render, redirect
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import default_storage
from django.contrib import messages
import os
import pyrebase
from firebase_admin import db
from django.http import JsonResponse
from django.shortcuts import render, redirect
import re

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
database = firebase.database()


def main(request):
    if request.method == 'POST' and request.FILES['file']:
        # Get the uploaded file from the request
        uploaded_file = request.FILES['file']

        file = request.FILES['file']
        file_name = file.name

        # Upload file to Firebase Storage root directory
        storage.child(file_name).put(file)
        # Get the download URL of the uploaded file
        
        download_url = storage.child(file_name).get_url(None)

        db = firebase.database()
        # Store file details in the Realtime Database root
        file_data = {
            "file_name": file_name,
            "download_url": download_url
        }
        cleaned_file_name = re.sub(r'[.$#\[\]/]', '_', file_name)
        db.child(cleaned_file_name).set(file_data)

        return redirect('view-files')

    return render(request, 'main.html')

def get_firebase_data_paths(request):
    # Get a reference to the root of the Realtime Database
    root_ref = db.reference('/')

    # Get a snapshot of the entire database
    snapshot = root_ref.get()

    # Retrieve all data paths from the snapshot
    data_paths = []

    def traverse_data_paths(data, path):
        if isinstance(data, dict):
            for key, value in data.items():
                traverse_data_paths(value, path + '/' + key)
        else:
            data_paths.append(path)

    traverse_data_paths(snapshot, '')

    # Return the list of data paths as JSON response
    return JsonResponse(data_paths, safe=False)

def view_firebase_files(request):
    
    # Get a reference to the Realtime Database root
    root_ref = db.reference('/')

    # Retrieve the data containing file URLs or references
    file_data = root_ref.get()

    file_ids = []
    files = database.get().val()
    if files:
        file_ids = list(files.keys())
    
    print(file_ids)

    file_list = [{'url': url, 'name': name} for name, url in file_data.items()]

    if request.method == 'POST':
        # Retrieve the file ID from the submitted form
        file_id = request.POST.get('file_id')

        # Delete the file by its ID from the Realtime Database
        database.child('files').child(file_id).remove()


        return redirect('view-files')
    
    return render(request, 'files.html', {'file_data': file_list})


def delete_file(request, file_name):
    # Assuming you have already initialized the Pyrebase app    
    db = firebase.database()

    print(file_name)
    try:
        # Remove the file entry from the Realtime Database
        db.child(file_name).remove()
        
        message = 'File deleted successfully.'
    except Exception as e:
        # Handle any exceptions that occur during the database operation
        message = f'Failed to delete the file. Error: {str(e)}'

    return redirect('view-files') 

from django import forms

class FileUploadForm(forms.Form):
    file = forms.FileField()

from django.shortcuts import render, redirect
import base64

import base64

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Set up Pyrebase
            database = firebase.database()

            # Get the uploaded file
            file = request.FILES['file']

            # Read the file data and encode as base64
            file_data = base64.b64encode(file.read()).decode('utf-8')

            # Generate a unique file ID
            file_id = database.generate_key()

            # Save the file data to the Realtime Database
            database.child(file_id).set(file_data)
            return redirect('view-files')
    else:
        form = FileUploadForm()

    return render(request, 'upload.html', {'form': form})