from django.urls import path
from comments import views

urlpatterns = [
    path('comments/', views.CommentList.as_view(), name='comment_list'),
    path(
        'comments/<int:pk>/',
        views.CommentDetail.as_view(),
        name='comment_detail'
    ),
]
