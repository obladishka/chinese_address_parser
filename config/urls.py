from parser.views import ParserView

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", ParserView.as_view(), name="api-page"),
]
