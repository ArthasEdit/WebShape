from django.urls import path
from . import views
 

app_name = 'core'

urlpatterns = [
    path('core/', views.core, name='core'),
    path('core_reversed/', views.core_reversed, name='core_reversed'),
    path('test/<int:vw>/', views.check_answer, name='check_answer'),
    path('reset/', views.reset, name='reset'),
    path('', views.manage_words, name='manage_words'),
    path('new_words/submit/', views.generate_words, name='generate_words'),
    path('manage_words/delete_words/', views.delete_words, name='delete'),
    path('core_reversed/test/<int:vw>/', views.check_answer_reversed, name='check_reversed'),
    path('core_reversed/<str:name>/', views.core_filter, name='filter_reverse'),
    path('core/<str:name>/', views.core_filter, name='filter'),
    path('api/words/', views.VocabularyWordList.as_view(), name='word-list'),
    path('api/words/<int:pk>/', views.VocabularyWordDetail.as_view(), name='word-detail'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('manage_words/filter/<str:sub_name>/', views.manage_words_filter, name='manage_filter' ),
]
