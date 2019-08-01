from django.shortcuts import render, HttpResponse, redirect
from django.core.paginator import Paginator, InvalidPage
from django.core.exceptions import ObjectDoesNotExist
from index.models import Category, Post, Comments
from django.contrib.auth.models import User
from myUser.models import Profile as ProfileModel
from django.db import connection
from collections import namedtuple
from myUser import views
import datetime
from django.utils import timezone
import xlwt
import datetime
import pytz
import mimetypes, os
import gzip
import delegator

def export(request):
    if request.user.is_superuser:
        # Создаем книку
        book = xlwt.Workbook('utf8')

        # Создаем шрифт
        font = xlwt.easyxf('font: height 240,name Arial, bold on,\
            italic off; align: wrap on, vert top, horiz center;')

        # Добавляем лист
        sheet = book.add_sheet('Post')
        sheet.write(0,0,'id',font)
        sheet.write(0,1,'published_date',font)
        sheet.write(0,2,'text',font)
        sheet.write(0,3,'image_url',font)
        sheet.write(0,4,'user',font)
        sheet.write(0,5,'category',font)

        font = xlwt.easyxf('font: height 240,name Arial, bold off,\
            italic off; align: wrap on, vert top, horiz center;')

        posts = Post.objects.all()
        i = 1
        j = 0

        for post in posts:
            sheet.write(i,j,post.id,font)
            published_date = post.published_date.strftime("%B %d, %Y")
            sheet.write(i,j+1,published_date,font)
            sheet.write(i,j+2,post.text,font)
            sheet.write(i,j+3,post.image_url,font)
            user = post.id_user.username
            sheet.write(i,j+4,user,font)
            category = str(post.id_category.id) + " (" + post.id_category.name_category + ")"
            sheet.write(i,j+5,category,font)
            i +=1

        # Ширина колонки
        sheet.col(1).width = 5000
        sheet.col(2).width = 10000
        sheet.col(3).width = 15000
        sheet.col(4).width = 5000
        sheet.col(5).width = 5000

        # Лист в положении "альбом"
        sheet.portrait = False

        sheet.set_print_scaling(85)
        book.save('posts.xls')
        res = save_file(request, 'posts.xls')
        os.remove('posts.xls')
        return res
    else:
        redirect('/')

def backup(request):
    if request.user.is_superuser:
        with connection.cursor() as cursor:
            cursor.execute('select current_user;')
            current_user = cursor.fetchone()
            cursor.execute('SELECT current_database();')
            current_db = cursor.fetchone()
            command = ("pg_dump postgresql://%s:qwerty123@127.0.0.1:5432/%s > dump.dump" % (current_user[0], current_db[0]))
            print(command)
        with gzip.open('backup.gz', 'wb') as f:
            c = delegator.run(command)
            f.write(c.out.encode('utf-8'))
            return save_file(request, 'dump.dump')
    else:
        redirect('/')
def save_file(request, file_name):

    fp = open(file_name, "rb");
    response = HttpResponse(fp.read());
    fp.close();
    file_type = mimetypes.guess_type(file_name);
    if file_type is None:
        file_type = 'application/octet-stream';
    response['Content-Type'] = file_type
    response['Content-Length'] = str(os.stat(file_name).st_size);
    response['Content-Disposition'] = "attachment; filename=" + file_name;
    return response;

def users(request):
    if request.user.is_superuser:
        users = User.objects.all().order_by('id')
        try:
            page_num = request.GET["page"]
        except KeyError:
            page_num = 1
        pag = Paginator(users, 10)
        try:
            users_on_page = pag.page(page_num)
        except InvalidPage:
            users_on_page = pag.page(1)
    else:
        redirect('/')
    return render(request, "myAdmin/users.html", locals())

def delete_user(request, id_user):
    if request.user.is_superuser:
        with connection.cursor() as cursor:
            cursor.execute('delete from "myUser_profile" where id_user_id = %s; delete from "auth_user" where auth_user.id = %s;', (id_user, id_user))
    else:
        redirect('/')
    return redirect("/admins/users")

def categories(request):
    if request.user.is_superuser:
        categories = Category.objects.raw('SELECT * FROM "index_category"')
        try:
            page_num = request.GET["page"]
        except KeyError:
            page_num = 1
        pag = Paginator(categories, 10)
        try:
            categories_on_page = pag.page(page_num)
        except InvalidPage:
            categories_on_page = pag.page(1)
    else:
        redirect('/')
    return render(request, "myAdmin/categories.html", locals())

def search_user(request):
    req = request.GET.get('search_user')
    print(req)
    try:
        page_num = request.GET["page"]
    except KeyError:
        page_num = 1
    try:
        users = User.objects.raw('select * from get_user_fields(%s);', [req])
        # users = User.objects.filter(username__icontains=req).order_by('-id')
    except ObjectDoesNotExist:
        return render(request, 'myAdmin/users.html')
    pag = Paginator(users, 10)
    try:
        users_on_page = pag.page(page_num)
    except InvalidPage:
        users_on_page = pag.page(1)
    return render(request, 'myAdmin/users.html', locals())

def add_category(request):
    if request.user.is_superuser:
        if request.method == "POST":
            name_category = request.POST.get('name_category')
            with connection.cursor() as cursor:
                cursor.execute('INSERT INTO "index_category" (name_category) VALUES (%s);', [name_category])
    else:
        redirect('/')
    return redirect("/admins/categories")

def delete_category(request, id_category):
    if request.user.is_superuser:
        with connection.cursor() as cursor:
            cursor.execute('delete from "index_category" where id = %s;', [id_category])
    else:
        redirect('/')
    return redirect("/admins/categories")
# Create your views here.
