from celery import shared_task
from .models import TaskRequest

@shared_task(bind=True)
def test_task(self):
    print(f'Request: {self.request!r}')
    for i in range(10):
        print(i)
    return 'Task executed successfully!'

@shared_task(bind=True)
def delete_requests(self):
    TaskRequest.objects.filter(answer='AC').delete()
    return 'Accepted TaskRequest deleted successfully!'
