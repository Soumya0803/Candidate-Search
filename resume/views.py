from django.shortcuts import render
# from django.http import HttpResponse
from .finder.CandidateSearch import SearchCandidate
from .models import Resume

# Create your views here.

def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    # paginate Resume
    query = SearchCandidate("java", "sql")
    res = Resume.objects.raw(query)
    context = { "meow": "meow" }
    return render(request, 'resume/index.html', context)