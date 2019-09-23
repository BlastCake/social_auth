from django.shortcuts import render, redirect, reverse
from django.views.generic import View
import requests


class SocialAuth(View):

    def get(self, request):
        """
            Проверяет наличие access_token в сессии, если он есть значит пользователь уже авторизован
            и редиректит на (user_detail_url) страницу пользователя. Если его нет, то
            авторизует пользователя и получает 'code', в дальнейшем необходимый для получения access_token.

        """

        if 'token' in request.session:
            return redirect(reverse('user_detail_url'))

        return render(request, 'main/index.html')


class UserPage(View):

    def get(self, request):
        """
            Проверяет наличие access_token в сессии, если его нет, то делает запрос на получение, с помощью переменной
            'code', переданной в эту вьюху. Записывает access_token и user_id в сессию.
            Если access_token присутствует в сессии, то рендерит шаблон и передает в контексте данные о пользователе
            и его друзьях.

        """

        if 'token' not in request.session:
            # TODO Подставить client_id и client_secret из своего приложения VK
            # TODO Проверить (если необходимо) на каком порту запущено прилжение

            url = 'https://oauth.vk.com/access_token?client_id=*****&client_secret=*****' \
                  '&redirect_uri=http://127.0.0.1:8000/social/user_detail/&code={}'.format(request.GET['code'])
            response_data = requests.get(url).json()

            token = response_data['access_token']
            user_id = response_data['user_id']
            request.session['token'] = token
            request.session['user_id'] = user_id
            request.session['code'] = request.GET['code']

        user_data = requests.get(f'https://api.vk.com/method/users.get?userd_id={request.session["user_id"]}'
                                 f'&fields=photo_400&access_token={request.session["token"]}&v=5.101').json()[
            'response'][0]

        friends_data = requests.get(f'https://api.vk.com/method/friends.get?user_ids={request.session["user_id"]}'
                                    f'&fields=photo_100&access_token={request.session["token"]}&v=5.101').json()[
            'response']['items']

        context = {

            'user': user_data,
            'friends': friends_data[:5]
        }

        return render(request, 'main/user_detail.html', context=context)


def log_out(request):
    del request.session['token']
    del request.session['user_id']
    del request.session['code']

    return redirect(reverse('authorize_url'))
