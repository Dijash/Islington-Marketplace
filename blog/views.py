import base64
import mimetypes
from pathlib import Path

from django.conf import settings
from django.shortcuts import render, get_object_or_404

from .models import Blog


def blog_list(request):
    topic_filter = request.GET.get('topic', '').strip()

    blogs = Blog.objects.filter(is_active=True)

    if topic_filter:
        blogs = blogs.filter(topic__iexact=topic_filter)

    blogs = blogs.order_by('order', '-created_at')

    for blog in blogs:
        blog.inline_image = None
        if not blog.image:
            continue

        image_path = Path(settings.MEDIA_ROOT) / blog.image.name
        if not image_path.exists():
            continue

        mime_type, _ = mimetypes.guess_type(str(image_path))
        if not mime_type:
            mime_type = 'image/jpeg'

        try:
            encoded = base64.b64encode(image_path.read_bytes()).decode('ascii')
        except OSError:
            continue

        blog.inline_image = f"data:{mime_type};base64,{encoded}"

    topics = (
        Blog.objects.filter(is_active=True)
        .values_list('topic', flat=True)
        .distinct()
    )

    return render(request, 'blog/blog_list.html', {
        'blogs': blogs,
        'topics': topics,
        'selected_topic': topic_filter,
    })


def blog_detail(request, id):
    blog = get_object_or_404(Blog, id=id, is_active=True)
    return render(request, 'blog/blog_detail.html', {'blog': blog})
