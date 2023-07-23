import csv
import imaplib
import re
import ssl
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.permissions import AllowAny
import requests
import json
import numpy as np
from operator import itemgetter
from celery import group, chord 
from django.conf import settings
import functools
import itertools
import time
import operator

from utils.common import error_response, get_error_text, success_response
from .models import *
from datetime import datetime
import cv2
import base64
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from .models import *

# Create your views here.
from django_mailbox.signals import message_received
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import email
import django_mailbox
import os


class ProcessUploadDataViewSet(ViewSet):
    
    http_method_names = ["post", ]
    permission_classes = [AllowAny, ]

    def create(self, request, *args, **kwargs):
        try:
            data = {}
            
            return success_response(data=data,
                                    message="Data Processed and Uploaded Successfully")
        except Exception as e:
            print(e)
            errors = get_error_text()
            return error_response(errors=errors)

