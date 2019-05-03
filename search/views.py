from django.shortcuts import render, get_object_or_404
from django.utils import timezone
#from .forms import PostForm
from django.shortcuts import redirect
#from .models import Post


# Create your views here.
def search_page(request):
    #posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'search/search_page.html', {})
