from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import ActivityLog


class ActivityLogListView(LoginRequiredMixin, ListView):
    """
    View para listar logs de atividade do usuário atual
    """
    model = ActivityLog
    template_name = 'auditoria/activity_log_list.html'
    context_object_name = 'logs'
    paginate_by = 50
    
    def get_queryset(self):
        """Filtra logs do usuário atual ou relacionados a seus objetos"""
        user = self.request.user
        
        # Admin vê tudo
        if user.is_superuser or user.groups.filter(name='empresa_admin').exists():
            queryset = ActivityLog.objects.all()
        else:
            # Usuário comum vê apenas seus logs
            queryset = ActivityLog.objects.filter(
                Q(actor=user) |  # Ações que ele fez
                Q(object_repr__icontains=f'usuario={user.id}')  # Objetos dele
            )
        
        # Filtros opcionais via GET
        action = self.request.GET.get('action')
        if action:
            queryset = queryset.filter(action=action)
        
        date_from = self.request.GET.get('date_from')
        if date_from:
            queryset = queryset.filter(created_at__date__gte=date_from)
        
        date_to = self.request.GET.get('date_to')
        if date_to:
            queryset = queryset.filter(created_at__date__lte=date_to)
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estatísticas para o contexto
        user = self.request.user
        context['total_logs'] = self.get_queryset().count()
        context['user_actions'] = self.get_queryset().filter(actor=user).count()
        context['actions_choices'] = ActivityLog.ACTIONS
        
        return context

# Create your views here.
