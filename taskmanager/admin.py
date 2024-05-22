from django.contrib import admin

from .models import WorkSpace
from .models import Unit
from .models import Task


# Register your models here.
admin.site.register(WorkSpace)
admin.site.register(Unit)
admin.site.register(Task)