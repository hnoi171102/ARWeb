import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import pyrebase

# cred = credentials.Certificate("./ar-demo-808a4-firebase-adminsdk-w6gpm-76368eb650.json") # Replace with your own service account key path
# firebase_admin.initialize_app(cred, {
#     'databaseURL': 'https://ar-demo-808a4-default-rtdb.firebaseio.com'
# })

# ref = db.reference('')
# ref.delete()

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
db = firebase.database()
def delete_data_by_id(data_id):
    # Initialize Firebase app

    # Get a reference to the Realtime Database
    db = firebase.database()

    # Delete the data by ID
    try:
        db.child(data_id).remove()
        print(f"Data with ID {data_id} deleted successfully.")
    except Exception as e:
        print(f"Failed to delete data with ID {data_id}. Error: {str(e)}")

# Example usage
data_id = "-NVkAtS0ZIjkGDHf5F3h"
delete_data_by_id(data_id)