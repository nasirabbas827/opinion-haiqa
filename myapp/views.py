from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import user_registerForm, LoginForm, CommentForm, UserUpdateForm
from .models import user_register, Post, Comment
import nltk
from nltk.corpus import sentiwordnet as sentiworddictionary
from nltk.corpus import wordnet

# Ensure necessary NLTK resources are downloaded
nltk.download('sentiwordnet')
nltk.download('wordnet')

def register(request):
    if request.method == 'POST':
        form = user_registerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = user_registerForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = user_register.objects.get(username=username)
                if user.password == password:
                    request.session['username'] = username
                    messages.success(request, 'Login successful!')
                    return redirect('home')
                else:
                    messages.error(request, 'Invalid password.')
            except user_register.DoesNotExist:
                messages.error(request, 'Username does not exist.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def home(request):
    username = request.session.get('username')
    if not username:
        return redirect('login')

    # Fetch all posts
    posts = Post.objects.all()

    # Calculate the average sentiment score for each post and classify it
    post_with_sentiments = []
    for post in posts:
        comments = Comment.objects.filter(post=post)
        if comments.exists():
            avg_sentiment_score = sum(comment.sentiment_score for comment in comments if comment.sentiment_score is not None) / comments.count()
        else:
            avg_sentiment_score = 0  # Default score if no comments

        # Classify sentiment
        if avg_sentiment_score > 0.5:
            sentiment_classification = 'Good'
        elif avg_sentiment_score >= 0:
            sentiment_classification = 'Neutral'
        elif avg_sentiment_score > -0.5:
            sentiment_classification = 'Bad'
        else:
            sentiment_classification = 'Worst'

        post_with_sentiments.append({
            'post': post,
            'avg_sentiment_score': avg_sentiment_score,
            'sentiment_classification': sentiment_classification,
        })

    # Sort posts by average sentiment score (highest first)
    sorted_posts = sorted(post_with_sentiments, key=lambda x: x['avg_sentiment_score'], reverse=True)

    context = {
        'username': username,
        'posts_with_sentiments': sorted_posts,
    }
    return render(request, 'home.html', context)


def calculate_sentiment(comment_text):
    sentiment_score = 0.0
    sentiment_label = 'neutral'

    
    words = comment_text.split()

    for word in words:
        synsets = wordnet.synsets(word)
        if not synsets:
            continue


        synset = synsets[0]

        swn_synset = sentiworddictionary.senti_synset(synset.name())
        
        sentiment_score += swn_synset.pos_score() - swn_synset.neg_score()

    if sentiment_score > 0:
        sentiment_label = 'positive'
    elif sentiment_score < 0:
        sentiment_label = 'negative'

    return sentiment_score, sentiment_label

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    username = request.session.get('username')

    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            sentiment_score, sentiment_label = calculate_sentiment(text)
            if Comment.objects.filter(post=post, username=username).exists():
                messages.error(request, 'You have already commented on this post.')
            else:
                Comment.objects.create(
                    post=post,
                    username=username,
                    text=text,
                    sentiment_score=sentiment_score,
                    sentiment_label=sentiment_label
                )
                messages.success(request, f'Comment added successfully! Sentiment: {sentiment_label.capitalize()}')
        else:
            messages.error(request, 'Comment text cannot be empty.')

    comments = Comment.objects.filter(post=post)
    context = {
        'post': post,
        'comments': comments,
    }
    return render(request, 'post_detail.html', context)

def comment_on_post(request, post_id):
    username = request.session.get('username')
    if not username:
        return redirect('login')

    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            sentiment_score, sentiment_label = calculate_sentiment(text)
            Comment.objects.create(
                post=post,
                username=username,
                text=text,
                sentiment_score=sentiment_score,
                sentiment_label=sentiment_label
            )
            messages.success(request, f'Comment added successfully! Sentiment: {sentiment_label.capitalize()}')
        else:
            messages.error(request, 'Comment text cannot be empty.')

    return redirect('home')

def logout_view(request):
    request.session.flush()
    messages.success(request, 'Logged out successfully!')
    return redirect('login')

def update_profile(request):
    username = request.session.get('username')
    if not username:
        return redirect('login')

    user = get_object_or_404(user_register, username=username)

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('home')
    else:
        form = UserUpdateForm(instance=user)

    return render(request, 'update_profile.html', {'form': form})
