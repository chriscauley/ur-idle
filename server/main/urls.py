from django.contrib import admin
from django.urls import include, path, re_path

from unrest.views import index

# forms loaded via unrest schema
import unrest.user.forms
import todo.forms

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path("^(app|auth)/", index),
    path("", index),
    path('', include('unrest.urls')),
]
