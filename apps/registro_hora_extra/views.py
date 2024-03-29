import csv
import json

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

from .forms import RegistroHoraExtraForm

from .models import RegistroHoraExtra
from django.views.generic import ListView, UpdateView, DeleteView, CreateView


class HoraExtraList(ListView):
    model = RegistroHoraExtra

    class HoraExtraList(ListView):
        model = RegistroHoraExtra

        def get_queryset(self):
            empresa_logada = self.request.user.funcionario.empresa
            return RegistroHoraExtra.objects.filter(
                funcionario__empresa=empresa_logada)

class HoraExtraEdit(UpdateView):
    model = RegistroHoraExtra
    form_class = RegistroHoraExtraForm

    def get_form_kwargs(self):
        kwargs = super(HoraExtraEdit, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

class HoraExtraEditBase(UpdateView):
    model = RegistroHoraExtra
    form_class = RegistroHoraExtraForm
    #success_url = reverse_lazy('update_hora_extra_base')

    def get_success_url(self):
        return reverse_lazy('update_hora_extra_base', args=[self.object.id]) # se eu quiser permanecer na pagína que estou

    def get_form_kwargs(self):
        kwargs = super(HoraExtraEditBase, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

class HoraExtraDelete(DeleteView):
    model = RegistroHoraExtra
    success_url = reverse_lazy('list_hora_extra')

class HoraExtraNovo(CreateView):
    model = RegistroHoraExtra
    form_class = RegistroHoraExtraForm

    def get_form_kwargs(self):
        kwargs = super(HoraExtraNovo, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
class UtilizouHoraExtra(View):
    def post(self, *args, **kwargs):
        responde = json.dumps({'mensagem': 'Requisicao executada'})
        registro_hora_extra = RegistroHoraExtra.objects.get(id=kwargs['pk'])
        registro_hora_extra.utilizada = True
        registro_hora_extra.save()

        empregado = self.request.user.funcionario

        responde = json.dumps(
            {'mensagem': 'Requisicao executada',
             'horas': float(empregado.total_horas_extra)
             }
        )
        return HttpResponse(responde, content_type='application/json')

class ExportarParaCSV(View):
    def get(selfs, request):
            response = HttpResponse(
                content_type="text/csv",
                headers={"Content-Disposition": 'attachment; filename="somefilename.csv"'},
            )
            registro_he = RegistroHoraExtra.objects.filter(utilizada=False)

            writer = csv.writer(response)
            writer.writerow(['Id', 'Motivo', 'Funcionario', 'Rest. Func', 'Horas'])

            for registro in registro_he:
                writer.writerow(
                [registro.id, registro.motivo, registro.funcionario,
                registro.funcionario.total_horas_extras, registro.horas
                ])

            return response