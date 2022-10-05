from multiprocessing import context
from django.views import View # <- View class to handle 
from django.http import HttpResponse # <- a class to 
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
from .models import Artists, Song, Playlist
# at top of file with other imports
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
# Auth
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator




# Create your views here.

# Here we will be creating a class called Home and extending it from the View class
class Home(TemplateView):
    template_name = "home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["playlists"] = Playlist.objects.all()
        return context

class About(TemplateView):
    template_name = "about.html"
    
 #adds artist class for mock database dat
# @method_decorator(login_required, name='dispatch')
class ArtistList(TemplateView):
    template_name = "artist_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name")
        if name != None:
            context["header"] = f"Searching for {name}"
            context["artists"] = Artists.objects.filter(user=self.request.user)
            # We add a header context that includes the search param
        else:
            context["artists"] = Artists.objects.all()
            # default header for not searching 
            context["header"] = "Trending Artists"
        return context


class ArtistCreate(CreateView):
    model = Artists
    fields = ['name', 'img', 'bio']
    template_name = "artist_create.html"

    # This is our new method that will add the user into our submitted form
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ArtistCreate, self).form_valid(form)

    def get_success_url(self):
        print(self.kwargs)
        return reverse('artist_detail', kwargs={'pk': self.object.pk})
    
    
class ArtistDetail(DetailView):
    model = Artists
    template_name = "artist_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["playlists"] = Playlist.objects.all()
        return context
    
class ArtistUpdate(UpdateView):
    model = Artists
    fields = ['name', 'img', 'bio', 'verified_artist']
    template_name = "artist_update.html"

    def get_success_url(self):
        return reverse('artist_detail', kwargs={'pk': self.object.pk})
    
    
class ArtistDelete(DeleteView):
    model = Artists
    template_name = "artist_delete_confirmation.html"
    success_url = "/artists/"


class SongCreate(View):

    def post(self, request, pk):
        title = request.POST.get("title")
        minutes = request.POST.get("minutes")
        seconds = request.POST.get("minutes")
        length = 60 * int(minutes) + int(seconds)
        artist = Artists.objects.get(pk=pk)
        Song.objects.create(title=title, length=length, artist=artist)
        return redirect('artist_detail', pk=pk)
    

class PlaylistSongAssoc(View):
    def get(self, request, pk, song_pk):
        assoc = request.GET.get("assoc")
        if assoc == "remove":
            Playlist.objects.get(pk=pk).song.remove(song_pk)
        if assoc == "add":
            Playlist.objects.get(pk=pk).song.add(song_pk)
        return redirect('home') 
            
            
            
class Signup(View):
    # show a form to fill out
    def get(self, request):
        form = UserCreationForm()
        context = {"form": form}
        return render(request, "registration/signup.html", context)
    # on form submit, validate the form and login the user.
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("artist_list")
        else:
            context = {"form": form}
            return render(request, "registration/signup.html", context)