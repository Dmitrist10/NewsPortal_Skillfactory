from django.db import models

class Author(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        allPosts = Post.objects.filter(author=self)
        allAuthorCommentsRating = Comment.objects.filter(user=self.user)
        allAuthorPostsCommentsRating = Comment.objects.filter(post__in=allPosts)

        postsRating = sum([post.rating * 3 for post in allPosts])
        commentsRating = sum([comment.rating for comment in allAuthorCommentsRating])
        commentsPostsRating = sum([comment.rating for comment in allAuthorPostsCommentsRating])
        
        self.rating = postsRating + commentsRating + commentsPostsRating
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    postType = models.CharField(max_length=2, choices=[('NW', 'Новость'), ('AR', 'Статья')])
    creationDate = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')

    title = models.CharField(max_length=1000)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def Like(self):
        self.rating += 1
        self.save()

    def Dislike(self):
        self.rating -= 1
        self.save()

    def preview(self) -> str:
        return self.text[:124] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    creationDate = models.DateTimeField(auto_now_add=True)

    text = models.TextField()
    rating = models.IntegerField(default=0)

    def Like(self):
        self.rating += 1
        self.save()
        
    def Dislike(self):
        self.rating -= 1
        self.save()

