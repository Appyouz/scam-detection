from django.urls import path
from . import views

app_name = "ml_model"
urlpatterns = [
    path('', views.home, name='home'),
    path('prediction_api/', views.prediction_view, name="prediction_api")
]
