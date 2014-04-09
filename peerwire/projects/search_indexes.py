from haystack import indexes
from projects.models import User, Project

class ProjectIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    status = indexes.CharField(model_attr='status', faceted=True)
    seeking = indexes.CharField(model_attr='seeking', faceted=True)
    level = indexes.CharField(model_attr='level', faceted=True)

    def get_model(self):
        return Project

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

