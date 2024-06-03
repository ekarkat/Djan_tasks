from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import WorkSpaceForm
from .models import Workspace


# Create your views here.
@login_required
def create_workspace(request):
    if request.method == 'POST':
        form = WorkSpaceForm(request.POST, user=request.user)
        if form.is_valid():
            workspace = form.save(commit=False)
            workspace.owner = request.user  # Set the owner to the current user
            workspace.save()
            form.save_m2m()  # Needed because 'commit=False' doesn't save ManyToMany data
            return redirect('admin')  # Redirect to a new URL
    else:
        form = WorkSpaceForm(user=request.user)
    return render(request, 'taskmanager/create_workspace.html', context={'form': form})
