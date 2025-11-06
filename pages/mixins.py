from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.shortcuts import redirect
from django.http import Http404


class OwnerQuerysetMixin(LoginRequiredMixin):
    """
    Limita o queryset ao owner do objeto.
    Se o usuário for superuser OU pertencer ao grupo 'empresa_admin',
    deixa ver tudo (ou então aplique um filtro por empresa, se existir).
    """
    owner_field_name = "usuario"  # Padrão do projeto Athena

    def is_admin(self):
        """Verifica se o usuário é admin ou superuser"""
        u = self.request.user
        return u.is_superuser or u.groups.filter(name="empresa_admin").exists()

    def get_queryset(self):
        """Aplica filtro de escopo por usuário"""
        qs = super().get_queryset()
        
        # Admin vê tudo
        if self.is_admin():
            return qs
        
        # Usuário comum vê apenas seus registros
        filter_kwargs = {self.owner_field_name: self.request.user}
        return qs.filter(**filter_kwargs)


class OwnerObjectPermissionMixin(UserPassesTestMixin):
    """
    Garante que o objeto pertence ao usuário (ou que ele é admin).
    Use em Detail/Update/DeleteView.
    """
    owner_field_name = "usuario"  # Padrão do projeto Athena

    def is_admin(self):
        """Verifica se o usuário é admin ou superuser"""
        u = self.request.user
        return u.is_superuser or u.groups.filter(name="empresa_admin").exists()

    def test_func(self):
        """Testa se o usuário pode acessar o objeto"""
        try:
            obj = self.get_object()
            
            # Admin pode tudo
            if self.is_admin():
                return True
            
            # Verifica se o objeto pertence ao usuário
            owner = getattr(obj, self.owner_field_name, None)
            return owner == self.request.user
            
        except Exception:
            return False

    def handle_no_permission(self):
        """Customiza tratamento de acesso negado"""
        messages.error(
            self.request, 
            "❌ Você não tem permissão para acessar este registro."
        )
        # Redireciona para a lista do modelo
        model_name = self.model._meta.model_name
        try:
            return redirect(f'{model_name}-list')
        except:
            return redirect('home')

    def get_object(self, queryset=None):
        """
        Sobrescreve get_object para garantir escopo por usuário
        """
        if queryset is None:
            queryset = self.get_queryset()
        
        # Busca o objeto pelo pk
        pk = self.kwargs.get(self.pk_url_kwarg)
        if pk is not None:
            # Admin pode acessar qualquer objeto
            if self.is_admin():
                queryset = self.model.objects.all()
            else:
                # Usuário comum apenas seus objetos
                filter_kwargs = {
                    'pk': pk,
                    self.owner_field_name: self.request.user
                }
                queryset = queryset.filter(**filter_kwargs)
        
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(f"Nenhum {self.model._meta.verbose_name} encontrado.")
        
        return obj


class OwnerCreateMixin:
    """Mixin para definir o proprietário do objeto na criação"""
    
    def form_valid(self, form):
        """✅ GARANTIR QUE USUARIO SEJA SEMPRE PREENCHIDO"""
        # Verificar se o model tem campo 'usuario' e se não está preenchido
        if hasattr(form.instance, 'usuario'):
            if not form.instance.usuario_id:  # Verifica se usuario_id não está definido
                form.instance.usuario = self.request.user
        
        return super().form_valid(form)


class GroupRequiredMixin(UserPassesTestMixin):
    """
    Mixin que exige pertencer a um grupo específico
    Compatível com django-braces mas implementado nativamente
    """
    group_required = None  # String ou lista de grupos
    
    def test_func(self):
        """Verifica se o usuário pertence ao grupo obrigatório"""
        if not self.group_required:
            return True  # Se não especificou grupo, permite acesso
            
        user = self.request.user
        
        # Superuser sempre pode acessar
        if user.is_superuser:
            return True
        
        # Empresa admin sempre pode acessar (grupo master)
        if user.groups.filter(name="empresa_admin").exists():
            return True
        
        # Verificar grupo específico
        if isinstance(self.group_required, str):
            # Grupo único
            return user.groups.filter(name=self.group_required).exists()
        elif isinstance(self.group_required, (list, tuple)):
            # Lista de grupos - usuário deve estar em pelo menos um
            for group_name in self.group_required:
                if user.groups.filter(name=group_name).exists():
                    return True
            return False
        
        return False
    
    def handle_no_permission(self):
        """Customiza tratamento de grupo não autorizado"""
        if not self.request.user.is_authenticated:
            # Usuário não logado - redireciona para login
            messages.warning(
                self.request, 
                "⚠️ Você precisa fazer login para acessar esta página."
            )
            return redirect('login')
        
        # Usuário logado mas sem permissão
        group_display = self.group_required
        if isinstance(self.group_required, (list, tuple)):
            group_display = ', '.join(self.group_required)
        
        messages.error(
            self.request, 
            f"❌ Acesso restrito ao(s) grupo(s): '{group_display}'. "
            f"Contate o administrador para solicitar permissões."
        )
        return redirect('home')


class FuncionarioRequiredMixin(GroupRequiredMixin):
    """Mixin específico para funcionários - atalho comum"""
    group_required = 'funcionario'


class AdminRequiredMixin(GroupRequiredMixin):
    """Mixin específico para admins - atalho comum"""
    group_required = 'empresa_admin'


class StaffRequiredMixin(GroupRequiredMixin):
    """Mixin para staff (funcionario OU admin) - grupos múltiplos"""
    group_required = ['funcionario', 'empresa_admin']


class AdminOnlyMixin(UserPassesTestMixin):
    """Apenas superuser ou empresa_admin - versão legacy"""
    
    def test_func(self):
        u = self.request.user
        return u.is_superuser or u.groups.filter(name="empresa_admin").exists()
    
    def handle_no_permission(self):
        messages.error(self.request, "❌ Acesso restrito a administradores.")
        return redirect('home')
# Deploy: 2025-11-06 00:04:16
