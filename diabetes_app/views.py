from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django import forms
import pickle
import numpy as np
import os

# Load the saved model
model_path = os.path.join(os.path.dirname(__file__), "../diabetes_project/model_rf.pkl")
try:
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
except Exception as e:
    model = None
    print("Error loading model:", e)

# Custom registration form with an optional email field
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=False)  # Email is now optional

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data.get('email')  # Get the email value if provided
        if email:
            user.email = email  # Only save the email if it was provided
        if commit:
            user.save()
        return user

def home_view(request):
    return render(request, 'home.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('predict')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    # Add a message if the user was redirected from the predict page
    next_url = request.GET.get('next', '')
    if next_url == '/predict/':
        return render(request, 'login.html', {'message': 'Please log in to access the Predict Diabetes page.'})
    return render(request, 'login.html')

def register_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def predict_view(request):
    if request.method == "POST":
        features = [float(request.POST.get(key)) for key in [
        "Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
        "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"
    ]]
        prediction = model.predict([features])
        result = "Diabetic" if prediction[0] == 1 else "Non-Diabetic"
        return render(request, 'predict.html', {'result': result})
    return render(request, 'predict.html')


def logout_user(request):
    logout(request)
    return redirect('login')

def send_feedback(request):
    if request.method == 'POST':
        feedback = request.POST.get('feedback')
        if feedback:
            send_mail(
                'Website Feedback',
                feedback,
                'your_email@gmail.com',  # Replace with your email
                ['joshejosh04@gmail.com'],  # Replace with the recipient email
            )
            messages.success(request, 'Thank you for your feedback!')
            return redirect('/')
        else:
            messages.error(request, 'Feedback cannot be empty.')
    return render(request, 'feedback.html')