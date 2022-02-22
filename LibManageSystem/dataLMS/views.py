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
        form = RegistrationForm(request.POST or None)
        return render(request, 'dataLMS/register.html', {'form':form})
    
    def post(self, request):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            
            if User.objects.filter(email=request.POST['email']).exists():
                return render(request, 'dataLMS/register.html', {'form':form, 'error':'Email already exists. Please Log In'})
            
            request.session['email'] = request.POST['email']
            form.save()
            return HttpResponseRedirect(reverse('account'))



class LoginView(View):

    def get(self, request):
        loginForm = LoginForm(request.POST or None)
        return render(request, 'dataLMS/login.html', {'form':loginForm})

    def post(self, request):
        loginForm = LoginForm(request.POST or None)
        if loginForm.is_valid():
            a = request.POST['password']
            if User.objects.filter(email=request.POST['email']).exists():
                if 'email' in request.session.keys():
                    if request.POST['email'] == request.session['email']:
                        return render(request, 'dataLMS/login.html', {'form':loginForm, 'error':'User already logged in!'})
                else:
                    if User.objects.get(email=request.POST['email']).password == a:
                        
                        request.session['email'] = request.POST['email']
                        return HttpResponseRedirect(reverse('account'))

                    else:
                        return render(request, 'dataLMS/login.html', {'form':loginForm, 'error':'Password invalid'})
            else:
                return render(request, 'dataLMS/login.html', {'form':loginForm, 'error':'Email Does not Exist'})


class BookListView(View):
    def get(self, request):
        books = Books.objects.all()
        if 'email' in request.session.keys():
            return render(request, 'dataLMS/bookList.html', {'books':books, 'data':True})
        return render(request, 'dataLMS/bookList.html', {'books':books})



class BookDetailView(View):

    def get(self, request, slug):
        data = Books.objects.get(slug=slug)
        return render(request, 'dataLMS/bookDetail.html', {'object':data})
    
    
    def post(self, request, slug):
        data = Books.objects.get(slug=slug)
        try:
            
            a = IssuedBooks.objects.create(issuer=User.objects.get(email=request.session['email']), issuedBook=Books.objects.get(slug=slug))
                
            return render(request, 'dataLMS/bookDetail.html', {'object':data,'status':'You issued This Book!'})
        except Exception as e:
            # return HttpResponse(e)
            return HttpResponseRedirect(reverse('login'))



class AccountView(View):

    def get(self, request):
        try:
            object = User.objects.get(email=request.session['email'])
            try:
                context= [IssuedBooks.objects.get(issuer=User.objects.get(email=request.session['email'])).issuedBook]
            except Exception:
                context = 'No Books Issued'
                return render(request, 'dataLMS/account.html', {'object':object, 'bookData':context, 'issueStatus':False, 'error':'No books Issued!'})
            return render(request, 'dataLMS/account.html', {'object':object, 'bookData':context, 'issueStatus':True})
        except Exception as e:
            return HttpResponse(e)
            # return HttpResponseRedirect(reverse('login'))


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('books'))