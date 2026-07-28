from django.urls import include, path

from utilities.urls import get_model_urls

from . import views  # noqa: F401  (imported to populate the model view registry)

app_name = 'netbox_itsm'
urlpatterns = [
    path('services/', include(get_model_urls('netbox_itsm', 'service', detail=False))),
    path('services/<int:pk>/', include(get_model_urls('netbox_itsm', 'service'))),

    path('service-dependencies/', include(get_model_urls('netbox_itsm', 'servicedependency', detail=False))),
    path('service-dependencies/<int:pk>/', include(get_model_urls('netbox_itsm', 'servicedependency'))),

    path('service-assets/', include(get_model_urls('netbox_itsm', 'serviceasset', detail=False))),
    path('service-assets/<int:pk>/', include(get_model_urls('netbox_itsm', 'serviceasset'))),

    path('portfolios/', include(get_model_urls('netbox_itsm', 'serviceportfolio', detail=False))),
    path('portfolios/<int:pk>/', include(get_model_urls('netbox_itsm', 'serviceportfolio'))),

    path('portfolio-members/', include(get_model_urls('netbox_itsm', 'serviceportfoliomember', detail=False))),
    path('portfolio-members/<int:pk>/', include(get_model_urls('netbox_itsm', 'serviceportfoliomember'))),

    path('business-capabilities/', include(get_model_urls('netbox_itsm', 'businesscapability', detail=False))),
    path('business-capabilities/<int:pk>/', include(get_model_urls('netbox_itsm', 'businesscapability'))),
]
