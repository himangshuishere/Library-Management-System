from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from .models import UsersModel, BooksModel, IssuedBooksModel

# Create your views here.

class HomeView(View):
    template_name = 'home.html'
    model = BooksModel.objects.all()

    def get(self, request):
        status = False
        if 'userEmail' in list(request.session.keys()):
            status = True
        return render(request, self.template_name, {'books':self.model, 'status':status})



class AccountPage(View):
    template_name = 'account.html'
    model = UsersModel

    def get(self, request):
        try:
            try:
                books = [IssuedBooksModel.objects.get(issuedBy=UsersModel.objects.get(userEmail=request.session['userEmail']))]
            except IssuedBooksModel.DoesNotExist:
                books = None
                return render(request, self.template_name, { 'details': UsersModel.objects.get(userEmail=request.session['userEmail']), 'books':books})

            return render(request, self.template_name, { 'details': UsersModel.objects.get(userEmail=request.session['userEmail']), 'books':books})

        except Exception as e:
            # return HttpResponse(e)
            return HttpResponse("<h1> You are not signed in! </h1>")


class BookDetailView(View):
    template_name = 'bookDetails.html'
    model = BooksModel

    def get(self, request, id): # For viewing a book
        book_id = id
        book = BooksModel.objects.get(bookID=book_id)
        return render(request, self.template_name, {'book':book})
    
    def post(self, request, id): # For Issuing a book
        book_id = id
        book = BooksModel.objects.get(bookID=book_id)
        try:
            if IssuedBooksModel.objects.filter(issuedBook=book_id, issuedBy=UsersModel.objects.get(userEmail=request.session['userEmail'])).exists():
                return render(request, self.template_name, {'book':book, 'message':'You Have already issued this book!'})
            
            iBook = IssuedBooksModel.objects.create(issuedBy=UsersModel.objects.get(userEmail=request.session['userEmail']), issuedBook=BooksModel.objects.get(bookID=book_id))
            self.context['message'] = 'Book Issued Successfully'
            return HttpResponseRedirect(reverse('account'))
            # return render(request, self.template_name, {'book':book, 'message':'Book Issued Successfully'})
        except Exception as e:
            return HttpResponseRedirect(reverse('login'))


class LoginView(View):
    template_name = 'login.html'
    model = UsersModel

    def get(self, request):
        if 'userEmail' in list(request.session.keys()):
            return HttpResponseRedirect(reverse('account'))
        return render(request, self.template_name)

    def post(self, request):
        try:
            user = UsersModel.objects.get(userEmail=request.POST['email'])
            if user.userPassword == request.POST['password']:
                request.session['userEmail'] = user.userEmail
                return HttpResponseRedirect(reverse('home'))
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
            request.session['userEmail'] = user.userEmail
            return HttpResponseRedirect(reverse('home'))
        except Exception as e:
            return render(request, self.template_name, {'error': e})


class LogoutView(View):
    def get(self, request):
        try:
            del request.session['userEmail']
        except Exception as e:
            pass
        return HttpResponseRedirect(reverse('home'))