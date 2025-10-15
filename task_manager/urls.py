from django.contrib import admin
from django.urls import path, include
from task_manager.views import IndexView
from task_manager.users.views import CustomLoginView, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('users/', include('task_manager.users.urls')),
]
