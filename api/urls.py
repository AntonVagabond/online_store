from django.urls import path, include

from api.spectacular.urls import urlpatterns as doc_urls
from users.urls import urlpatterns as user_urls
from products.urls import urlpatterns as product_urls
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView,
                                            TokenVerifyView)


app_name = 'api'

urlpatterns = [
    path('auth/', include('djoser.urls.jwt')),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('token/verify/', TokenVerifyView.as_view()),
]

urlpatterns += doc_urls
urlpatterns += user_urls
urlpatterns += product_urls
