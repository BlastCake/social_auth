from django.shortcuts import redirect


def redirect_auth(request):
    return redirect('authorize_url', permanent=True)