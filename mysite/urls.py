"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from mysite.views import LoadPage, LoadCheckIp, checksingleip, ReadXl,    export_users_xls, About, Contact, addcontact, ReadBulk, ContactDev, LoginPage,DownloadResume, AuthUser, logout, FileHashSingle, BulkHash, downxlshash,HashBulkRead

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginPage),
    path('Authuser/', AuthUser),
    path('Logout/', logout),
    path('main/', LoadPage),
    path('loadcip/',LoadCheckIp),
    path('checksingleip/', checksingleip),
    path('ipxl/', ReadXl),
    path('downxls/<ref>/', export_users_xls),
    path('About/', About),
    path('Contact/', Contact),
    path('Contactdev/', ContactDev),
    path('contacted/', addcontact),
    path('ipbulk/', ReadBulk),
    path('resume/',DownloadResume),
    path('loadfilehash/', FileHashSingle),
    path('hashxl/', BulkHash),
    path('downxlshash/<ref>',downxlshash),
    path('hashbulk/', HashBulkRead)
]