from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from auctions.models import Listing
from .models import User, Bid, Comment, Category



def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
def createListing(request):
    return render(request, "auctions/createListing.html")

def addListing(request):
    if request.method == "GET":
        categories = category.objects.all()
        return render(request, "auctions/addListing.html", {
            "categories": categories
        })
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image = request.POST["image"]
        if image == "":
            image = "https://t3.ftcdn.net/jpg/03/08/79/70/360_F_308797039_9fsJmkRwEcLJT73bk0EbGIqKpQiibfVa.jpg"
        author = request.user
        category = request.POST["category"]
        active = True
        winner = None
        listing = Listing(title=title, description=description, starting_bid=starting_bid, image=image, author=author, category=category, active=active, winner=winner)
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    
def watchlist(request):
    user = request.user
    listings = user.listingWatchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })
    
def listing_view(request, id):
    listing = Listing.objects.get(id = id)
    comments = Comment.objects.filter(listing=listing)
    ListingInWatchlist = request.user in listing.watchlist_users.all()
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "ListingInWatchlist": ListingInWatchlist,
        "comments": comments
    })
    
    
def bid (request, id):
    amount = request.POST["amount"]
    listing = Listing.objects.get(id = id)
    if int(amount) > listing.starting_bid:
        bid = Bid(amount=amount, bidder=request.user, listing=listing)
        bid.save()
        listing.starting_bid = amount
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=(id,)))
    else:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "message": "Bid must be higher than the current bid."
        })
        
def addWatchlist(request, id):
    listing = Listing.objects.get(id = id)
    user = request.user
    listing.watchlist_users.add(user)
    return HttpResponseRedirect(reverse("listing", args=(id,)))

def removeWatchlist(request, id):
    listing = Listing.objects.get(id = id)
    user = request.user
    listing.watchlist_users.remove(user)
    return HttpResponseRedirect(reverse("listing", args=(id,)))

def endAuction(request, id):
    listing = Listing.objects.get(id = id)
    listing.active = False
    listing.winner = Bid.objects.filter(listing=listing).last().bidder
    listing.save()
    return HttpResponseRedirect(reverse("listing", args=(id,)))

def comment(request, id):
    comment = request.POST["comment"]
    listing = Listing.objects.get(id = id)
    commenter = request.user
    comment = Comment(comment=comment, commenter=commenter, listing=listing)
    comment.save()
    return HttpResponseRedirect(reverse("listing", args=(id,)))

def winner_msg(request, id):
    listing = Listing.objects.get(id = id)
    if listing.winner == request.user:
        return render(request, "auctions/winner_msg.html"), {
            "message": "Congratulations! You won the auction."
        }
    
def categories_view(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })
def category(request, name):
    listings = Listing.objects.filter(category=name)
    return render(request, "auctions/category.html", {
        "listings": listings
    })
