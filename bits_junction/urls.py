from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bits_junction.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include('bits_junction_app.urls')),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^admin/', include(admin.site.urls)),
) + static(
   settings.STATIC_URL, document_root=settings.STATIC_ROOT
) + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)