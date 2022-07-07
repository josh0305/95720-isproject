from django.shortcuts import render, HttpResponse

def home(request):
	return render(request, 'home/index.html')

# Create your views here.
