from django.urls import path
from .views import process_content

urlpatterns = [
    path("process/", process_content, name="process_content"),
]
