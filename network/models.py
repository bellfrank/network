from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# need additional modles to this file to represnt details about posts, likes, and followers.
# class Posts(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_post")
#     description = models.TextField(max_length=64)
#     time_posted = last_modified = models.DateField(auto_now_add = True)
#     status = models.BooleanField(default=True)
#     # img = models.ImageField(upload_to='images/')

#     def __str__(self):
#             return f"{self.user}: {self.description} {self.time_posted} {self.status}"


# class AuctionComments(models.Model):
#     # comment = models.CharField(max_length=500, blank=True)
#     post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="comments")
#     name = models.CharField(max_length=255, default="none")
#     body = models.CharField(max_length=255)

#     date_added = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.id}: {self.post} {self.name}"