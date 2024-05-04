from .models import UserInfo
from django.shortcuts import get_object_or_404

def userinfo(request):
    userinfo = None
    if request.user.is_authenticated:
        userinfo = get_object_or_404(UserInfo, id=request.user.id)
    return {'userinfo': userinfo}
