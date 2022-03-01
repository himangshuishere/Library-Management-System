from django.urls import path
from .views import HomeView, AccountPage, BookDetailView, LoginView, RegisterView, ReturnBookView, LogoutView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('book/<uuid:id>', BookDetailView.as_view(), name='book-Detail'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('account/', AccountPage.as_view(), name='account'),
    path('return/<uuid:id>', ReturnBookView.as_view(), name='return'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
