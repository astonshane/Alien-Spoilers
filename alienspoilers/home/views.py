from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
# Create your views here.

def index(request):
        return render(request,
                'home/index.html',
                {} )
    #return HttpResponse("Hello World. Homepage")
