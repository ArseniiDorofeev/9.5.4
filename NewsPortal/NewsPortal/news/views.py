from audioop import reverse
from datetime import date

from django import forms
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.edit import UpdateView
from pyexpat.errors import messages

from .models import AuthorRequest
from .models import News, Article, Post, Category
from .models import UserProfile


def news_list(request):
    news = Post.objects.order_by('-date_create')
    paginator = Paginator(news, 10)  # Разбиваем на страницы, по 10 новостей на каждой
    page = request.GET.get('page')
    news = paginator.get_page(page)
    return render(request, 'news/news_list.html', {'news': news})


def news_search(request):
    query = request.GET.get('q')
    results = Post.objects.filter(
        Q(title__icontains=query) |  # Поиск по названию
        Q(author__icontains=query) |  # Поиск по автору
        Q(date_create__gte=query)  # Поиск по дате
    )
    return render(request, 'news/news_search.html', {'results': results})


def news_detail():
    return None


class NewsForm:
    def is_valid(self):
        pass

    def save(self, commit):
        pass


class NewsCreateView(CreateView):
    model = News
    form_class = NewsForm
    template_name = 'news/news_form.html'
    success_url = reverse_lazy('news_list')


class NewsUpdateView(UpdateView):
    model = News
    form_class = NewsForm
    template_name = 'news/news_form.html'
    success_url = reverse_lazy('news_list')


class NewsDeleteView(DeleteView):
    model = News
    template_name = 'news/news_confirm_delete.html'
    success_url = reverse_lazy('news_list')


class ArticleForm:
    pass


class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'news/article_form.html'
    success_url = reverse_lazy('article_list')


class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'news/article_form.html'
    success_url = reverse_lazy('article_list')


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = 'news/article_confirm_delete.html'
    success_url = reverse_lazy('article_list')


class ProfileUpdateView(UpdateView):
    model = UserProfile
    fields = ['first_name', 'last_name', 'email', 'avatar']
    template_name = 'profile_update.html'

    # Добавляем декоратор @login_required
    @login_required
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


from django.contrib.auth.models import User, Group

# Создание пользователя
user = User.objects.create_user('имя_пользователя', 'почта', 'пароль')

# Добавление пользователя в группу "common"
common_group = Group.objects.get(name='common')
user.groups.add(common_group)

# Добавление пользователя в группу "authors"
authors_group = Group.objects.get(name='authors')
user.groups.add(authors_group)


class AuthorRequestForm(forms.ModelForm):
    class Meta:
        model = AuthorRequest
        fields = []


def request_author_status(request):
    if request.method == 'POST':
        form = AuthorRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('author_request_list')
    else:
        form = AuthorRequestForm()
    return render(request, 'request_author_status.html', {'form': form})


def author_request_list(request):
    author_requests = AuthorRequest.objects.all()
    return render(request, 'author_requests.html', {'author_requests': author_requests})


def approve_author_request(request, request_id):
    author_request = AuthorRequest.objects.get(id=request_id)
    if request.method == 'POST':
        # Обработка одобрения запроса
        author_request.approved = True
        author_request.save()
        return redirect('author_request_list')
    return render(request, 'approve_author_request.html', {'author_request': author_request})


def reject_author_request(request, request_id):
    author_request = AuthorRequest.objects.get(id=request_id)
    if request.method == 'POST':
        # Обработка отклонения запроса
        author_request.approved = False
        author_request.save()
        return redirect('author_request_list')
    return render(request, 'reject_author_request.html', {'author_request': author_request})


@login_required
def subscribe_to_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    request.user.subscribed_posts.add(category)
    return HttpResponseRedirect(reverse('category_detail', args=[category_id]))


@login_required
def unsubscribe_from_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    request.user.subscribed_posts.remove(category)
    return HttpResponseRedirect(reverse('category_detail', args=[category_id]))


@login_required
def create_post(request):
    new_post = Post.objects.create(title="Новая статья", content="Содержание новой статьи", category_id=1)  # Пример
    new_post.save()

    subscribers = new_post.category.subscribers.all()
    for subscriber in subscribers:
        subject = f"Новая статья в вашей подписке: {new_post.title}"
        message = f"Здравствуйте, {subscriber.username}!\nНовая статья в вашей подписке: {new_post.title}\n\n{new_post.content}"
        from_email = "noreply@example.com"
        recipient_list = [subscriber.email]

        send_mail(subject, message, from_email, recipient_list)

    return redirect('news_list')


def send_news_to_subscribers(news, subscribers):
    subject = "Новая новость в категории " + news.category
    message = f"Здравствуйте!\n\nНовость в категории {news.category}:\n{news.title}\n\n{news.content}"
    from_email = "your_email@example.com"
    recipient_list = [subscriber.email for subscriber in subscribers]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
