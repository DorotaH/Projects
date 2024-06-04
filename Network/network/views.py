from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView
from django.core.paginator import Paginator
import json

from .models import User, Post, Likes


class IndexView(ListView):
    template_name = 'network/index.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.all().order_by('-timestamp')

    def post(self, request):
        content = request.POST["post_content"]
        if content is None or content.strip() == '':
            self.object_list = self.get_queryset()
            return self.render_to_response(self.get_context_data(
                message="Content of the post cannot be empty.",
                current_user=request.user
            ))
        else:
            author = request.user
            post = Post(author=author, content=content)
            post.save()
            return HttpResponseRedirect(reverse("index"))
    


class ProfileView(ListView):
    template_name = 'network/profile.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(author__username=self.kwargs['username']).order_by('-timestamp')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs['username']
        user = User.objects.get(username=username)
        context['profile_user'] = username
        context['followers'] = user.followers.count()
        context['following'] = user.following.count()
        if self.request.user.is_authenticated:
            context['is_following'] = self.request.user in user.followers.all()
            context['current_user'] = self.request.user.username
        else:
            context['is_following'] = None
            context['current_user'] = None
        return context


class LoginView(View):
    def get(self, request):
        return render(request, "network/login.html")

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class RegisterView(View):
    def get(self, request):
        return render(request, "network/register.html")

    def post(self, request):
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))


class EditView(View):
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        return JsonResponse({
            'post': post.serialize()
        }, safe=False, content_type='application/json')

    def post(self, request, post_id):
        try:
            data = json.loads(request.body)
            post = Post.objects.get(id=post_id)
            post.content = data['content']
            post.save()
            return JsonResponse({"message":"Post updated succesfully", "content": post.content})
        except:
            return JsonResponse({"error": "Something went wrong"})


class FollowView(View):
    def get(self, request, username):
        user = User.objects.get(username=username)
        data = {
            "username": username,
            "followers": user.followers.count(),
            "following": user.following.count(),
        }
        if request.user.is_authenticated:
            data['is_following'] = request.user in user.followers.all()
            data['current_user'] = request.user.username
        else:
            data['is_following'] = None
            data['current_user'] = None
        return JsonResponse(data, safe=False, content_type='application/json')

    def post(self, request, username):
        user = User.objects.get(username=username)
        if request.user in user.followers.all():
            user.followers.remove(request.user)
            request.user.following.remove(user)
            is_following = False
        else:
            user.followers.add(request.user)
            request.user.following.add(user)
            is_following = True
        return JsonResponse({
            'is_following': is_following,
            'following': request.user.followers.count(),
            'followers': request.user.following.count()
        }, safe=False, content_type='application/json')


class ManageLikesView(View):
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        likes = Likes.objects.filter(post=post)
        user_has_liked = request.user in [like.user for like in likes]
        return JsonResponse({
            'likes': len(likes),
            'is_liked': user_has_liked,
            'is_authenticated': request.user.is_authenticated
        }, safe=False, content_type='application/json')

    def post(self, request, post_id):        
        post = Post.objects.get(id=post_id)
        likes = Likes.objects.filter(post=post)
        user_has_liked = request.user in [like.user for like in likes]
        if user_has_liked:
            like = Likes.objects.get(user=request.user, post=post)
            like.delete()
        else:
            like = Likes(user=request.user, post=post)
            like.save()

        return JsonResponse({
            'likes': len(Likes.objects.filter(post=post)),
            'is_liked': user_has_liked,
            'is_authenticated': request.user.is_authenticated
        }, safe=False, content_type='application/json')


class FollowingView(LoginRequiredMixin, ListView):
    template_name = 'network/following.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(author__in=self.request.user.following.all()).order_by('-timestamp')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.request.user
        return context