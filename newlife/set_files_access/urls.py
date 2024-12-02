from django.urls import path
from .views import AccessView, UserFilesView, SharedFilesView

urlpatterns = [
    path('files/<str:file_id>/accesses/', AccessView.as_view(), name='access'),
    path('files/disk/', UserFilesView.as_view(), name='user-files'),
    path('shared/', SharedFilesView.as_view(), name='shared-files'),
]