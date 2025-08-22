from django.urls import path
from .views import BookListView, toggle_favorite, upload_book, book_detail, search_books, delete_book, edit_book, analyze_book, preview_book
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('upload/', upload_book, name='upload_book'),
    path('book/<int:pk>/', book_detail, name='book_detail'),
    path('book/<int:pk>/edit/', edit_book, name='edit_book'),
    path('book/<int:pk>/delete/', delete_book, name='delete_book'),
    path('search/', search_books, name='search_books'),
    path('toggle-favorite/<int:pk>/', toggle_favorite, name='toggle_favorite'),
    path('book/<int:pk>/analyze/', analyze_book, name='analyze_book'),
    path("books/book/<int:pk>/preview/<int:page>/", views.preview_book, name="preview_book"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)