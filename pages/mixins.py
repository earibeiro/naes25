from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.shortcuts import redirect


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


class OwnerCreateMixin(LoginRequiredMixin):
    """
    Mixin para CreateView que automaticamente define o owner
    """
    owner_field_name = "usuario"
    
    def form_valid(self, form):
        """Define o usuário atual como owner do objeto"""
        # Define o owner antes de salvar
        if hasattr(form.instance, self.owner_field_name):
            setattr(form.instance, self.owner_field_name, self.request.user)
        
        return super().form_valid(form)


class AdminOnlyMixin(UserPassesTestMixin):
    """
    Mixin que permite acesso apenas para admins
    """
    
    def test_func(self):
        """Permite acesso apenas para admins"""
        u = self.request.user
        return u.is_superuser or u.groups.filter(name="empresa_admin").exists()
    
    def handle_no_permission(self):
        """Customiza tratamento de acesso negado para admins"""
        messages.error(
            self.request, 
            "❌ Acesso restrito a administradores."
        )
        return redirect('home')


class GroupRequiredMixin(UserPassesTestMixin):
    """
    Mixin que exige pertencer a um grupo específico
    """
    group_required = None
    
    def test_func(self):
        """Verifica se o usuário pertence ao grupo"""
        if not self.group_required:
            return True
            
        u = self.request.user
        return (
            u.is_superuser or 
            u.groups.filter(name=self.group_required).exists() or
            u.groups.filter(name="empresa_admin").exists()
        )
    
    def handle_no_permission(self):
        """Customiza tratamento de grupo não autorizado"""
        messages.error(
            self.request, 
            f"❌ Acesso restrito ao grupo '{self.group_required}'."
        )
        return redirect('home')