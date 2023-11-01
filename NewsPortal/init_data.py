from django.contrib.auth.models import User

from news.models import Author, Category, Post, Comment

# Создаем двух пользователей
user1 = User.objects.create_user('user1')
user2 = User.objects.create_user('user2')

# Создаем два объекта модели Author, связанные с пользователями
author1 = Author.objects.create(user=user1)
author2 = Author.objects.create(user=user2)

# Создаем четыре категории
category1 = Category.objects.create(name="Спорт")
category2 = Category.objects.create(name="Политика")
category3 = Category.objects.create(name="Образование")
category4 = Category.objects.create(name="Наука")

# Создаем две статьи и одну новость
post1 = Post.objects.create(author=author1, post_type="article", title="Статья 1", text="Текст статьи 1")
post2 = Post.objects.create(author=author2, post_type="article", title="Статья 2", text="Текст статьи 2")
post3 = Post.objects.create(author=author1, post_type="news", title="Новость 1", text="Текст новости 1")

# Присваиваем им категории (минимум две категории на статью/новость)
post1.categories.add(category1, category2)
post2.categories.add(category2, category3)
post3.categories.add(category3, category4)

# Создаем четыре комментария к разным объектам модели Post
comment1 = Comment.objects.create(post=post1, user=user1, text="Комментарий к статье 1")
comment2 = Comment.objects.create(post=post1, user=user2, text="Комментарий к статье 1")
comment3 = Comment.objects.create(post=post2, user=user1, text="Комментарий к статье 2")
comment4 = Comment.objects.create(post=post3, user=user2, text="Комментарий к новости 1")

# Применяем функции like() и dislike() к статьям/новостям и комментариям
post1.like()
post2.dislike()
comment1.like()
comment2.dislike()

# Обновляем рейтинги пользователей
author1.update_rating()
author2.update_rating()

# Выводим username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта)
best_author = Author.objects.order_by('-rating').first()
print(f"Лучший пользователь: {best_author.user.username}, Рейтинг: {best_author.rating}")

# Выводим дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи,
# основываясь на лайках/дислайках к этой статье
best_post = Post.objects.filter(post_type="article").order_by('-rating').first()
print(f"Дата добавления: {best_post.created_at}")
print(f"Username автора: {best_post.author.user.username}")
print(f"Рейтинг статьи: {best_post.rating}")
print(f"Заголовок статьи: {best_post.title}")
print(f"Превью статьи: {best_post.preview()}")

# Выводим все комментарии к этой статье (дата, пользователь, рейтинг, текст)
comments_to_best_post = Comment.objects.filter(post=best_post)
for comment in comments_to_best_post:
    print(f"Дата: {comment.created_at}")
    print(f"Пользователь: {comment.user.username}")
    print(f"Рейтинг комментария: {comment.rating}")
    print(f"Текст комментария: {comment.text}")
    print()
