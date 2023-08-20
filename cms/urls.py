from django.contrib import admin
from django.urls import path
from cms_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cms_api_data/', views.cms_api_data),
]
