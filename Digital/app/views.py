from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import redirect
from .models import Book, Author, Category, Publisher
from .forms import BookCopyFormSet, BookForm


class AdminOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'app/home.html'
    login_url = '/login/'

class AboutPageView(TemplateView):
    template_name = 'app/about.html'


class BookListView(ListView):
    model = Book
    context_object_name = 'posts'
    template_name = 'app/book_list.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Book.objects.filter(
                Q(title__icontains=query) |
                Q(authors__first_name__icontains=query) |
                Q(authors__last_name__icontains=query) |
                Q(categories__category_name__icontains=query) |
                Q(publisher__name__icontains=query)
            ).distinct()
        return Book.objects.all()


class BookDetailView(DetailView):
    model = Book
    template_name = 'app/book_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        copies = self.object.copies.all()

        context['total_copies'] = copies.count()
        context['available_copies'] = copies.filter(availability_status='Available').count()
        context['reference_only_copies'] = copies.filter(availability_status='Reference Only').count()
        context['unavailable_copies'] = copies.filter(availability_status='Unavailable').count()

        return context


class BookCreateView(LoginRequiredMixin, AdminOnlyMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'app/book_create.html'
    login_url = '/accounts/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['copy_formset'] = BookCopyFormSet(self.request.POST or None)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        copy_formset = context['copy_formset']

        if not copy_formset.is_valid():
            return self.render_to_response(context)

        if form.cleaned_data.get('new_publisher_name'):
            publisher = Publisher.objects.create(
                name=form.cleaned_data['new_publisher_name'],
                address=form.cleaned_data.get('new_publisher_address', ''),
                email=form.cleaned_data.get('new_publisher_email', '')
            )
            form.instance.publisher = publisher

        self.object = form.save()

        authors = form.cleaned_data['authors']
        new_authors = form.cleaned_data.get('new_authors')
        if new_authors:
            for name in new_authors.split(','):
                parts = name.strip().split(' ', 1)
                if len(parts) == 2:
                    first, last = parts
                else:
                    first, last = parts[0], ''
                author, created = Author.objects.get_or_create(first_name=first, last_name=last)
                authors = authors | Author.objects.filter(pk=author.pk)
        self.object.authors.set(authors)

        categories = form.cleaned_data['categories']
        new_categories = form.cleaned_data.get('new_categories')
        if new_categories:
            for cat_name in new_categories.split(','):
                category, created = Category.objects.get_or_create(category_name=cat_name.strip())
                categories = categories | Category.objects.filter(pk=category.pk)
        self.object.categories.set(categories)

        copy_formset.instance = self.object
        copy_formset.save()

        return super().form_valid(form)


class BookUpdateView(LoginRequiredMixin, AdminOnlyMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'app/book_update.html'
    login_url = '/accounts/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['copy_formset'] = BookCopyFormSet(
            self.request.POST or None,
            instance=self.object
        )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        copy_formset = context['copy_formset']

        if not copy_formset.is_valid():
            return self.render_to_response(context)

        if form.cleaned_data.get('new_publisher_name'):
            publisher = Publisher.objects.create(
                name=form.cleaned_data['new_publisher_name'],
                address=form.cleaned_data.get('new_publisher_address', ''),
                email=form.cleaned_data.get('new_publisher_email', '')
            )
            form.instance.publisher = publisher

        self.object = form.save()

        authors = form.cleaned_data['authors']
        new_authors = form.cleaned_data.get('new_authors')
        if new_authors:
            for name in new_authors.split(','):
                parts = name.strip().split(' ', 1)
                if len(parts) == 2:
                    first, last = parts
                else:
                    first, last = parts[0], ''
                author, created = Author.objects.get_or_create(first_name=first, last_name=last)
                authors = authors | Author.objects.filter(pk=author.pk)
        self.object.authors.set(authors)

        categories = form.cleaned_data['categories']
        new_categories = form.cleaned_data.get('new_categories')
        if new_categories:
            for cat_name in new_categories.split(','):
                category, created = Category.objects.get_or_create(category_name=cat_name.strip())
                categories = categories | Category.objects.filter(pk=category.pk)
        self.object.categories.set(categories)

        copy_formset.instance = self.object
        copy_formset.save()

        return super().form_valid(form)


class BookDeleteView(LoginRequiredMixin, AdminOnlyMixin, DeleteView):
    model = Book
    template_name = 'app/book_delete.html'
    success_url = reverse_lazy('book')
    login_url = '/accounts/login/'


# ✅ SIGN UP VIEW (ONLY ONE)
class SignUpView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_staff = False
        user.is_superuser = False
        user.save()

        login(self.request, user)
        return redirect(self.success_url)
