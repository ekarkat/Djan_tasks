from django.contrib import admin

from .models import WorkSpace
from .models import Unit
from .models import Task
from .models import TaskRequest
from .models import TaskComment, WorkSpaceComment, UnitComment

# Register your models here.
admin.site.register(WorkSpace)
admin.site.register(Unit)
admin.site.register(Task)
# admin.site.register(TaskRequest)
# admin.site.register(TaskComment)
# admin.site.register(WorkSpaceComment)
# admin.site.register(UnitComment)
