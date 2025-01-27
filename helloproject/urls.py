"""
URL configuration for helloproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
#from django.contrib import admin
#from django.urls import include, path

#urlpatterns = [
    # path("admin_site/", include("admin_site.urls")),
  #  path("polls/", include("polls.urls")),
   # path('admin/', admin.site.urls),
#]

from django.contrib import admin
from django.urls import path
from admin_site import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('', views.user),
    # path('show',views.show,name = 'show'),
     path('edit/<int:id>', views.edit),
     path('update/<int:id>', views.update),
     path('delete/<int:id>', views.destroy),

    path('emp', views.user, name='user'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('show', views.show, name='show'),
    #path('edit/<int:id>/', views.edit, name='edit'),
    path('update/<int:id>/', views.update, name='update'),
    #path('destroy/<int:id>/', views.destroy, name='destroy'),
    path('change_password/', views.change_password, name='change_password'),
    path('reset_password/<int:id>/', views.reset_password, name='reset_password'),
    path('reset_password/', views.reset_password, name='reset_password'),

]
