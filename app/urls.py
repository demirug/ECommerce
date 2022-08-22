from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from apps.helper.views import FeedbackFAQView
from apps.textpage.views import TextPageDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),


    path("page/<slug:slug>/", TextPageDetailView.as_view(), name="textpage"),
    path("helper/", FeedbackFAQView.as_view(), name="helper"),

    path('', include(('apps.orders.urls', 'orders'))),
    path('', include(('apps.products.urls', 'products'))),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
