from django.shortcuts import render, redirect
from django.core.paginator import Paginator, InvalidPage
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.contrib.auth.models import User
from index.models import Category, Post, Comments
from myUser.models import Profile as ProfileModel
import datetime

def profile(request):
    categories = Category.objects.all()
    user_profile = request.user
    profile = ProfileModel.objects.get(id_user = request.user.id)

    birth_date = profile.birthday
    today = datetime.date.today()
    years = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    try:
        page_num = request.GET["page"]
    except KeyError:
        page_num = 1
    print(user_profile.id)
    posts = Post.objects.all().filter(id_user = user_profile).order_by('-published_date')
    pag = Paginator(posts, 10)
    try:
        posts_on_page = pag.page(page_num)
    except InvalidPage:
        posts_on_page = pag.page(1)
    return render(request, 'myUser/profile.html', locals())

# def delete_post(request, id_post):
#     post = Post.objects.get(id = id_post)
#     post.delete()
#     username = request.user.username
#     return redirect("/profile/")

def edit_profile(request):
    categories = Category.objects.all()
    user_profile = request.user
    user = User.objects.get(id = request.user.id)
    profile = ProfileModel.objects.get(id_user = request.user.id)

    birth_date = profile.birthday
    today = datetime.date.today()
    years = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        birthday = request.POST.get("birthday")
        gender = request.POST.get("gender")
        email = request.POST.get("email")
        password = request.POST.get("password")
        new_password = request.POST.get('new_password')
        avatar_url = ''
        if request.FILES:
            if request.FILES.get('avatar_url'):
                url = 'static/image/' + request.FILES.get('avatar_url').name
                handle_uploaded_file(request.FILES.get('avatar_url'), url)
                avatar_url = 'image/' + request.FILES.get('avatar_url').name

        url = request.FILES.get('avatar_url')
        print(url)
        if url is not None:
            profile.avatar_url = avatar_url
        profile.birthday = birthday
        profile.gender = gender
        profile.save()

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        if password != '' and new_password != '':
            if user.check_password(password):
                user.set_password(password)
            else:
                args = Cabinet.set_context(request)
                args['edit_error'] = 'Неверный пароль'
                return render(request, 'myUser/edit_profile.html', args)
        user.save()
        login(request, user)
        return redirect('/profile')
    return render(request, 'myUser/edit_profile.html', locals())

def auth(request):
        args = {}
        if request.POST:
            username = request.POST.get('login')
            password = request.POST.get('inputPassword')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/profile/', context={'username': username})
            else:
                args['login_error'] = 'Пользователь не найден'
                return render(request, 'myUser/login.html', args)
        else:
            return render(request, 'myUser/login.html')

def logout_view(request):
        logout(request)
        return redirect('/')

def sign_up(request):
    args = {}
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        birthday = request.POST.get("birthday")
        gender = request.POST.get("gender")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        repeat_password = request.POST.get("repeat_password")
        date_joined = timezone.now()

        if not User.objects.all().filter(username = username):
            if password == repeat_password:
                newUser = User()
                newUser.first_name = first_name
                newUser.last_name = last_name
                newUser.username = username
                newUser.set_password(password)
                newUser.email = email
                newUser.date_joined = date_joined
                newUser.save()

                user = authenticate(username=username, password=password)
                print(newUser.id)
                newProfile = ProfileModel.objects.get(id_user = newUser.id)
                newProfile.birthday = birthday
                newProfile.gender = gender
                newProfile.save()

                login(request, user)
                return redirect('/profile', locals())
            else:
                args['reg_error'] = 'Пароли не совпадают'
                return render(request, 'myUser/registration.html', args)
        else:
            args['reg_error'] = 'Пользователь с таким именем уже существует'
            return render(request, 'myUser/registration.html', args)
    return render(request, 'myUser/registration.html')

def new_post(request):
    categories = Category.objects.all()
    profile = ProfileModel.objects.get(id_user = request.user)
    if request.method == "POST":
        text = request.POST.get('text')
        published_date = timezone.now()
        id_category = request.POST.get('id_category')
        id_user = request.user.id
        image_url = ''
        if request.FILES:
            if request.FILES.get('image_url'):
                url = 'static/image/' + request.FILES.get('image_url').name
                handle_uploaded_file(request.FILES.get('image_url'), url)
                image_url = 'image/' + request.FILES.get('image_url').name
        newPost = Post()
        newPost.text = text
        newPost.published_date = published_date
        newPost.id_category = Category.objects.get(id = id_category)
        newPost.id_user = User.objects.get(id = id_user)
        newPost.image_url = image_url
        newPost.save()
        profile.count_post += 1
        profile.save()
        return redirect("/profile")
    return render(request, 'myUser/profile.html', locals())

def handle_uploaded_file(f, url):
        with open(url, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
# Create your views here.
