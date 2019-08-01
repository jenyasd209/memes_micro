from django.shortcuts import render, redirect
from django.core.paginator import Paginator, InvalidPage
from django.core.exceptions import ObjectDoesNotExist
from index.models import Category, Post, Comments
from django.contrib.auth.models import User
from myUser.models import Profile as ProfileModel
from . import views
from django.db import connection
from collections import namedtuple
from myUser import views
import datetime
from django.utils import timezone

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def index(request):
    categories = Category.objects.all()
    comments = Comments.objects.all()
    try:
        page_num = request.GET["page"]
    except KeyError:
        page_num = 1
    posts = Post.objects.all().order_by('-published_date')
    pag = Paginator(posts, 10)
    try:
        posts_on_page = pag.page(page_num)
    except InvalidPage:
        posts_on_page = pag.page(1)
    return render(request, 'index/index.html', locals())

def old(request):
    categories = Category.objects.all()
    comments = Comments.objects.all()
    try:
        page_num = request.GET["page"]
    except KeyError:
        page_num = 1
    posts = Post.objects.all().order_by('published_date')
    pag = Paginator(posts, 10)
    try:
        posts_on_page = pag.page(page_num)
    except InvalidPage:
        posts_on_page = pag.page(1)
    return render(request, 'index/index.html', locals())

def category(request, category):
    categories = Category.objects.all()
    category = Category.objects.get(name_category = category)
    comments = Comments.objects.all()
    try:
        page_num = request.GET["page"]
    except KeyError:
        page_num = 1
    posts = Post.objects.all().filter(id_category = category.id).order_by('-published_date')
    pag = Paginator(posts, 10)
    try:
        posts_on_page = pag.page(page_num)
    except InvalidPage:
        posts_on_page = pag.page(1)
    return render(request, 'index/categories.html', locals())

def profile_user(request, id_user):
    categories = Category.objects.all()
    user_profile = User.objects.get(id = id_user)
    profile = ProfileModel.objects.get(id_user = id_user)

    birth_date = profile.birthday
    today = datetime.date.today()
    years = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    try:
        page_num = request.GET["page"]
    except KeyError:
        page_num = 1
    print(user_profile.id)
    posts = Post.objects.all().filter(id_user = user_profile)
    pag = Paginator(posts, 10)
    try:
        posts_on_page = pag.page(page_num)
    except InvalidPage:
        posts_on_page = pag.page(1)
    return render(request, 'myUser/profile.html', locals())

def new_comment(request, id_post):
    # categories = Category.objects.all()
    post = Post.objects.get(id = id_post)
    user_profile = User.objects.get(id = post.id_user.id)
    profile = ProfileModel.objects.get(id_user = request.user.id)
    if request.method == "POST":
        text = request.POST.get('text')
        published_date = timezone.now()
        id_user = request.user.id
        # id_post = id_post

        newComment = Comments()
        newComment.text = text
        newComment.published_date = published_date
        newComment.id_user = User.objects.get(id = id_user)
        newComment.id_post = Post.objects.get(id = id_post)
        newComment.save()
        post.count_comment += 1
        post.save()
        profile.count_comment += 1
        profile.save()
        return redirect("/post_id" + str(id_post))
    return render(request, 'myUser/profile.html', locals())

def delete_post(request, id_post):
    post = Post.objects.get(id = id_post)
    user_profile = User.objects.get(id = post.id_user.id)
    profile = ProfileModel.objects.get(id_user = post.id_user)
    profile.count_post -= 1
    profile.save()
    post.delete()
    return redirect("/profile/")

def delete_comment(request, id_comment):
    comment = Comments.objects.get(id = id_comment)
    id_post = comment.id_post.id
    post = Post.objects.get(id = id_post)
    user_profile = User.objects.get(id = comment.id_user.id)
    profile = ProfileModel.objects.get(id_user = comment.id_user)
    profile.count_comment -= 1
    post.count_comment -= 1
    profile.save()
    post.save()
    comment.delete()
    # print(id_post)
    return redirect("/post_id" + str(id_post))

def edit_post(request, id_post):
    post = Post.objects.get(id = id_post)
    categories = Category.objects.all()
    print('redirect')
    if request.method == "POST":
        text = request.POST.get('text')
        id_category = request.POST.get('id_category')
        id_user = request.user.id
        image_url = ''
        if request.FILES:
            if request.FILES.get('image_url'):
                url = 'static/image/' + request.FILES.get('image_url').name
                handle_uploaded_file(request.FILES.get('image_url'), url)
                image_url = 'image/' + request.FILES.get('image_url').name
        # newPost = Post()
        if image_url != '':
            post.image_url = image_url
        post.text = text
        post.id_category = Category.objects.get(id = id_category)
        if not request.user.is_superuser:
            post.id_user = User.objects.get(id = id_user)
        post.save()
        return redirect("/post_id"+str(post.id))
    return render(request, "myUser/edit_post.html", locals())

def post(request, id_post):
    categories = Category.objects.all()
    post = Post.objects.get(id = id_post)
    user_profile = User.objects.get(id = post.id_user.id)
    profile = ProfileModel.objects.get(id_user = post.id_user)

    try:
        page_num = request.GET["page"]
    except KeyError:
        page_num = 1
    comments = Comments.objects.all().filter(id_post = id_post)
    print(comments)
    pag = Paginator(comments, 15)
    try:
        comments_on_page = pag.page(page_num)
    except InvalidPage:
        comments_on_page = pag.page(1)
    return render(request, 'index/post.html', locals())

def search_post(request):
    categories = Category.objects.all()
    req = request.GET.get('search_post')
    print(req)
    try:
        page_num = request.GET["page"]
    except KeyError:
        page_num = 1
    try:
        posts = Post.objects.raw('select * from get_object_fields(%s) ORDER BY published_date;', [req])
    except ObjectDoesNotExist:
        return render(request, 'index/index.html')
    pag = Paginator(posts, 10)
    try:
        posts_on_page = pag.page(page_num)
    except InvalidPage:
        posts_on_page = pag.page(1)
    return render(request, 'index/index.html', locals())


def handle_uploaded_file(f, url):
        with open(url, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

# Create your views here.
