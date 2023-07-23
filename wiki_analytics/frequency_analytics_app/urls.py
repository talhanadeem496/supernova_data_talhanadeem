from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'process_and_upload', views.ProcessUploadDataViewSet, basename="Send Email")
# router.register(r'receive_email', views.ReceiveEmail, basename="Receive Email")



urlpatterns = [
    path('', include(router.urls)),
]