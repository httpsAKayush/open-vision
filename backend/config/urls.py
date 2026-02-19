from django.contrib import admin
from django.urls import include,path

urlpatterns=[
    path('admin/',admin.site.urls),
    path('api/users/',include('apps.users.urls')),
    path('api/repositories/',include('apps.repositories.urls')),
    path('api/issues/',include('apps.issues.urls')),
    path('api/matching/',include('apps.matching.urls')),
]
