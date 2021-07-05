from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
import traceback
from client_webapp.token import get_access_token
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from django.contrib.auth import authenticate, login, logout
import re
from common_app.models import Account
from oauth2_provider.models import Application , RefreshToken
from client_webapp.function import is_email_exist
from client_webapp.models import Task
from django.db.models import Q
import datetime
from client_webapp.permission import IsUserOnly
from django.shortcuts import render, redirect
from rest_framework import generics, mixins
from client_webapp.serializers import TaskSerializer
from django.views import View

class SignupViewset(viewsets.ViewSet):
    def create(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            
            if not re.search(r'\w+@\w+',email if email else "not a email"):
                raise Exception("email id is not valid")
            if password and len(password)<6:
                raise Exception("password should be atleast 6 charater")
            if email and password:
                if not first_name:
                    raise Exception('please enter first name')
                if not last_name:
                    raise Exception('please enter last name')
                if is_email_exist(email):
                    raise Exception('email already exist')
                account_obj = Account.objects.create(email=email,name= str(first_name)+" "+str(last_name))
                account_obj.set_password(password)
                account_obj.is_active = True
                account_obj.account_type = 'M'
                account_obj.save()
                # token = get_access_token(account_obj)
                Application.objects.get_or_create(user=account_obj,client_type=Application.CLIENT_CONFIDENTIAL,authorization_grant_type=Application.GRANT_PASSWORD)
                return Response({'message': "Account Created","success":True},status=status.HTTP_200_OK)

        except Exception as error:
            traceback.print_exc()
            return Response({"message":str(error),"success":False},status=status.HTTP_200_OK) 

class LoginViewset(viewsets.ViewSet):
    def create(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            if email and password:
                if not email:
                    raise Exception("please enter email")
                if not password:
                    raise Exception("please enter password")

                if not re.search(r'\w+@\w+',email):
                    user_obj = Account.objects.get(email = email)
                    email = user_obj.email

                    user = authenticate(email=email,password=password)
                else:
                    user = authenticate(email=email,password=password)

                if user.account_type == 'M':
                    user = authenticate(email=email,password=password)
                    token = get_access_token(user)
                    return Response({"token":token,"user_id":user.id,"email":user.email,"success":True},status=status.HTTP_200_OK)
                else:
                    raise Exception("credentials not match")
        except Exception as error:
            traceback.print_exc()
            return Response({"message":str(error),"success":False},status=status.HTTP_200_OK) 

class LogoutViewset(viewsets.ViewSet):
    permission_classes = [TokenHasReadWriteScope]

    def list(self, request):
        try:
            RefreshToken.objects.filter(access_token=request.auth).delete()
            request.auth.delete()
            return Response({'message':"user logged out successfully","success":True},status=status.HTTP_200_OK)
        except Exception as error:
            traceback.print_exc()
            return Response({"message":str(error),"success":False},status=status.HTTP_200_OK)

class ManagerViewset(viewsets.ViewSet):
    permission_classes = [TokenHasReadWriteScope,IsUserOnly]

    def list(self, request):
        try:
            user_obj = request.user
            task_list = [{"id":task_obj.id,"title":task_obj.title,"description":task_obj.description,"status":task_obj.status,"task_date":task_obj.task_date,'selected':True if Task.objects.filter(account=user_obj) else False} 
            for task_obj in Task.objects.filter(is_active=True)]
            return Response({'data':task_list,"success":True},status=status.HTTP_200_OK)
        except Exception as error:
            traceback.print_exc()
            return Response({"message":str(error),"success":False},status=status.HTTP_200_OK)