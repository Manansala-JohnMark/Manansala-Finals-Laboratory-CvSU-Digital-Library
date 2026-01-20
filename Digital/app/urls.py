from django.urls import path
from .views import (
    HomePageView,
    AboutPageView,
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
)
from django.contrib.auth import views as auth_views
from .views import SignUpView


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('books/', BookListView.as_view(), name='book'),
    path('books/create/', BookCreateView.as_view(), name='book_create'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('books/<int:pk>/edit/', BookUpdateView.as_view(), name='book_update'),
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book_delete'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/',auth_views.LoginView.as_view(template_name='registration/login.html'),name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
