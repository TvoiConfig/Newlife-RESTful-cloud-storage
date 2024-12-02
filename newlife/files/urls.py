from django.urls import path
from files.views import FileUploadView, FileEmployView

urlpatterns = [
    path('files/', FileUploadView.as_view(), name='upload-files'),
    path('files/<str:file_id>/', FileEmployView.as_view(), name='employ-file'),
]