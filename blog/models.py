from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateField(default=timezone.now)
    published_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['-published_date']

    def body_prev(self):
        text_list = self.text.split(' ')
        if len(text_list) > 20:
            return ' '.join(text_list[:20])
        return self.text

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"pk": self.pk})
    


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)


    def approve(self ):
        self.approved_comment = True
        self.save()
    
    def get_absolute_url(self):
        return reverse("blog:detail")
    

    def __str__(self):
        return self.author
