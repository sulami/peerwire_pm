from django.db import models

class News(models.Model):
    title = models.CharField(max_length=50)
    text =  models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

