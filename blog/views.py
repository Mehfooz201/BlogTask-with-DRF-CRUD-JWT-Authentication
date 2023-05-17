from django.shortcuts import render, HttpResponseRedirect
from .forms import SignupForm, loginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import BlogPost
from django.contrib.auth.models import Group
from django.db.models import Q
from django.contrib.auth.decorators import login_required



from rest_framework.response import Response
from rest_framework import status
from .serializers import BlogPostSerializer
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from .serializers import RegistrationSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework import serializers
import uuid
from rest_framework_simplejwt.authentication import JWTAuthentication




#Registration API'S
class RegistrationAPIView(generics.GenericAPIView):
    
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        # serializer.is_valid(raise_exception = True)
        # serializer.save()
        if(serializer.is_valid()):
            serializer.save()
            return Response({
                "RequestId": str(uuid.uuid4()),
                "Message": "User created successfully",
                
                "User": serializer.data}, status=status.HTTP_201_CREATED
                )
        
        return Response({"Errors": serializers.errors}, status=status.HTTP_400_BAD_REQUEST)



# List all blog posts
class BlogPostList(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    

# Retrieve, update or delete a blog post
class BlogPostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer



# Add the Post
def addPost(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                content = form.cleaned_data['content']
                post = BlogPost(title=title, content=content)
                post = form.save(commit=False)
                post.host = request.user 
                post.save()
                form = PostForm()
                messages.success(request, 'You Post has been added !')

        else:
            form = PostForm()

        return render(request, 'blog/addpost.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')



# Update the Post
def updatePost(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi = BlogPost.objects.get(pk=id)
            form = PostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your Post has been updated !')
        else:
            pi = BlogPost.objects.get(pk=id)
            form = PostForm(instance=pi)

        return render(request, 'blog/updatepost.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')


# Update the Post
def singlePost(request, id):
    posts = BlogPost.objects.get(pk=id)
    return render(request, 'blog/detailpost.html', {'posts': posts})


# Delete the Post
def deletePost(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi = BlogPost.objects.get(pk=id)
            pi.delete()
           
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/login/')

# ------------------------------------------------------------ #

# Home
def home(request):
    posts = BlogPost.objects.all()
    return render(request, 'blog/home.html', {'posts':posts})


#Search
def searchBar(request):
    if request.method=='GET':
        query = request.GET.get('search_query')
        if query:
            posts = BlogPost.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(host__username__icontains=query) |
                Q(publication_date__icontains=query) 
            )       
        
    return render(request, 'blog/searchBar.html', {'posts':posts, 'query':query})





# ------------------------ Login and Registration with DRF Serializers -------------------- #

# Sign Up
def user_signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                messages.success(request, 'Congratulations, You have become an Author !')
                user = form.save()
                group = Group.objects.get(name='Author')
                user.groups.add(group)

        else:
            form = SignupForm()
        return render(request, 'blog/signup.html', {'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')

# Sign in
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = loginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, "Logged in Successfully !")
                    return HttpResponseRedirect('/')
        else:
            form = loginForm()
        return render(request, 'blog/login.html', {'form':form})
    else:
        return HttpResponseRedirect('/')


# Logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


