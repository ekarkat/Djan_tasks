from rest_framework.routers import DefaultRouter 
from django.urls import path

from .user.views import UserProfileViewSet
from .workspace.views import WorkspaceViewSet
from .unit.views import UnitViewSet
from .task.views import TaskViewSet
from .generic.views import TaskRequestViewSet

# urlpatterns = [
#     path('users/', views.user_list, name='user_list'),
# ]


router = DefaultRouter()
router.register(r'users', UserProfileViewSet, basename='user')
router.register(r'workspaces', WorkspaceViewSet, basename='workspace')
router.register(r'units', UnitViewSet, basename='units')
router.register(r'tasks', TaskViewSet, basename='tasks')
router.register(r'tasksrequest', TaskRequestViewSet, basename='tasksrequest')
urlpatterns = router.urls
