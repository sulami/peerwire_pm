from django.db import models
import markdown

class News(models.Model):
    title = models.CharField(max_length=50)
    text =  models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

    def get_markdown(self):
        return markdown.markdown(
            self.text,
            safe_mode='escape',
            output_format='html5',
            extensions=['codehilite(noclasses=true,pygments_style=friendly)']
            )

