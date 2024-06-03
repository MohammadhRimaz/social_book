from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, Post, LikePost, FollowersCount, Comment
from itertools import chain
import random
from PIL import Image
from .forms import CommentForm
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta

#login_required is using for user's can't access home page without signin...
@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    user_following_list = []

    user_following = FollowersCount.objects.filter(follower=request.user.username)
    user_following_list.append(request.user.username)

    for users in user_following:
        user_following_list.append(users.user)


    # Order the posts by creation time (newest first)
    feed_lists = Post.objects.filter(user__in=user_following_list).order_by('-created_at')

    #user suggestion starts
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)

    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if (x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))

    #Fetch active users
    active_users = Profile.objects.filter(last_seen__gte=timezone.now() - timedelta(minutes=60)).exclude(user=user_object).order_by('?')[:9]

    # Ensure the logged-in user is in the active users list
    if user_profile not in active_users:
        active_users = list(active_users)
        active_users.insert(0, user_profile)


    return render(request, 'index.html', {'user_profile':user_profile, 'posts':feed_lists, 'suggestions_username_profile_list':suggestions_username_profile_list[:4], 'active_users':active_users})

@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains= username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)

        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})

@login_required(login_url='signin')
def upload(request):
    
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        # Create a new post with the resized image  
        new_post = Post.objects.create(user= user, image= image, caption= caption)
        new_post.save()

        #Open the original image using Pillow
        img = Image.open(new_post.image.path)

        # Resize the image to your desired dimensions (e.g., width=300, height=300)
        resized_img = img.resize((1920, 1500))

        # Save the resized image
        resized_img.save(new_post.image.path)

        return redirect ('/') 
    else :
        return redirect ('/')

@login_required(login_url='signin')
def add_comment(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('/') 
    else:
        form = CommentForm()

    return render(request, 'index.html', {'form': form})

def get_comments_api(request, post_id):
    comments = Comment.objects.filter(post__id=post_id)
    comments_data = [{'user__username': comment.user.username, 'text': comment.text} for comment in comments]

    return JsonResponse({'comments': comments_data, 'user': str(request.user)})

@login_required(login_url='signin')
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # Delete the post
    post.delete_post()
    return redirect('/')

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes=post.no_of_likes-1
        post.save()
        return redirect('/')

@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))

    context = {
        'user_object' : user_object,
        'user_profile' : user_profile,
        'user_posts' : user_posts,
        'user_post_length' : user_post_length,
        'button_text' : button_text,
        'user_followers' : user_followers,
        'user_following' : user_following
    }
    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower = follower, user = user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower= follower, user= user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

            return redirect('settings')

    return render (request, 'setting.html', {'user_profile':user_profile})

def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password == password2:
            if User.objects.filter(email= email).exists():
                messages.info(request, 'This Email is Already Taken.') 
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'This Username is already Taken.')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                #create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Password does not match.')
            return redirect('signup')
    else:
        return render(request, 'signup.html')
    
def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username ,password=password)

        if user is not None:
            auth.login(request, user)
            Profile.objects.filter(user=user).update(last_seen=timezone.now())
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')
    else:
        return render(request, 'signin.html')

#this login_required is using for user's can't access logout page without login...
@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect ('signin')
