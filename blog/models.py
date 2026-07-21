from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=200)
    topic = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='blogs/')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        db_table = 'core_blog'

    def __str__(self):
        return self.title

    @property
    def short_description(self):
        words = self.description.split()
        if len(words) > 20:
            return ' '.join(words[:20]) + '...'
        return self.description
