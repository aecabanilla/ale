from django.urls import path
from importaciones.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path(r'', IndexView.as_view()),
    path('decidir_card/', DecidirCardView.as_view(), name='decidir_card'),
    path('decidir_card/<int:pk>/', DecidirCardDetailView.as_view(), name='decidir_card_detail'),
    path('decidir_pmc/', DecidirPMCView.as_view(), name='decidir_pmc'),
    path('decidir_pmc/<int:pk>/', DecidirPMCDetailView.as_view(), name='decidir_pmc_detail'),
    path('gire/', GireView.as_view(), name='gire'),
    path('sir/', SIRView.as_view(), name='sir'),
    path('sir/<int:pk>/', SirDetailView.as_view(), name='sir_detail'),
    path('upload_raw_decidir_card/', DecidirCardUploadView.as_view(), name='upload_raw_decidir_card'),
    path('upload_raw_decidir_pmc/', DecidirPMCUploadView.as_view(), name='upload_raw_decidir_pmc'),
    path('upload_raw_gire/', GireUploadView.as_view(), name='upload_raw_gire'),
    path('upload_raw_sir/', SIRUploadView.as_view(), name='upload_raw_sir'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('conciliaciones/', ConciliacionesView.as_view(), name='conciliaciones'),
    path('conciliaciones/<int:pk>/', ConciliacionesDetailView.as_view(), name='conciliaciones_detail'),
    path('results/', ResultsView.as_view(), name='results'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
