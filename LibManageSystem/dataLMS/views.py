from urllib import request
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import logout

from django.urls import reverse
from django.views import View
from django.views.generic.list import ListView

from dataLMS.models import Books, IssuedBooks

from .forms import LoginForm, RegistrationForm

# Create your views here.
class RegisterView(View):

    def get(self, request):
        form = RegistrationForm()
        return render(request, 'dataLMS/register.html', {'form':form})
    
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            
            if User.objects.filter(email=request.POST['email']).exists():
                return render(request, 'dataLMS/register.html', {'form':form, 'error':'Email already exists. Please Log In'})
            
            form.save()
            return HttpResponseRedirect(reverse('account'))



class LoginView(View):

    def get(self, request):
        loginForm = LoginForm()
        return render(request, 'dataLMS/login.html', {'form':loginForm})

    def post(self, request):
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            a = request.POST['password']
            if User.objects.filter(email=request.POST['email']).exists():
                if User.objects.get(email=request.POST['email']).password == a:
                    request.session['email'] = request.POST['email']
                    object = User.objects.get(email=request.session['email'])
                    context= IssuedBooks.objects.get(issuer=request.session['email']).issuedBook
                    return render(request, 'dataLMS/account.html', {'object':object, 'bookData':[context]})
                else:
                    return render(request, 'dataLMS/login.html', {'form':loginForm, 'error':'Password invalid'})
            else:
                return render(request, 'dataLMS/login.html', {'form':loginForm, 'error':'Email Does not Exist'})


class BookListView(ListView):
    model = Books
    paginate_by = 100  # if pagination is desired
    template_name = 'dataLMS/bookList.html'

class BookDetailView(View):

    def get(self, request, slug):
        data = Books.objects.get(slug=slug)
        return render(request, 'dataLMS/bookDetail.html', {'object':data})
    
    
    def post(self, request, slug):
        data = Books.objects.get(slug=slug)
        try:
            a = IssuedBooks.objects.create(issuer=request.session['email'], issuedBook=Books.objects.get(slug=slug))
            return render(request, 'dataLMS/bookDetail.html', {'object':data,'status':'You issued This Book!'})
        except Exception:
            return HttpResponse("<h1>Please Sign In To Issue this Book</h1>")


class AccountView(View):

    def get(self, request):
        object = User.objects.get(email=request.session['email'])
        context= IssuedBooks.objects.get(issuer=request.session['email']).issuedBook
        return render(request, 'dataLMS/account.html', {'object':object, 'bookData':[context]})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('login'))