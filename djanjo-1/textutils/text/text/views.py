from django.shortcuts import render, HttpResponse

def index(request):
    return render(request,'index.html')

def analyze(request):
    djtext = request.POST.get('text', 'default')
    removepunc=request.POST.get('removepunc','off')
    charcount=request.POST.get('charcount','off')
    charupper=request.POST.get('charupper','off')
    ExtraSpaceRemover_Box=request.POST.get('ExtraSpaceRemover_Box','off')

    if removepunc == "on":
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        analyzed = ""
        for char in djtext:
            if char not in punctuations:
                analyzed = analyzed + char
        params = {'purpose': 'Remove Punctuations', 'analyzed_text': analyzed}
        djtext=analyzed
        
    
    if(charcount == "on"):  
        analyzed = 0
        for char in djtext:
            analyzed = analyzed + 1
        params = {'purpose': 'Count the text', 'analyzed_text': analyzed}
        djtext=analyzed
        
    
    if(charupper == "on"):
        analyzed = ""
        for char in djtext:
            analyzed = analyzed + char.upper()
        params = {'purpose': 'UPPER CASE', 'analyzed_text': analyzed}
        djtext = analyzed
    

    if(ExtraSpaceRemover_Box == 'on'):
        analyzed = ""
        textarea = djtext.strip()          #--------> .strip() method in use

        for index, char in enumerate(textarea):
            if not (textarea[index] == " " and textarea[index+1] == " ") :
                analyzed = analyzed + char
        params = {'purpose':'Extra Space Removering', 'analyzed_text':analyzed}
        djtext=analyzed
        
    return render(request, 'analyze.html', params)
    