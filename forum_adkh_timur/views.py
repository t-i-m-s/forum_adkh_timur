from django.shortcuts import render
from users.models import BaseUser, UserInfo
from django.http import HttpResponseNotAllowed


def main_page(request):
    if request.method == 'GET':
        context = {}
        no_ava = '/res/media/avatars/empty_profile.png'  # относительно static
        if request.user.is_authenticated:
            user: BaseUser = request.user
            context.update({'nickname': user.nickname})
            try:
                u_inf: UserInfo = user.user_info
                context.update({'avatar_url': u_inf.avatar.url if u_inf.avatar else no_ava})

            except BaseUser.user_info.RelatedObjectDoesNotExist:
                context['avatar_url'] = no_ava
        return render(request, 'main_page.html', context=context)
    else:
        return HttpResponseNotAllowed(('GET',))
