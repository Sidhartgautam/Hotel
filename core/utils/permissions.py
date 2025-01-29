import requests
from django.conf import settings
from core.utils.moredealstoken import get_moredeals_token
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from core.utils.response import PrepareResponse
from property.models import Property
from rest_framework.permissions import BasePermission


class IsHotelPermission(BasePermission):    
    def has_permission(self, request, view):
        
        token = get_moredeals_token(request)
        sso_service_url = f"{settings.SSO_SERVICE_URL}permissions/hotel/"
        response = requests.get(sso_service_url, headers={'Authorization': f'{token}'})
        if response.status_code == 200:
            return True
        return False
    
class IsSuperuserPermission(BasePermission):
    def has_permission(self, request, view):
        token = get_moredeals_token(request)
        sso_service_url = f"{settings.SSO_SERVICE_URL}permissions/superuser/"
        response = requests.get(sso_service_url, headers={'Authorization': f'{token}'})
        if response.status_code == 200:
            if response.json()['data']['is_superuser']:
                return True
            else:
                return False
        return False
    
class IsHotelAndHotelOwnerPermission(BasePermission):
    def has_permission(self, request, view):
        token=get_moredeals_token(request) 
        print(token)
        if not token:
            return False
        sso_service_url = f"{settings.SSO_SERVICE_URL}permissions/hotel/"
        response = requests.get(sso_service_url, headers={'Authorization': f'{token}'})
        print(response.json())
        if response.status_code == 200:
            if response.json()['data']['is_hotel']:
                if request.user.is_authenticated and request.user.is_hotel_owner:
                    print("User messi", request.user)
                    return True
        return False
    
class HotelOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user