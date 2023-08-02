from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegistrationForm, UserForm, ProfileForm, SavedCoinForm
from .models import Profile, SavedCoin
from django.http import Http404, JsonResponse

import requests

# Create your views here.
def home(request):
    url = "https://coinranking1.p.rapidapi.com/coins"

    querystring = {"referenceCurrencyUuid":"yhjMzLPhuIDl","timePeriod":"24h","tiers[0]":"1","orderBy":"marketCap","orderDirection":"desc","limit":"50","offset":"0"}

    headers = {
        "X-RapidAPI-Key": "c08d086787msh739f2577cb5be6dp1562d2jsne92fba0598e2",
        "X-RapidAPI-Host": "coinranking1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json() 
    coins = data['data']['coins']

    context = {
        'coins': coins,
    }

    # for coin in coins:  
    #     print(coin['name'],coin['price']) 
    # data = response.json()
    return render(request, 'home.html', context)

def detail_page(request, pk):
    headers = {
        "X-RapidAPI-Key": "d4e5ce3c5cmsh29e5df404ea0631p153ea1jsnc681364d7c7d",
        "X-RapidAPI-Host": "coinranking1.p.rapidapi.com"
    }

    querystring = {"referenceCurrencyUuid":"yhjMzLPhuIDl","timePeriod":"24h"}

    response = requests.get(f'https://coinranking1.p.rapidapi.com/coin/{pk}', headers=headers, params=querystring)
    data = response.json()

    # print(f'Response status: {response.status_code}')
    # print(f'Response data: {data}')

    if response.status_code != 200 or data.get('status') != 'success':
        raise Http404("Coin not found")

    coin = data['data']['coin']

    saved = SavedCoin.objects.filter(uuid=coin['uuid'], user=request.user).exists()

    context = {
        'uuid': coin['uuid'],
        'symbol': coin['symbol'],
        'name': coin['name'],
        'description': coin['description'],
        'color': coin['color'],
        'iconUrl': coin['iconUrl'],
        'websiteUrl': coin['websiteUrl'],
        '24hVolume': coin['24hVolume'],
        'marketCap': coin['marketCap'],
        'price': coin['price'],
        'btcPrice': coin['btcPrice'],
        'change': coin['change'],
        'rank': coin['rank'],
        'numberOfMarkets': coin['numberOfMarkets'],
        'numberOfExchanges': coin['numberOfExchanges'],
        'coinrankingUrl': coin['coinrankingUrl'],
        'sparkline': coin['sparkline'],
        'links': coin['links'],  # Added this line
        'supply': coin['supply'],  # Added this line
        'allTimeHigh': coin['allTimeHigh'],  # Added this line
        'saved': saved,
    }
    return render(request, 'service/detail_page.html', context)

def detail_full(request, pk):
    headers = {
        "X-RapidAPI-Key": "d4e5ce3c5cmsh29e5df404ea0631p153ea1jsnc681364d7c7d",
        "X-RapidAPI-Host": "coinranking1.p.rapidapi.com"
    }

    querystring = {"referenceCurrencyUuid":"yhjMzLPhuIDl","timePeriod":"24h"}

    response = requests.get(f'https://coinranking1.p.rapidapi.com/coin/{pk}', headers=headers, params=querystring)
    data = response.json()

    # print(f'Response status: {response.status_code}')
    # print(f'Response data: {data}')

    if response.status_code != 200 or data.get('status') != 'success':
        raise Http404("Coin not found")

    coin = data['data']['coin']

    saved = SavedCoin.objects.filter(uuid=coin['uuid'], user=request.user).exists()

    context = {
        'uuid': coin['uuid'],
        'symbol': coin['symbol'],
        'name': coin['name'],
        'description': coin['description'],
        'color': coin['color'],
        'iconUrl': coin['iconUrl'],
        'websiteUrl': coin['websiteUrl'],
        '24hVolume': coin['24hVolume'],
        'marketCap': coin['marketCap'],
        'price': coin['price'],
        'btcPrice': coin['btcPrice'],
        'change': coin['change'],
        'rank': coin['rank'],
        'numberOfMarkets': coin['numberOfMarkets'],
        'numberOfExchanges': coin['numberOfExchanges'],
        'coinrankingUrl': coin['coinrankingUrl'],
        'sparkline': coin['sparkline'],
        'links': coin['links'],  # Added this line
        'supply': coin['supply'],  # Added this line
        'allTimeHigh': coin['allTimeHigh'],  # Added this line
        'saved': saved,
    }
    return render(request, 'service/detail_full.html', context)

def profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile_form = ProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserForm(instance=request.user)
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile_form = ProfileForm(instance=profile)

    bookmakers = SavedCoin.objects.filter(user=request.user)
    
    content = {
        'user_form': user_form,
        'profile_form': profile_form,
        'bookmakers': bookmakers,
    }
    return render(request, 'service/profile.html', content)

def user_login(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
         # Validate and sanitize the input data
        if not username or not password:
            messages.error(request, 'Please provide both username and password.')
            return redirect('user_login')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.success(request, 'Your message was sent successfully!')

    return render(request, 'authentication/user_login.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'logout out!')
    return redirect('user_login')  

def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_login')  # Redirect to the login page after successful registration
    else:
        form = UserRegistrationForm()

    return render(request, 'authentication/user_register.html', {'form': form})

def about(request):
    return render(request, 'about.html')

def save_coin(request, pk):
    if request.method == 'POST':
        form = SavedCoinForm(request.POST)
        if form.is_valid():
            saved_coin = form.save(commit=False)
            saved_coin.user = request.user
            saved_coin.save()
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'error'})
        
def remove_coin(request, pk):
    if request.method == 'POST':
        SavedCoin.objects.filter(uuid=pk, user=request.user).delete()
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'error'})

# def save_coin(request, pk):
#     if request.method == 'POST':
#         form = SavedCoinForm(request.POST)
#         if form.is_valid():
#             saved_coin = form.save(commit=False)
#             saved_coin.user = request.user
#             saved_coin.save()
#             return redirect('detail_page', pk=pk)
#     else:
#         form = SavedCoinForm()
#     return render(request, 'service/save_coin.html', {'form': form})

def test_endpoints(request):
    url = "https://coinranking1.p.rapidapi.com/search-suggestions"

    querystring = {"referenceCurrencyUuid":"yhjMzLPhuIDl"}

    headers = {
        "X-RapidAPI-Key": "c08d086787msh739f2577cb5be6dp1562d2jsne92fba0598e2",
        "X-RapidAPI-Host": "coinranking1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(response.json())
    return render(request, 'test_endpoints.html')
