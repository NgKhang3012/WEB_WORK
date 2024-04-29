from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomPasswordResetForm
from .forms import CustomSetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetDoneView 
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetCompleteView
from DjangoApp.models import *
import openai
from .forms import PostForm  
from django.urls import reverse
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
    success_url='passwordresetcomplete'
    
def index(request):
    top_posts = Post.objects.order_by('-star')[:2]  # Lấy 2 bài đăng có star lớn nhất
    other_posts = Post.objects.exclude(pk__in=[post.pk for post in top_posts])  # Lấy các bài đăng không thuộc top_posts
    if request.method == 'POST':
        if 'button-login' in request.POST:
            email = request.POST.get('input-login-account')
            password = request.POST.get('input-login-password')
            user = authenticate(request, username=email,email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('whilelogin') 
            else:
                return render(request, "index.html", {'error_message_login': 'Invalid email or password'})
        elif 'button-reg' in request.POST:
            email = request.POST.get('input-reg-account')
            password = request.POST.get('input-reg-password')
            confirm_password = request.POST.get('input-reg-repassword')
            if User.objects.filter(username=email).exists():
                return render(request,"index.html",{'error_message_reg_1': 'Your email is exits', 'reg_check': True})
            elif password != confirm_password:
                return render(request, 'index.html', {'error_message_reg': 'Passwords do not match', 'reg_check': True})
            else: 
                user = User.objects.create_user(username=email,email=email, password=password)
                user.save()
                return redirect('whilelogin')
    else:
        return render(request, 'index.html', {'top_posts': top_posts, 'other_posts': other_posts} )

def whilelogin(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            # Tạo URL động cho trang chi tiết của bài viết mới tạo
            post_url = reverse('post', kwargs={'post_id': post.id})  # Đặt tên cho tham số post_id
            # return redirect(post_url)
    return render(request,'index-login.html', {'form': form})

def search(request):
    searched = ""
    keys = []
    if request.method == "POST":
        searched = request.POST["searched"]
        keys = Post.objects.filter(title__contains=searched)
    return render(request, 'search.html', {"searched": searched, "keys": keys})

def ai_suggest(request):
    result=None
    if request.method=="POST":
        question=request.POST.get('question')
        allpost= Post.objects.all()
        trainning=""
        for post in allpost:
            trainning+=f'{post.title}, địa chỉ: {post.address}, đánh giá: {post.star} sao; \n'
        question= f'Bạn tên là FoodieFriend, nhiệm vụ của bạn chỉ là tư vấn về món ăn, không trả lời câu hỏi không liên quan đến món ăn, hãy đọc câu hỏi sau: "{question}". Nếu câu hỏi hợp lệ hãy trả lời ngắn gọn và thật thông minh phù hợp với câu hỏi của người dùng dựa theo các dữ liệu sau(bạn không cần liệt kê hết, chỉ đưa ra những gì phù hợp, và đừng nhầm lẫn giữa quán ăn và quán bán nước): {trainning}. Nếu không hợp lệ thì trả lời là: Tôi là chuyên gia về món ăn, tôi không thể trả lời những câu hỏi liên quan đến món ăn. Bạn không được dùng kí tự đặc biệt trong câu trả lời.'
        API_KEY='sk-proj-voH84xT8yXBZGuMC2LldT3BlbkFJ1bd9xnxCsI7egzwW7Xlf'
        openai.api_key=API_KEY
        response=openai.completions.create(
            model='gpt-3.5-turbo-instruct',
            prompt=question,
            max_tokens=512,
            temperature=1,
        )
        result=response.choices[0].text
    return render(request,'ai_suggest.html',{'result': result})

def post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'index-post.html', {'post': post}) 