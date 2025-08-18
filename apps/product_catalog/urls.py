from django.urls import path, include

app_name = 'product_catalog'
urlpatterns = [
    path('v1/', include(('apps.product_catalog.apis.v1.urls', 'v1'), namespace='v1')),  # Assign 'v1' namespace
]
