from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.funcionarios.models import Funcionario
from apps.registro_hora_extra.models import RegistroHoraExtra
from django.db.models import Sum
import requests


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




import requests
from django.http import JsonResponse

def get_github_user_info(request, username):
    username = 'acatcesar'
    url = f'https://api.github.com/users/{username}'
    response = requests.get(url)


    if response.status_code == 200:
        data = response.json()
        return JsonResponse({'Nome completo': data['name']})
    else:
        return JsonResponse({'mensagem': 'Usuário não encontrado'}, status=404)


# def get_cotacao(request):
#     token = 'hq5CAHPZYezxFJYXRwPyHE'
#     url = f'https://brapi.dev/api/quote/PETR4%2C%5EBVSP?range=1d&interval=1d&fundamental=true&dividends=true'
#     response = requests.get(url)
#
#     if response.status_code == 200:
#         data = response.json()
#         print(data)
#         return JsonResponse( data)
#     else:
#         return JsonResponse({'mensagem': 'Usuário não encontrado'}, status=404)

def get_cotacao(request):
    token = 'hq5CAHPZYezxFJYXRwPyHE'
    url = f'https://brapi.dev/api/quote/PETR4?token={token}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return JsonResponse(data)
    else:
        return JsonResponse({'mensagem': 'Ação não encontrata'}, status=404)
