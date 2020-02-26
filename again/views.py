from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

# Create your views here.
def index(request):
    # Uncomment following 2 lines for automatic redirects
    # from index page to dashboard for authorized users (for Kirill)
    # if request.user.is_authenticated:	# TODO: replace with something more beautiful
    #     return HttpResponseRedirect('/finances/dashboard')
    template = loader.get_template('again/index.html')
    return HttpResponse(template.render({}, request))