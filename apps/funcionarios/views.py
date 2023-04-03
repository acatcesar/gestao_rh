import io

from django import template
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from reportlab.pdfgen import canvas

from django.template.loader import get_template
import xhtml2pdf.pisa as pisa


from .models import Funcionario
from .. import funcionarios


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

def relatorio_funcionarios(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'  #Content-Disposition ele baixa o arquivo

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    p.drawString(200, 810, 'Relatório de funcionário')

    funcionarios = Funcionario.objects.filter(
        empresa=request.user.funcionario.empresa)

    str_ = 'Nome: %s | Hora Extra %.2f '

    p.drawString(0, 800, '_' * 150)

    y = 750
    for funcionario in funcionarios:
        p.drawString(10, y, str_ % (funcionario.nome, funcionario.total_horas_extras))
        y -= 20

    p.showPage()
    p.save()


    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response

class Render:
    @staticmethod
    def render(path: str, params: dict, filename: str):
        template = get_template(path)
        html = template.render(params)
        response = io.BytesIO()
        pdf = pisa.pisaDocument(
            io.BytesIO(html.encode("UTF-8")), response)
        if not pdf.err:
            response = HttpResponse(
                response.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment;filename=%s.pdf' % filename
            return response
        else:
            return HttpResponse("Error Rendering PDF", status=400)

class Pdf(View):

    def get(self, request):
        params = {
            'today': 'Variavel today',
            'sales': 'Variavel sales',
            'request': request,
        }
        return Render.render('funcionarios/relatorio.html', params, 'myfile')