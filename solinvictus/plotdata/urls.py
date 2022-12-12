from django.urls import path

from . import views

urlpatterns = [
    # ex: /plotdata/
    path('', views.index, name='index'),
    # ex: /plotdata/2/
    path('<int:location_id>/', views.detail, name='detail'),

]
