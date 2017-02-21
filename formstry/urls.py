"""formstry URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from views import create_req, show_req, welcome, show_all, show_detail, create_negative, negative

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^welcome/', welcome),
    url(r'^create/', create_req),
    # url(r'^request/(?P<tag>\w+)', show_req),
    url(r'^all/', show_all),
    url(r'^show/(?P<tag>\w+)/', show_detail),
    url(r'^one/', create_negative),
    url(r'^negative_created/', negative),
]

if settings.DEBUG:
    urlpatterns == static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)