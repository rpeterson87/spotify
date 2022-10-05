from django.contrib import admin
from .models import Artists, Playlist
from .models import Song

admin.site.register(Artists) # this line will add the model to the admin panel
admin.site.register(Song) # this line will add the model to the admin panel
admin.site.register(Playlist) # this line will add the model to the admin panel
