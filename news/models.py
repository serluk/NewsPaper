from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.IntegerField(default=0)

    def update_rating(self):
        post_rat = self.post_set.all().aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += post_rat.get('postRating')

        comment_rat = self.authorUser.comment_set.all().aggregate(commentRat=Sum('rating'))
        cRat = 0
        cRat += comment_rat.get('commentRat')

        self.ratingAuthor = pRat * 3 * cRat
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    news = 'nw'
    article = 'ar'

    types_article = [
        (news, 'Новости'),
        (article, 'Статья')
    ]

    article_type = models.CharField(max_length=2, choices=types_article, default=news)
    add_time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.TextField()
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:124] + '...'

    def __str__(self):
        return f'{self.title}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        try:
            return self.comment_post.author.user.username
        except:
            return self.comment_user.username