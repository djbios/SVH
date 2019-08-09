from django.contrib import admin
from svh.models import *
from svh.tasks import convert_videosource_task


class VideoSourceAdmin(admin.ModelAdmin):
    ordering = ['path']
    search_fields = ['path', '_name']

    def make_published(self, request, queryset):
        queryset.update(published=True)

    make_published.short_description = "Publish videos"

    def convert_in_default_format(self, request, queryset):
        for vs_id in queryset.values_list('id', flat=True):
            convert_videosource_task.apply_async(args=[vs_id, 'default'])

    convert_in_default_format.short_description = "Convert selected videos in default format"

    actions = [make_published, convert_in_default_format]


admin.site.register(VideoSource, VideoSourceAdmin)
admin.site.register(VideoFolder)
