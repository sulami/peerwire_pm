from haystack import indexes
from projects.models import User, Project

class ProjectIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Project

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

