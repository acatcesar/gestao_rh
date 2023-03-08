from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
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

class FuncionarioNovo(CreateView):
    model = Funcionario
    fields = ['nome', 'departamentos']

    def form_valid(self, form):

        funcionarioObj = form.save(commit=False) # cria o Objeto em memória e não manda pro BD
        username = funcionarioObj.nome.split(' ')[0] + funcionarioObj.nome.split(' ')[1]
        funcionarioObj.empresa = self.request.user.funcionario.empresa
        funcionarioObj.user = User.objects.create(username=username)
        funcionarioObj.save()
        return super(FuncionarioNovo, self).form_valid(form)
