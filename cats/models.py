from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg

# Create your models here.

class Cat(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='cats/')
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cats')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def average_rating(self):
        avg = self.ratings.aggregate(Avg('score'))['score__avg']
        return round(avg, 1) if avg else 0
    
    def total_ratings(self):
        return self.ratings.count()


class Rating(models.Model):
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('cat', 'user')  # Prevents duplicate ratings
    
    def __str__(self):
        return f'{self.user.username} rated {self.cat.name}: {self.score}'


class Comment(models.Model):
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.cat.name}'
    
    def user_rating(self):
        try:
            rating = Rating.objects.get(cat=self.cat, user=self.user)
            return rating.score
        except Rating.DoesNotExist:
            return None