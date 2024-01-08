from api.spectacular.urls import urlpatterns as doc_urls
from users.urls import urlpatterns as user_urls
from products.urls import urlpatterns as product_urls
from carts.urls import urlpatterns as cart_urls


app_name = 'api'

urlpatterns = []

urlpatterns += doc_urls
urlpatterns += user_urls
urlpatterns += product_urls
urlpatterns += cart_urls
