from django.urls import path
from . import views
from .views import get_firebase_data_paths
from .views import view_firebase_files
from .views import upload_file
from .views import delete_file
urlpatterns = [
    path('', views.main, name="main"),
    path('firebase-data-paths/', get_firebase_data_paths, name='firebase-data-paths'),
    path('view-files/', view_firebase_files, name='view-files'),
    path('upload/', upload_file, name='upload-file'),
    path('delete/<str:file_name>/', views.delete_file, name='delete_file'),
]
