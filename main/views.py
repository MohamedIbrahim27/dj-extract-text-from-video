from django.shortcuts import render,redirect
from PIL import Image
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
# Create your views here.
from django.contrib.auth.decorators import login_required
import speech_recognition as sr 
from moviepy.editor import VideoFileClip
from tempfile import NamedTemporaryFile
import os
from django.conf import settings

def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username=None
            email=None
            password=None
            passwordconfigration=None
            username=request.POST['username']
            email=request.POST['email']
            password=request.POST['password']
            passwordconfigration=request.POST['passwordconfigration']
            # user = None
            if User.objects.filter(email=email).exists():
                pass
            else:
                if password != passwordconfigration:
                    pass
                else:
                    user = User.objects.create_user(
                    username=username,
                    is_active=True,
                    email=email,
                    password=password,
                    )
                    user.save()
            # if user is not None:
            #     login(request, user)
                return redirect('/login')
        return render(request,'register.html')
    

def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('/')
        return render(request,'login.html')
from django.http import JsonResponse

@login_required(login_url='/login/')
def extractt(request):
    return render(request,'main.html')

def extract(request):
    text = ''
    if request.method == 'POST':
        if 'vid' in request.FILES:
            vid = request.FILES['vid']
            language = request.POST.get('language')
            with NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
                for chunk in vid.chunks():
                    temp_video.write(chunk)
                temp_video_path = temp_video.name
                
            video_clip = VideoFileClip(temp_video_path)
            audio_path = os.path.join(settings.MEDIA_ROOT, 'extracted_audio.wav')
            video_clip.audio.write_audiofile(audio_path, codec='pcm_s16le')
            r = sr.Recognizer()
            with sr.AudioFile(audio_path) as source:
                data = r.record(source)
                if language == 'chi_sim':
                    text = r.recognize_google(data, language='zh-CN')
                else:
                    text = r.recognize_google(data, language=language)
    return JsonResponse({'text': text})