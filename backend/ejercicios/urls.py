from rest_framework.routers import DefaultRouter
from .views import LeccionViewSet, PreguntaViewSet

router = DefaultRouter()
router.register(r'lecciones', LeccionViewSet, basename='leccion')
router.register(r'preguntas', PreguntaViewSet, basename='pregunta')

urlpatterns = router.urls
