from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = "core"

urlpatterns = [   
    path("", views.HomeView.as_view(), name="home"),
    path("shop/", views.ShopView.as_view(), name="shop"),
    path("product/<int:pk>", views.s_product, name="product"),
    path("blog/", views.BlogView.as_view(), name="blog"),
    path("post/<int:pk>", views.s_blog, name="post"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact_view, name="contact"),
    path("cart/", views.CartView.as_view(), name="cart"),
]

 
# Adicione estas linhas para servir arquivos de mídia durante o desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
