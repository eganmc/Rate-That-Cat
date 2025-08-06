from django.db import models

# Create your models here.

class Cat(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='cats/')
    description = models.TextField(blank=True)
    rating = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=50)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author_name}'