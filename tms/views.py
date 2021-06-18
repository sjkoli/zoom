from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    #return HttpResponse("Hello World !!!")
    data = ["Hello World !!"]
    return render(request, 'tms/index.html', {'data': data})