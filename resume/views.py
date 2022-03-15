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
        paginator = Paginator(res_list, 6) # Show 6 resumes per page.
        page_number = request.GET.get('page',1)
        page_obj = paginator.get_page(page_number)
        context = { 'page_obj': page_obj , 'query': query, 'search': search, 'option': option}
    return render(request, 'resume/index.html', context)