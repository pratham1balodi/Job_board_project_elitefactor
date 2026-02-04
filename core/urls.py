from django.contrib import admin
from django.urls import path, include
from jobs.views import HomepageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomepageView.as_view(), name='homepage'),
    path('jobs/', include('jobs.urls')),
    path('users/', include('users.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
