from django.shortcuts import render

# Create your views here.

# messaging/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message,User
from .forms import MessageForm

@login_required
def send_message(request, recipient_id):
    recipient = User.objects.get(id=recipient_id)
    
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
    received_messages = Message.objects.filter(receiver=request.user)
    sent_messages = Message.objects.filter(sender=request.user)
    
    return render(request, 'messaging/inbox.html', {
        'received_messages': received_messages,
        'sent_messages': sent_messages,
    })

@login_required
def message_detail(request, message_id):
    # View the message details
    message = Message.objects.get(id=message_id)
    if message.receiver != request.user and message.sender != request.user:
        return redirect('messaging:inbox')  # Unauthorized access if not sender or receiver
    
    return render(request, 'messaging/message_detail.html', {'message': message})

