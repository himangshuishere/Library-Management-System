from django.urls import path
from .views import HomeView, AccountPage, BookDetailView, LoginView, RegisterView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('account/', AccountPage.as_view(), name='account'),
    path('book/<uuid:id>', BookDetailView.as_view(), name='book-Detail'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
]
