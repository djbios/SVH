from django.contrib import admin
from svh.models import *


class VideoSourceAdmin(admin.ModelAdmin):
    def make_published(self, request, queryset):
        queryset.update(published=True)

    make_published.short_description = "Publish videos"
    actions = [make_published]


admin.site.register(VideoSource, VideoSourceAdmin)
admin.site.register(VideoFolder)
