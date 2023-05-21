"""django_educenter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

from main import views as main_views

urlpatterns = [
    path('PinocchioInLadiesUnderwear/', admin.site.urls),

    # main urls
    path('', main_views.home, name="home"),
    path('about/', main_views.about, name="about"),
    path('contact/', main_views.contact, name="contact"),

    # academics urls
    path('', include('academics.urls')),

    # posting urls
    path('', include('postings.urls')),

    # users urls
    path('', include('users.urls')),

    # RestAPI urls
    path('api/', include('django_educenter.routers')),

    # gmail OAUTH
    path('accounts/', include('allauth.urls')),

    # JWT urls
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),

    # debug toolbar
    path('__debug__/', include('debug_toolbar.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]
