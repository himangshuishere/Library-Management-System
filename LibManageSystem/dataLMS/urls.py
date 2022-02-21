from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from dataLMS.views import AccountView, BookListView, LoginView, LogoutView, RegisterView, BookDetailView

urlpatterns = [
    path('', BookListView.as_view(), name='books'),
    path('book/<slug:slug>/', BookDetailView.as_view(), name='bookDetail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('account/', login_required(TemplateView.as_view(template_name='dataLMS/account.html')), name='account'),
    # path('account/', login_required(AccountView.as_view()), name='account'),
    path('logout/', LogoutView.as_view(), name='logoutView'),
]
