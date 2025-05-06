from django.urls import path
from . import views
from .views import predict_view

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('predict/', predict_view, name="predict"),  # Keep only one
    path('feedback/', views.send_feedback, name='send_feedback'),  
    # path('admin/predictions/', view_predictions, name="view_predictions"),
]
