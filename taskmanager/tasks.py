from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from .models import TaskRequest, Task


@shared_task
def test_task():
    return 'Task executed successfully!'


@shared_task
def delete_acepted_requests():
    accepted_taskrequests = TaskRequest.objects.filter(answer='AC')
    if accepted_taskrequests:
        number = len(accepted_taskrequests)
        accepted_taskrequests.delete()
    return f'{number} Accepted TaskRequests deleted successfully!'


@shared_task
def check_deadline(task_id):
    task = Task.objects.get(id=task_id)
    recepient_list = [task.owner.email]
    if task.addressed_to:
        recepient_list.append(task.addressed_to.email)
    print('sending the email')
    send_mail(
        subject=f'Task {task.title} has expired!',
        message=f'Your Task {task.title} has expired! at {task.deadline}',
        from_email=settings.ADMIN_EMAIL,
        recipient_list=recepient_list,
    )
    task.status = Task.StatusChoices.EXPIRED
    task.save()
    return f'Deadline for task with id {task_id} was checked successfully!'
