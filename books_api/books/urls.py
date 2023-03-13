from django.urls import path
from . import views
 
urlpatterns = [
    path('createTable', views.create_table),
    path('books', views.book_list),
    path('books/<int:pk>', views.book_detail),
    path('book/upvote/<int:pk>', views.upvote_book),
]