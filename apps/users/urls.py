from django.urls import path

from .views import JWTLoginView,JWTRefreshView,MeView,RegisterView,TokenLoginView,TokenLogoutView,UserListView,VerifyUserView


urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/token/', TokenLoginView.as_view()),
    path('logout/token/', TokenLogoutView.as_view()),
    path('login/jwt/', JWTLoginView.as_view()),
    path('login/jwt/refresh/', JWTRefreshView.as_view()),
    path('me/', MeView.as_view()),     
    path('', UserListView.as_view()),
    path('<int:pk>/verify/', VerifyUserView.as_view()),
]