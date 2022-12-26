from django.urls import path

from . import views

'''
    If you want to change the URL of the polls detail view to something else,
    perhaps to something like polls/specifics/12/ instead of doing it in the
    template (or templates) you would change it in polls/urls.py:
    ...
    # added the word 'specifics'
    path('specifics/<int:question_id>/', views.detail, name='detail'),
    ...
'''
app_name = 'plotdata'
urlpatterns = [
    # ex: /plotdata/
    path('', views.index, name='index'),
    # ex: /plotdata/2/
    # the 'name' value as called by the {% url %} template tag
    path('<int:location_id>/', views.detail, name='detail'),
    path('<int:location_id>/edit/', views.edit, name='edit'),
    path('<int:location_id>/save/', views.save, name='save'),
]
