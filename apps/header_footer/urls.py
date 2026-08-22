from django.urls import path

from .views import HeaderView, HeaderDetailView, FooterView, FooterTextView

urlpatterns = [
    path('header/', HeaderView.as_view()),
    path('header/<int:pk>/', HeaderDetailView.as_view()),
    path('footer/', FooterView.as_view()),
    path('footer-text/', FooterTextView.as_view()),
]
