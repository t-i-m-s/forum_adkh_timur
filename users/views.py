import os

from django.shortcuts import render
from .models import BaseUser, UserInfo
from django.http import HttpResponse, HttpResponseServerError, JsonResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.contrib.auth import logout, login, authenticate
from forum_adkh_timur.settings import MAIN_PAGE_URL
from django.contrib.staticfiles import finders
from django.core.mail import send_mail


def register_user(request):

    if request.method == 'GET':
        return render(request, 'users/register_page.html')

    elif request.method == 'POST':
        if request.POST['psw'] != request.POST['psw_repeat']:
            return render(request, 'users/register_page.html', context={
                'error_message': 'passwords not match'
            })
        user = BaseUser.objects.create_user(request.POST['nickname'],
                                            request.POST['email'],
                                            request.POST['psw_repeat'])
        UserInfo.objects.create(user=user)
        user.save()
        login(request, user)
        # send_mail(
        #     'Hi message!',
        #     f"Hi, {request.POST['nickname']}",
        #     None,
        #     [request.POST['email']],
        #     fail_silently=False,
        # )
        return HttpResponseRedirect(MAIN_PAGE_URL)


def log_in(request):

    if request.method == 'GET':
        return render(request, 'users/login_page.html')

    elif request.method == 'POST':
        if not request.POST['email'] or not request.POST['psw']:
            return render(request, 'users/register_page.html', context={
                'error_message': 'incorrect email or password'
            })
        user = authenticate(email=request.POST['email'],
                            password=request.POST['psw'])
        login(request, user)
        return HttpResponseRedirect(MAIN_PAGE_URL)


def log_out(request):
    logout(request)
    return HttpResponseRedirect(MAIN_PAGE_URL)


def profile(request, nickname):
    if request.method == 'GET':
        no_dt = 'Unknown'
        no_ava = '/res/media/avatars/empty_profile.png'  # относительно static
        try:
            if nickname == 'me':
                user: BaseUser = request.user
            else:
                user: BaseUser = BaseUser.objects.get(nickname=nickname)

            context = {'nickname': user.nickname, 'email': user.email}

            try:
                u_inf: UserInfo = user.user_info
                context.update({
                    'avatar_url': u_inf.avatar.url if u_inf.avatar else no_ava,
                    'age': u_inf.age if u_inf.age else no_dt,
                    'country': u_inf.country if u_inf.country else no_dt,
                    'job': u_inf.job if u_inf.job else no_dt,
                    'about_user': u_inf.about_user if u_inf.about_user else no_dt,
                })
                return render(request, 'users/profile_page.html',
                              context=context)

            except BaseUser.user_info.RelatedObjectDoesNotExist:
                context.update({
                    'avatar_url': no_ava,
                    'age': no_dt,
                    'country': no_dt,
                    'job': no_dt,
                    'about_user': no_dt,
                })
                return render(request, 'users/profile_page.html',
                              context=context)

        except BaseUser.objects.model.DoesNotExist:
            return render(request, 'main_page.html',
                          context={
                              'error_message': 'user does not exist'
                          })
    elif request.method == 'POST':
        u_inf: UserInfo = request.user.user_info
        data = request.POST
        new_avatar = request.FILES.get('avatar')
        if new_avatar is not None:
            prev_avatar = u_inf.avatar
            if prev_avatar:
                prev_avatar_path = prev_avatar.path
                os.remove(prev_avatar_path)
            u_inf.avatar = new_avatar
        u_inf.age = data['age']
        u_inf.job = data['job']
        u_inf.country = data['country']
        u_inf.about_user = data['about_user']
        u_inf.save()
        return HttpResponseRedirect(request.path)
    else:
        return HttpResponseNotAllowed(('GET', 'POST'))
