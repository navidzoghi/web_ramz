from django.urls import path, include

app_name = 'review'
urlpatterns = [
    path('v1/', include(('apps.review.apis.v1.urls', 'v1'), namespace='v1')),  # Assign 'v1' namespace
    #
]
