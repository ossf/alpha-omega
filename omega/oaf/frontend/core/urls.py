"""core URL Configuration

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
from django.contrib import admin
from django.urls import path
from oaffe.views import (
    home,
    api_get_assertion,
    api_add_assertion,
    search_subjects,
    show_assertions,
    download_assertion,
    download_assertions,
    refresh,
    policy_heapmap,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("assertions", search_subjects, name="search_assertions"),
    path("assertions/show", show_assertions, name="show_assertions"),
    path("assertions/refresh", refresh, name="refresh_policies"),
    path("assertions/download-all", download_assertions, name="download_assertions"),
    path("assertions/<str:assertion_uuid>/download", download_assertion, name="download_assertion"),
    path("api/assertion/add", api_add_assertion, name="api_add_assertion"),
    path("api/assertion/<str:assertion_uuid>", api_get_assertion, name="api_get_assertion"),
    path("heatmap", policy_heapmap, name="policy_heapmap"),
    path("", home),
]
