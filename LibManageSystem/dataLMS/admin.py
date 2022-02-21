from django.contrib import admin
from .models import Books, IssuedBooks

# Register your models here.
@admin.register(IssuedBooks)
class BooksAdmin(admin.ModelAdmin):
    search_fields = ('issuer', 'issuedBook')

@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}
    search_fields = ('title', 'author')