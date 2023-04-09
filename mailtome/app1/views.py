import socket
import time
import pickle
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import NewUserForm, InputForm
from email_validator import validate_email, EmailNotValidError


def send(msg, client, request):
    print(f"[i] Msg Len : {len(b'msg')}")
    BUFFER_SIZE = 2048
    i = 1
    print("[i] APPROX SIZE : ", len(msg), " B")
    try:
        total_sent = 0
        while total_sent < len(msg):
            chunk = msg[total_sent:total_sent + BUFFER_SIZE]
            client.send(chunk)
            i += 1
            total_sent += len(chunk)
        print(f"[+] Total SENT pack : {i}")
        messages.success(request, "Send successful.")
        client.close()
    except ConnectionResetError:
        print('[-] ConnectionResetError')
        messages.error(request, "failed to send : ")
    print(f"Sent : {total_sent} B")


@login_required(login_url='login')
def land(request):
    context = {}
    if request.method == 'POST':
        form = InputForm(request.POST, request.FILES)
        if form.is_valid():
            subject = form.cleaned_data['sub']
            message = form.cleaned_data['mssg']
            file = request.FILES.get('file')
            if file:
                file_name = file.name
                file_data = file.read()
                if file:
                    # Check file size
                    if file.size > 20 * 1024 * 1024:  # 20 MB limit
                        messages.error(request, "File size cannot exceed 20 MB. Please upload again.")
                        return redirect('land')
                file_name = file.name
                file_data = file.read()
            else:
                file_name = None
                file_data = None
            send_list = [subject, message, file_name, file_data]
            intialize_socket(request, send_list)
        else:
            context['form'] = InputForm()
    context['form'] = InputForm()
    return render(request, 'index.html', context)


@login_required(login_url='login')
def intialize_socket(request, send_list):
    PORT = 5090
    SERVER = "192.168.1.5"
    ADDR = (SERVER, PORT)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    not_connect = True
    retry_count = 0
    while not_connect and retry_count != 5:
        try:
            client.connect(ADDR)
            not_connect = False
        except BrokenPipeError as e:
            time.sleep(2)
            print(f"[-] Server Connection Error\n[-] Retry : {retry_count}")
            retry_count += 1
            print(e)
    if not_connect:
        return False, None
    list = []
    to = request.user.email
    subject = send_list[0]
    msg = send_list[1]
    file = request.FILES.get('file')
    if file:
        file_name = file.name
        file_data = file.read()
    else:
        file_name = None
        file_data = None
    print(f"[i] To : {to} \n[i] Attchment : {file_name}")
    list.append(subject)  # 0
    list.append(msg)  # 1
    list.append(to)  # 2
    list.append(file_name)  # 3
    list.append(file_data)  # 4
    data = pickle.dumps(list)
    send(data, client, request)


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        mail = validate_email(form.email)
        if not mail:
            messages.error(request, "Invali Email Enter Again")
        if form.is_valid() and mail:
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect(land)
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Welcome {username}.")
                return redirect(land)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect(land)


def intro(request):
    return render(request=request, template_name="intro.html")

    