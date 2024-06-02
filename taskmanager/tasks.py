from celery import shared_task
from .models import TaskRequest

@shared_task(bind=True)
def test_task(self):
    for i in range(2):
        print(i)
    return 'Task executed successfully!'

@shared_task(bind=True)
def delete_acepted_requests(self):
    accepted_tasks = TaskRequest.objects.filter(answer='AC')
    if accepted_tasks:
        number = len(accepted_tasks)
        accepted_tasks.delete()
    return f'{number} Accepted TaskRequests deleted successfully!'
