from django import forms
from django.forms import inlineformset_factory
from .models import Book, BookCopy, Author, Category, Publisher

class BookForm(forms.ModelForm):
    new_authors = forms.CharField(
        required=False,
        help_text="Enter new authors separated by commas, e.g. John Doe, Jane Smith"
    )
    new_categories = forms.CharField(
        required=False,
        help_text="Enter new categories separated by commas"
    )
    new_publisher_name = forms.CharField(required=False)
    new_publisher_address = forms.CharField(required=False)
    new_publisher_email = forms.EmailField(required=False)

    class Meta:
        model = Book
        fields = ['title', 'authors', 'categories', 'publisher', 'publication_date', 'description']

BookCopyFormSet = inlineformset_factory(
    Book,
    BookCopy,
    fields=('copy_number', 'copy_type', 'availability_status'),
    extra=1,
    can_delete=True
)
