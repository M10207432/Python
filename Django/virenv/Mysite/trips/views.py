from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def hello_world(request):
    #return HttpResponse("Hello")
	return render(request, 'hello_world.html',
				{'current_time':123})
