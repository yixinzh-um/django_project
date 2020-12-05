from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.conf import settings



class Location(models.Model) :
    name = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Location must be greater than 2 characters")]
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
 
    def __str__(self) :
        return self.name


class Employer(models.Model) :
    name = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Employer must be greater than 2 characters")]
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    description = models.TextField(null=True,blank=True)
    def __str__(self) :
        return self.name


class Job(models.Model) :
    title = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Employer must be greater than 2 characters")]
    )
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE,null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE,null=True)
    salary_l = models.IntegerField(null=True)
    salary_h = models.IntegerField(null=True)
    description = models.TextField()
    # rating = models.DecimalField(max_digits=2, decimal_places=1, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    comments = models.ManyToManyField(settings.AUTH_USER_MODEL,
        through='Comment', related_name='comments_owned')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Picture
    # picture = models.BinaryField(null=True, blank=True, editable=True)
    # content_type = models.CharField(max_length=256, null=True, blank=True,
    #                                 help_text='The MIMEType of the file')

    # Favorites
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL,
        through='Fav', related_name='favorite_jobs')
    
    # Shows up in the admin list
    def __str__(self):
        return self.title

class Comment(models.Model) :
    text = models.TextField(
        validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")]
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shows up in the admin list
    def __str__(self):
        if len(self.text) < 15 : return self.text
        return self.text[:11] + ' ...'

class Fav(models.Model) :
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # https://docs.djangoproject.com/en/3.0/ref/models/options/#unique-together
    class Meta:
        unique_together = ('job', 'user')

    def __str__(self) :
        return '%s likes %s'%(self.user.username, self.job.title[:10])

