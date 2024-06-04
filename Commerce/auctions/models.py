from typing import Any
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    starting_bid = models.IntegerField()
    image = models.URLField(default='https://t3.ftcdn.net/jpg/03/08/79/70/360_F_308797039_9fsJmkRwEcLJT73bk0EbGIqKpQiibfVa.jpg')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    category = models.CharField(max_length=64, default="None")
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winner", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    watchlist_users = models.ManyToManyField(User, blank=True, related_name="listingWatchlist")
    
    
class Category(models.Model):
    name = models.CharField(max_length=64)
    
    def _str__(self):
        return self.name
    
class Bid(models.Model):   
    amount = models.IntegerField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.amount} by {self.bidder} on {self.listing}"
    
class Comment(models.Model):
    comment = models.CharField(max_length=64)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    