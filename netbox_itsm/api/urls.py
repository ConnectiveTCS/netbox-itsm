from netbox.api.routers import NetBoxRouter

from . import views

app_name = 'netbox_itsm'

router = NetBoxRouter()
router.register('services', views.ServiceViewSet)
router.register('service-dependencies', views.ServiceDependencyViewSet)
router.register('service-assets', views.ServiceAssetViewSet)

urlpatterns = router.urls
