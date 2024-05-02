from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomPasswordResetForm
from .forms import CustomSetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetDoneView 
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetCompleteView
from DjangoApp.models import *
from openai import OpenAI
import os
from .forms import PostForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
        
class CustomPasswordResetView(PasswordResetView):
    template_name = 'Forget_password.html'
    success_url='done'
    form_class = CustomPasswordResetForm
    html_email_template_name='custom_password_reset_email.html'
    
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name= 'Password_Reset_Done.html'    
    
class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name= 'Password_Reset_Complete.html'    

class CustomPasswordConfirmView(PasswordResetConfirmView):
    template_name= 'Password_Reset_Confirm.html' 
    form_class= CustomSetPasswordForm   
    success_url='done'
    
def index(request):
    if request.user.is_authenticated:
        return redirect('/usr/{}/'.format(request.user.id))
    top_posts = Post.objects.order_by('-star')[:2]  # Lấy 2 bài đăng có star lớn nhất
    other_posts = Post.objects.exclude(pk__in=[post.pk for post in top_posts])  # Lấy các bài đăng không thuộc top_posts
    if request.method == 'POST':
        if 'button-login' in request.POST:
            email = request.POST.get('input-login-account')
            password = request.POST.get('input-login-password')
            user = authenticate(request, username=email,email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/usr/{}/'.format(request.user.id))
            else:
                return render(request, "index.html", {'error_message_login': 'Invalid email or password','top_posts': top_posts, 'other_posts': other_posts})
        elif 'button-reg' in request.POST:
            email = request.POST.get('input-reg-account')
            password = request.POST.get('input-reg-password')
            try:
                validate_password(password)
            except ValidationError as e:
                return render(request,"index.html",{'error_message_reg_2': 'Your password is invalid', 'reg_check': True,'top_posts': top_posts, 'other_posts': other_posts})
            confirm_password = request.POST.get('input-reg-repassword')
            if User.objects.filter(username=email).exists():
                return render(request,"index.html",{'error_message_reg_1': 'Your email is exits', 'reg_check': True,'top_posts': top_posts, 'other_posts': other_posts})
            elif password != confirm_password:
                return render(request, 'index.html', {'error_message_reg': 'Passwords do not match', 'reg_check': True,'top_posts': top_posts, 'other_posts': other_posts})
            else: 
                user = User.objects.create_user(username=email,email=email, password=password)
                user.save()
                login(request,user)
                newuserinfo=UserInfo(id=request.user.id)
                newuserinfo.avatar='avatar_test.jpg'
                newuserinfo.save()
                return redirect('/usr/{}/'.format(request.user.id))
    else:
        return render(request, 'index.html', {'top_posts': top_posts, 'other_posts': other_posts} )
@login_required
def logoutPage(request):
    logout(request)
    return redirect('index')

@login_required
def whilelogin(request, user_id):
    if request.user.id==user_id:
        userinfo=get_object_or_404(UserInfo,id=user_id)
        top_posts = Post.objects.order_by('-star')[:2]  # Lấy 2 bài đăng có star lớn nhất
        other_posts = Post.objects.exclude(pk__in=[post.pk for post in top_posts])  # Lấy các bài đăng không thuộc top_posts
        form = PostForm()
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save()
                return redirect('/post/{}/'.format(post.id))
        return render(request,'index_login.html', {'form': form,'top_posts': top_posts, 'other_posts': other_posts, 'userinfo': userinfo})
    else:
        if request.user.is_authenticated:
            return redirect('/usr/{}/'.format(request.user.id))
        else:
            return redirect('index')

def search(request):
    searched = ""
    keys = []
    user = request.user if request.user.is_authenticated else None
    if request.method == "POST":
        searched = request.POST.get("searched", "")
        keys = Post.objects.filter(title__contains=searched)
    return render(request, 'search.html', {"searched": searched, "keys": keys, "user": user})
def ai_suggest(request):
    result=''
    if request.method=="POST":
        question=request.POST.get('question')
        allpost= Post.objects.all()
        trainning=""
        for post in allpost:
            trainning+=f'{post.title}, địa chỉ: {post.address}, đánh giá: {post.star} sao; \n'
        question= f'Bạn tên là FoodieFriend, nhiệm vụ của bạn chỉ là tư vấn về món ăn, không trả lời câu hỏi không liên quan đến món ăn và không trả lời những câu hỏi mà bạn không rõ yêu cầu, hãy đọc câu hỏi sau: "{question}". Nếu câu hỏi hợp lệ hãy trả lời ngắn gọn và thật thông minh phù hợp với câu hỏi của người dùng dựa theo các dữ liệu sau(bạn không cần liệt kê hết, chỉ đưa ra những gì phù hợp, và đừng nhầm lẫn giữa quán ăn và quán bán nước): {trainning}. Nếu không hợp lệ thì trả lời là: Tôi là chuyên gia về món ăn, tôi không thể trả lời những câu hỏi liên quan đến món ăn. Bạn không được dùng kí tự đặc biệt trong câu trả lời.'
        api_key = os.environ.get('OPENAI_API_KEY')
        client = OpenAI(api_key=api_key)
        stream = client.chat.completions.create(
            model='gpt-3.5-turbo-0125',
            messages=[
                {
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                ],
                }
            ],
            stream=True,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                result += chunk.choices[0].delta.content
    return render(request, 'ai_suggest.html', {'result': result})
@login_required
def editprofile(request, user_id):
    if request.user.id==user_id: 
        userinfo = get_object_or_404(UserInfo,id=user_id)
        if request.method=="POST":
            if 'savebtn' in request.POST:
                userinfo.firstname=request.POST.get('firstname')
                userinfo.lastname=request.POST.get('lastname')
                userinfo.phonenumber=request.POST.get('phonenumber')
                userinfo.gender=request.POST.get('gender')
                userinfo.avatar=request.FILES.get('inputavatar')
                userinfo.introduction=request.POST.get('introduction')
                userinfo.save()
                return render(request, 'profile.html',{'user':userinfo})
            if 'cancelbtn' in request.POST:
                return redirect('/usr/{}/'.format(request.user.id))
        return render(request, 'profile.html',{'user':userinfo})
    else:
        if request.user.is_authenticated:
            return redirect('/usr/{}/'.format(request.user.id))
        else:
            return redirect('index')

def post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    userinfo = post.idUser
    return render(request, 'index_post.html', {'post': post, 'userinfo': userinfo})
