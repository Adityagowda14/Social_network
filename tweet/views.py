from django.shortcuts import render
from .models import Tweet
from .forms import UserRegistrationForm
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.views import View
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import FriendRequest
from django.db import models 
from django.contrib import messages 
from django.db.models import Q
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta
# Create your views here.

def index(request):
    return render(request, 'index.html')


def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweet_list.html', {'tweets': tweets})

class UserSignupView(View):
    def get(self, request):
        return render(request, 'registration/registration.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        serializer = UserSerializer(data={'username': username, 'email': email, 'password': password})
        if serializer.is_valid():
            user = serializer.save()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('tweet_list')
        return render(request, 'registration/registration.html', {'error': serializer.errors})

class UserLoginView(View):
    def get(self, request):
        return render(request, 'registration/login.html')

    def post(self, request):
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            response = redirect('tweet_list')  # Redirect to tweet_list after login
            response.set_cookie('access', str(refresh.access_token))
            return response
        return render(request, 'registration/login.html', {'error': 'Invalid Credentials'})
    
class UserLogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('tweet_list')  # Redirect to login page after logout
    
class UserSearchView(View):
    def get(self, request):
        query = request.GET.get('q', '').strip()
        users = []
        
        if query:
            # Exact email match
            exact_email_match = User.objects.filter(email__iexact=query)
            
            if exact_email_match.exists():
                users = exact_email_match
            else:
                # Partial name match
                users = User.objects.filter(Q(username__icontains=query))
                
        return render(request, 'user_search.html', {'users': users, 'query': query})

class SendFriendRequestView(View):
    def post(self, request, to_user_id):
        to_user = get_object_or_404(User, id=to_user_id)
        from_user = request.user
        
        cache_key = f"friend_request_count_{from_user.id}"
        current_time = timezone.now()
        
        request_times = cache.get(cache_key, [])

        request_times = [timestamp for timestamp in request_times if current_time - timestamp < timedelta(minutes=1)]
        
        if len(request_times) >= 3:
            messages.error(request, 'You have reached the limit of 3 friend requests per minute.')
        else:
            request_times.append(current_time)
            cache.set(cache_key, request_times, timeout=60)
            FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
            messages.success(request, 'Friend request has been sent.')
        
        return redirect('tweet_list')

class AcceptFriendRequestView(View):
    def post(self, request, request_id):
        friend_request = get_object_or_404(FriendRequest, id=request_id)
        if friend_request.to_user == request.user:
            friend_request.accepted = True
            friend_request.save()
        return redirect('pending_requests')

class RejectFriendRequestView(View):
    def post(self, request, request_id):
        friend_request = get_object_or_404(FriendRequest, id=request_id)
        if friend_request.to_user == request.user:
            friend_request.delete()
        return redirect('pending_requests')

class FriendsListView(View):
    def get(self, request):
        friends = User.objects.filter(
            models.Q(sent_requests__to_user=request.user, sent_requests__accepted=True) |
            models.Q(received_requests__from_user=request.user, received_requests__accepted=True)
        ).distinct()
        return render(request, 'friends_list.html', {'friends': friends})

class PendingFriendRequestsView(View):
    def get(self, request):
        pending_requests = FriendRequest.objects.filter(to_user=request.user, accepted=False)
        return render(request, 'pending_requests.html', {'pending_requests': pending_requests})



    


