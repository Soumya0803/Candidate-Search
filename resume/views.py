from django.shortcuts import render
# from django.http import HttpResponse
from .finder.CandidateSearch import SearchCandidate
from .models import Resume
from django.core.paginator import Paginator

# Create your views here.

def index(request):
    search = request.GET.get('search', False)
    option = request.GET.get('radio', 'sql')
    context = {}
    if search:
        query = SearchCandidate(search, option)
        res_list = Resume.objects.raw(query)
        paginator = Paginator(res_list, 25) # Show 25 contacts per page.
        page_number = request.GET.get('page',0)
        page_obj = paginator.get_page(page_number)
        context = { 'page_obj': page_obj , 'query': query }
    return render(request, 'resume/index.html', context)