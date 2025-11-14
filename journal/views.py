from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def index(request):
    """Главная страница приложения"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added') if request.user.is_authenticated else Topic.objects.none()
    return render(request, 'journal/index.html', {'topics': topics})

def topics(request):
    """Список всех тем"""
    topics = Topic.objects.order_by('date_added')
    return render(request, 'journal/topics.html', {'topics': topics})

def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('date_added')
    context = {'topic':topic, 'entries':entries}
    return render(request, 'journal/topic.html', context)

@login_required
def new_topic(request):
    """Создание новой темы"""
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('journal:topics')
    
    return render(request, 'journal/new_topic.html', {'form': form})

@login_required
def new_entry(request, topic_id):
    """Добавление новой записи к теме"""
    topic = get_object_or_404(Topic, id=topic_id)
    
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('journal:topic', topic_id=topic_id)
    
    return render(request, 'journal/new_entry.html', {'topic': topic, 'form': form})

@login_required
def edit_entry(request, entry_id):
    """Редактирование существующей записи"""
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic
    
    if topic.owner != request.user:
        return redirect('journal:topic', topic_id=topic.id)
    
    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('journal:topic', topic_id=topic.id)
    
    return render(request, 'journal/edit_entry.html', {'entry': entry, 'topic': topic, 'form': form})

@login_required
def edit_topic(request, topic_id):
    """Редактирование существующей темы"""
    topic = get_object_or_404(Topic, id=topic_id)
    
    if topic.owner != request.user:
        return redirect('journal:topics')
    
    if request.method != 'POST':
        form = TopicForm(instance=topic)
    else:
        form = TopicForm(instance=topic, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('journal:topics')
    
    return render(request, 'journal/edit_topic.html', {'topic': topic, 'form': form})