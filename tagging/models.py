


from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=255)
    embedding = models.JSONField()  

    def __str__(self):
        return self.name



class TaggedContent(models.Model):
    content = models.TextField()
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if(len(self.content)>=50):
            return self.content[:50] + '...'
        else :
            return self.content