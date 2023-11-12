from django.urls import path
from .views import core, check_answer, reset, generate_words, delete_words, manage_words, core_reversed,check_answer_reversed, subject_core, VocabularyWordList, VocabularyWordDetail, register, user_login, manage_words_filter

app_name = 'core'

urlpatterns = [
    path('core/', core, name='core'),
    path('core_reversed/', core_reversed, name='core_reversed'),
    path('test/<int:vw>', check_answer, name='check_answer'),
    path('reset/', reset, name='reset'),
    path('', manage_words, name='manage_words'),
    path('new_words/submit', generate_words, name='generate_words'),
    path('manage_words/delete_words', delete_words, name='delete'),
    path('core_reversed/test/<int:vw>', check_answer_reversed, name='check_reversed'),
    path('core_reversed/<str:subject_name>/', subject_core, name='subject_view'),
    path('api/words/', VocabularyWordList.as_view(), name='word-list'),
    path('api/words/<int:pk>/', VocabularyWordDetail.as_view(), name='word-detail'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('manage_words/filter/<str:sub_name>/', manage_words_filter, name='manage_filter' ),
]
