from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message
from .forms import MessageForm

# Create your views here.

# messaging/views.py
@login_required
def send_message(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = recipient
            message.save()
            return redirect('messaging:inbox')
    else:
        form = MessageForm()

    return render(request, 'messaging/send_message.html', {'form': form, 'recipient': recipient})

@login_required
def inbox(request):
    # Get messages for the logged-in user (both sent and received)
    received_messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    sent_messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
    
    # Get all users except the current user
    all_users = User.objects.exclude(id=request.user.id)
    
    return render(request, 'messaging/inbox.html', {
        'received_messages': received_messages,
        'sent_messages': sent_messages,
        'all_users': all_users,
    })

@login_required
def message_detail(request, message_id):
    # View the message details
    message = get_object_or_404(Message, id=message_id)
    if message.receiver != request.user and message.sender != request.user:
        return redirect('messaging:inbox')  # Unauthorized access if not sender or receiver
    
    return render(request, 'messaging/message_detail.html', {'message': message})

