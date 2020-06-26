from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from svh.models import *
from mptt.admin import DraggableMPTTAdmin

from svh.rabbit.messages import send_message, VideoConvertTaskMessage


class VideoFileAdmin(admin.ModelAdmin):
    ordering = ['id']
    search_fields = ['name']

    def make_published(self, request, queryset):
        queryset.update(published=True)
    make_published.short_description = "Publish videos"

    def convert_in_default_format(self, request, queryset):
        for vs in queryset:
            start_conversion(fileId=vs.videofile_set.objects.filter(format='source').first().fileId, format='h264x480p')

    convert_in_default_format.short_description = "Convert selected videos in default format"

    def regex_rename(self, request, queryset):
        ids = queryset.values_list('id', flat=True)
        return HttpResponseRedirect(reverse('rename')+'?ids='+','.join(str(x) for x in ids))
    regex_rename.short_description = "Batch regex rename"

    actions = [make_published, convert_in_default_format, regex_rename]


admin.site.register(VideoFile, VideoFileAdmin)
admin.site.register(VideoFolder, DraggableMPTTAdmin)
admin.site.register(Gif)
admin.site.register(Preview)
