from calendar import c
from django.http import HttpResponse, HttpResponseRedirect
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
        try:
            return render(request, self.template_name, { 'details': UsersModel.objects.get(userId=request.session['userId'])})
        except Exception as e:
            return HttpResponse('<h1>You are not logged in!</h1>')


class BookDetailView(View):
    template_name = 'bookDetails.html'
    model = BooksModel
    context = {}

    def get(self, request, id): # For viewing a book
        book_id = id
        book = BooksModel.objects.get(bookID=book_id)
        self.context['book'] = book
        return render(request, self.template_name, self.context)
    
    def post(self, request, id): # For Issuing a book
        book_id = id
        try:
            if IssuedBooksModel.objects.filter(issuedBook=book_id, issuedBy=request.session['userId']).exists():
                self.context['error'] = 'You have already issued this book'
                return render(request, self.template_name, self.context)
            
            iBook = IssuedBooksModel.objects.create(issuedBy=UsersModel.objects.get(userId=request.session['userId']), issuedBook=BooksModel.objects.get(bookID=book_id))
            self.context['message'] = 'Book Issued Successfully'
            return render(request, self.template_name, self.context)
        except Exception as e:
            self.context['error'] = e
            return render(request, self.template_name, self.context)


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
# Need to fix login view


class RegisterView(View):
    template_name = 'register.html'
    model = UsersModel

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        try:
            if request.POST['password'] != request.POST['password2']:
                return render(request, self.template_name, {'error': 'Passwords do not match'})
            
            if len(request.POST['password']) < 8:
                return render(request, self.template_name, {'error': 'Password must be atleast 8 characters long'})
            user = UsersModel.objects.create(userName=request.POST['username'], userEmail=request.POST['email'], userPassword=request.POST['password'])
            request.session['userId'] = user.userId
            return HttpResponseRedirect(reverse('account'))
        except Exception as e:
            return render(request, self.template_name, {'error': e})


class LogoutView(View):
    def get(self, request):
        try:
            del request.session['userId']
        except Exception as e:
            pass
        return HttpResponseRedirect(reverse('home'))