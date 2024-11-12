from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup
from .models import Link

# Create your views here.
def scrape(request):

    if request.method == 'POST':
        site = request.POST.get("site","")

        page = requests.get(site)
        soup = BeautifulSoup(page.text,'html.parser')

        for link in soup.find_all('a'):
            link_address = link.get('href')
            link_text = link.string
            Link.objects.create(address=link_address, name=link_text)

        redirect("scrapper/results.html")
    
    data = Link.objects.all()
    context = {'data': data}
    return render(request, "scrapper/results.html",context=context)

def clear(request):
    Link.objects.all().delete()
    return redirect('scrape')
