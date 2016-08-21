"""fantasie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

import musiclib.views

urlpatterns = [
    # url(r'^admin', admin.site.urls),
    url(r'^$', musiclib.views.index, name='index'),
    url(r'^api/list$', musiclib.views.api_list),
    url(r'^api/meta$', musiclib.views.api_song_meta),
    url(r'^api/song_album_list', musiclib.views.api_song_album_list),
    url(r'^api/recommendation', musiclib.views.api_recommendation),
]
urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
              + static(settings.FRONTEND_URL, document_root=settings.FRONTEND_ROOT)
