from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

admin.site.site_header = "Vize Forum Admin Paneli"
admin.site.site_title = "Vize Forum Admin Paneli"
admin.site.index_title = "Vize Forum Admin Paneline Hoşgeldiniz"

urlpatterns = [
    path("admin/", admin.site.urls),    
    path("api-auth/", include("rest_framework.urls"), name="rest_framework"),
    path("api/member/", include("members.urls")),
    path("api/threads/", include("threads.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)