from django.urls import path
from .views import HoraExtraList, HoraExtraEdit,HoraExtraEditBase, HoraExtraDelete, HoraExtraNovo, UtilizouHoraExtra, ExportarParaCSV



urlpatterns = [
     path('', HoraExtraList.as_view(), name='list_hora_extra'),
     path('novo/', HoraExtraNovo.as_view(), name='create_registro_hora_extra'),
     path('editar/<int:pk>/', HoraExtraEdit.as_view(), name='update_hora_extra_base'),
     path('editar-funcionario/<int:pk>/', HoraExtraEditBase.as_view(), name='update_hora_extra'),
     path('utilizou-hora-extra/<int:pk>/',
          UtilizouHoraExtra.as_view(), name='utilizou_hora_extra'),
     path('delete/<int:pk>/', HoraExtraDelete.as_view(), name='delete_hora_extra'),
     path('exportar-csv', ExportarParaCSV.as_view(), name='exportar_csv'),

]