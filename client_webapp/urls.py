from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'v1/signup', SignupViewset, basename='SignupViewset')
router.register(r'v1/login', LoginViewset, basename='LoginViewset')
router.register(r'v1/logout', LogoutViewset, basename='LogoutViewset')
router.register(r'v1/clientviewset', ClientViewSet, basename='ClientViewSet')
urlpatterns = [
    path('', include(router.urls)),
]

# urlpatterns = [
#     path('', LoginViewset.as_view()),
#     path('clientgenericview/', ClientGenericView.as_view()),
#     # path('clientDetail/<int:pk>', ClientDetail.as_view()),
# ]
