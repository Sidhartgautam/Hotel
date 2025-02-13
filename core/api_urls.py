from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),


     path ('users/', include('users.urls')),
    path ('property/', include('property.urls')),
    path ('rooms/', include('rooms.urls')),
    path ('bookings/', include('bookings.urls')),
    path ('reviews/', include('reviews.urls')),
    path ('currencies/', include('currency.urls')),
    path ('countries/', include('country.urls')),
    path('faq/', include('faq.urls')), 
    path('offers/',include('offers.urls')),
    path('adminpannel/',include('adminpannel.urls')),
    path('meta/',include('meta.urls')),
    path('newsletter/',include('newsletter.urls'))
    
]
