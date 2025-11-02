from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
    context = {
        "variable1":"Park Jimin",
        "variable2":"Jeon Jungkook"
        }
    return render(request , 'index.html',context)
def about(request):
    return HttpResponse("This is our django About page")
def service(request):
    return HttpResponse("This is our django Service page")
def contact(request):
    return HttpResponse("This is our django Contact page")            