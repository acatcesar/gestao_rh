from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView
from .models import Funcionario


class FuncionariosList(ListView):
    model = Funcionario

    def get_queryset(self):
         empressa_logada = self.request.user.funcionario.empresa
         return Funcionario.objects.filter(empresa=empressa_logada)

class FuncionarioEdit(UpdateView):
    model = Funcionario
    fields = ['nome', 'departamentos']

class FuncionarioDelete(DeleteView):
    model = Funcionario
    success_url = reverse_lazy('list_funcionarios')
