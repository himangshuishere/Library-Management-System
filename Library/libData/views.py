from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from .models import UsersModel, BooksModel, IssuedBooksModel

# Create your views here.

class HomeView(TemplateView):
    template_name = 'home.html'
    model = BooksModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = BooksModel.objects.all()
        return context
    


class AccountPage(View):
    template_name = 'account.html'
    model = UsersModel

    def get(self, request):
        return render(request, self.template_name, { 'details': UsersModel.objects.get(userID=request.session['userID'])})


class BookDetailView(View):
    template_name = 'bookDetails.html'
    model = BooksModel

    def get(self, request, id): # For viewing a book
        context = {}
        book_id = id
        book = BooksModel.objects.get(bookID=book_id)
        context['book'] = book
        return render(request, self.template_name, context)
    
    def post(self, request, id): # For Issuing a book
        book_id = id
        try:
            iBook = IssuedBooksModel.objects.create(issuedBy=UsersModel.objects.get(userId=request.session['userId']), issuedBook=BooksModel.objects.get(bookID=book_id))
            return render(request, self.template_name, {'message': 'Book Issued Successfully'})
        except Exception as e:
            return render(request, self.template_name, {'error': e})


class LoginView(View):
    template_name = 'login.html'
    model = UsersModel

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        try:
            user = UsersModel.objects.get(userEmail=request.POST['email'])
            if user.userPassword == request.POST['password']:
                request.session['userId'] = user.userId
                return render(request, 'account.html', {'details': UsersModel.objects.get(userID=request.session['userId'])})
            else:
                return render(request, self.template_name, {'error': 'Invalid Password'})
        except Exception as e:
            return render(request, self.template_name, {'error': 'Invalid Email'})


class RegisterView(View):
    template_name = 'register.html'
    model = UsersModel

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        try:
            user = UsersModel.objects.create(userName=request.POST['name'], userEmail=request.POST['email'], userPassword=request.POST['password'])
            request.session['userId'] = user.userId
            return HttpResponseRedirect(reverse('account'))
        except Exception as e:
            return render(request, self.template_name, {'error': e})