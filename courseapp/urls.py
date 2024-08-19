
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path
from django.conf.urls.static import static 
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('kurslar/', include('courses.urls')),
    path('', include('pages.urls')), 
    path('account/', include('account.urls'))

] + static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
