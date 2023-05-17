from django.db import models
from django.contrib.auth.models import User




# Create your models here.
class BlogPost(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    tags = models.CharField(max_length=100)

    #Most Updated and Created Rooms here. Most recents 
    class Meta:
        ordering = ['-publication_date']  
    
    def save(self, *args, **kwargs):
        # Update the 'last_blog' field of the author when a new blog post is created
        created = not self.pk  # Check if the object is being created for the first time
        super().save(*args, **kwargs)
        if created:
            self.host.last_blog = self
            self.host.save()

    def __str__(self):
        return str(self.title)
    
