"""bug_tracker URL Configuration

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

from bug_tracker import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('ticket_detail/<int:id>/', views.ticket_detail, name='ticketdetail'),
    path('signup/', views.signup, name='signup'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('newticket/', views.newticket, name='newticket'),
    path('updateticket/<int:id>/', views.updateticket, name='update_ticket'),
    path('completedticket/<int:id>/', views.completed_ticket, name='completed_ticket'),
    path('invalidticket/<int:id>/', views.invalid_ticket),
    path('userpage/<int:id>/', views.userpage, name='userpage')
]
