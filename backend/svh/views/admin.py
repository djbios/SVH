from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
import re

from svh.forms import RenameForm
from svh.models import VideoFile


@staff_member_required
def regex_rename_sources(request):
    ids = request.GET.get('ids') or request.POST.get('ids')
    if not ids:
        return HttpResponseBadRequest()
    vs_list = [get_object_or_404(VideoFile, id=i) for i in ids.split(',')]

    if request.method == 'POST':
        form = RenameForm(request.POST)
        if form.is_valid():
            for vs in vs_list:
                vs._name = _regex(vs.name, form.cleaned_data.get('find'), form.cleaned_data.get('replace'))
                vs.save()
            form = RenameForm({'ids': ids})
    else:
        form = RenameForm(request.GET)

    context = {
        'vs_list': vs_list,
        'form': form
    }
    return render(request, 'svh/rename.html', context)


@staff_member_required
def regex_ajax(request):
    result = _regex(request.GET.get('str'), request.GET.get('find'), request.GET.get('replace'))
    return HttpResponse(result)


def _regex(str, find, replace):
    try:
        return re.sub(find or '', replace or '', str)
    except:
        return ''