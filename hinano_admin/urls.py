from django.contrib import admin
from django.urls import path, include
# from django.http import HttpResponse
from . import views
from django.conf import settings
from django.conf.urls.static import static
import static

urlpatterns = [
    path('admin/', admin.site.urls),
    #login
    path('', views.index, name='login'),
    path('logout', views.logout, name='logout'),
    path('postsignIn/', views.postsignIn),
    #dashboards
    path('dashboards', views.dashboards, name='dashboards'),
    # users
    path('users', views.users_index, name='users'),
    path('users/<str:id>', views.users_read),
    path('users_create', views.Users_create.as_view()),
    path('users_update/<str:id>', views.Users_update.as_view(), name='user-update'),
    path('users_delete/<str:id>', views.Users_delete.as_view(), name='user-delete'),
    # topics
    path('topics', views.topics_index, name='topics'),
    path('topics/<str:id>', views.topics_read),
    path('topics_create', views.Topics_create.as_view()),
    path('topics_update/<str:id>', views.Topics_update.as_view(), name='topic-update'),
    path('topics_delete/<str:id>', views.Topics_delete.as_view(), name='topic-delete'),
    #quizzes
    path('quizzes', views.quizzes_index, name='quizzes'),
    path('quizzes/<str:id>', views.quizzes_read),
    path('quizzes_create', views.Quizzes_create.as_view()),
    path('quizzes_update/<str:id>', views.Quizzes_update.as_view(), name='quizze-update'),
    path('quizzes_delete/<str:id>', views.Quizzes_delete.as_view(), name='quizze-delete'),
    # records
    path('records', views.records_index, name='records'),
    path('records/<str:id>', views.records_read),
    #contents
    path('contents', views.contents_index, name='contents'),
    path('contents/<str:id>', views.contents_read),
    path('contents_create', views.Contents_create.as_view()),
    path('contents_update/<str:id>', views.Contents_update.as_view(), name='content-update'),
    path('contents_delete/<str:id>', views.Contents_delete.as_view(), name='content-delete'),
    #comments
    path('comments', views.comments_index, name='comments'),
    path('comments/<str:id>', views.comments_read),

    path('login', views.login),
    path('inputfile', views.inputfile),
]
# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)