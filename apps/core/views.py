from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.funcionarios.models import Funcionario
from apps.registro_hora_extra.models import RegistroHoraExtra
from django.db.models import Sum


@login_required
def home(request):
    data = {}
    data['usuario'] = request.user
    funcionario = request.user.funcionario
    data['total_funcionarios'] = funcionario.empresa.total_funcionarios
    data['total_funcionarios_ferias'] = funcionario.empresa.total_funcionarios_ferias
    data['total_funcionarios_doc_pendente'] = funcionario.empresa.total_funcionarios_doc_pendente
    data['total_funcionarios_rg'] = 10
    data['total_hora_extra_utilizadas'] = RegistroHoraExtra.objects.filter(
        funcionario__empresa=funcionario.empresa, utilizada=True).aggregate(Sum('horas'))['horas__sum'] or 0
    data['total_hora_extra_pendente'] = RegistroHoraExtra.objects.filter(
        funcionario__empresa=funcionario.empresa, utilizada=False).aggregate(Sum('horas'))['horas__sum'] or 0
    return render(request, 'core/index.html', data)
