from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('msg_app/', include('messages_app.urls')),
    path('admin/', admin.site.urls),

]
