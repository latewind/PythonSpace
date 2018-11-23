from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from common.decorators import ajax_request
from .forms import ImageCreateForm
from django.shortcuts import get_object_or_404
from .models import Image
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from actions.utils import create_action
import redis
from django.conf import settings

r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


# Create your views here.


@login_required
def image_create(request):
    if request.method == 'POST':
        image_form = ImageCreateForm(request.POST)
        if image_form.is_valid():
            cd = image_form.cleaned_data
            new_item = image_form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            create_action(request.user, 'bookmarked image', new_item)
            messages.success(request, 'Success')
            return redirect(new_item.get_absolute_url())
    else:
        image_form = ImageCreateForm(request.GET)
    return render(request, 'images/image/create.html', {'section': 'images',
                                                        'form': image_form})


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    total_views = r.incr('image:{}:views'.format(image.id))
    r.zincrby('image_ranking', image.id, 1)
    return render(request, 'images/image/detail.html', {'image': image,
                                                        'total_views': total_views})


def image_ranking(request):
    image_ranking_ids = r.zrange('image_ranking', 0, -1, desc=True)[:10]
    image_ids = [int(_) for _ in image_ranking_ids]
    most_viewed = list(Image.objects.filter(id__in=image_ids))
    most_viewed.sort(key=lambda x: image_ids.index(x.id))
    return render(request, 'images/image/ranking.html', {'most_viewed': most_viewed})


@ajax_request
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('like')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.user_like.add(request.user)
                create_action(request.user, 'likes', image)
            else:
                image.user_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ko'})


@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 2)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        images = paginator.page(2)
    except EmptyPage:
        if request.is_ajax():
            # If the request is AJAX and the page is out of range return an empty page
            return HttpResponse('')
        # If page is out of range deliver last page of results
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,
                      'images/image/list_ajax.html',
                      {'section': 'images', 'images': images})
    return render(request,
                  'images/image/list.html',
                  {'section': 'images', 'images': images})
