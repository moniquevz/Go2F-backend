from django.db import models
from django.contrib.auth.models import User
from cities_light.models import City, Country
from django.db.models.signals import post_save

# Create your models here.


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(null=True, blank=True,
                              default='/placeholder.png')
    category = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    rating = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return self.name


class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(null=True, blank=True,
                              default='/placeholder.png')
    category = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    rating = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return self.name


# Creates timestamp for each like of a post (using through function on likes field in Post model below)
class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=200)                            # required field
    description = models.TextField(max_length=3000)                     # required field
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='post_user', blank=True, through=PostLike)
    comments = models.ManyToManyField('Comment', related_name='post_comment', blank=True)
    _id = models.AutoField(primary_key=True, editable=False)

    class Meta:
        ordering = ['-_id']                                             # reorders posts to show newest first

    def __str__(self):
        return self.title + "(" + str(self._id) + ")"


# Creates timestamp for each like of a post (using through function on likes field in Post model below)
class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    detail = models.TextField(max_length=3000)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='comment_user', blank=True, through=CommentLike)
    _id = models.AutoField(primary_key=True, editable=False)
    
    def __str__(self):
        return self.detail


class Template(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(null=True, blank=True,
                              default='/placeholder.png')
    category = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    rating = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return self.name


class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    category = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)
    website = models.CharField(max_length=100, default='SOME STRING')

    def __str__(self):
        return self.name

class ExclusiveContent(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    category = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)
    website = models.CharField(max_length=100, default='SOME STRING')

    def __str__(self):
        return self.name

class Star(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True, default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.rating)


class FollowerRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


# Profile edit choices
EXP_CHOICES = [
    ("Entry Level", "Entry Level (0-1 year)"),
    ("Junior", "Junior (1-2 years)"),
    ("Mid-level", "Mid-level (2-5 years)"),
    ("Senior", "Senior (5-8 years)"),
    ("Director", "Director (8+ years)"),
]

CLIENT_CHOICES = [
    ("0-5", "0-5 clients"),
    ("5-20", "5-20 clients"),
    ("20+", "20+ clients"),
]


BOOL_CHOICES = [
    ("True", "Yes"),
    ("False", "No"),
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(null=True, blank=True, default='/placeholder.png')
    cover_image = models.ImageField(null=True, blank=True, default='/placeholder.png')
    f_name = models.CharField("First name", max_length=25, null=True, blank=True)
    l_name = models.CharField("Last name", max_length=50, null=True, blank=True)
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.SET_NULL)
    city = models.ForeignKey(City, null=True, blank=True, on_delete=models.SET_NULL)
    website_url = models.URLField("Website address", null=True, blank=True)
    website_hide = models.BooleanField("Hide this link from my public profile", default=False)
    #industry = models.CharField("Professional Title", max_length=60, null=True, blank=True)
    title = models.CharField("Professional Title", max_length=60, null=True, blank=True)
    experience = models.CharField("Years of Experience as a Freelancer", max_length=35,
                                  choices=EXP_CHOICES, default="Entry Level")
    clients = models.CharField("How many clients do you manage?", max_length=15, choices=CLIENT_CHOICES, default="0-5")
    hires = models.CharField("Do you hire others?", max_length=6, choices=BOOL_CHOICES, default="No")
    #req_services = models.CharField("Professional Title", max_length=60, null=True, blank=True)
    #req_tools = models.CharField("Professional Title", max_length=60, null=True, blank=True)
    #curr_services = models.CharField("Professional Title", max_length=60, null=True, blank=True)
    #skills = models.CharField("Professional Title", max_length=60, null=True, blank=True)
    bio = models.TextField("About me", max_length=3000, blank=True, null=True)
    linkedin = models.URLField("LinkedIn", null=True, blank=True)
    linkedin_hide = models.BooleanField("Hide this link from my public profile", default=False)
    instagram = models.URLField("Instagram", null=True, blank=True)
    insta_hide = models.BooleanField("Hide this link from my public profile", default=False)
    twitter = models.URLField("Twitter", null=True, blank=True)
    twitter_hide = models.BooleanField("Hide this link from my public profile", default=False)
    github = models.URLField("Github", null=True, blank=True)
    github_hide = models.BooleanField("Hide this link from my public profile", default=False)
    dribble = models.URLField("Dribble", null=True, blank=True)
    dribble_hide = models.BooleanField("Hide this link from my public profile", default=False)
    behance = models.URLField("Behance", null=True, blank=True)
    behance_hide = models.BooleanField("Hide this link from my public profile", default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)

    def __str__(self):
        return "User " + str(self.user.pk) + " (" + str(self.user.first_name) + " " + str(self.user.last_name)+ ")"


# Receiver function for post_save signal below
def user_did_save(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


# Creates profile when new user is saved
post_save.connect(user_did_save, sender=User)