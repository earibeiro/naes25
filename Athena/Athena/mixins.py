from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Contract, ContractMovement
from .forms import ContractForm


class OwnerQuerysetMixin(LoginRequiredMixin):
    """
    Limita o queryset ao owner do objeto.
    Se o usuário for superuser OU pertencer ao grupo 'empresa_admin',
    deixa ver tudo (ou então aplique um filtro por empresa, se existir).
    """
    owner_field_name = "usuario"  # Padrão do projeto Athena (era "owner")

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


class ContractCreateView(LoginRequiredMixin, OwnerCreateMixin, CreateView):
    """CreateView para contratos"""
    model = Contract
    form_class = ContractForm
    template_name = 'pages/forms/contract_form.html'
    success_url = reverse_lazy('contract-list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        contract = form.save(commit=False)
        contract.usuario = self.request.user
        contract.save()
        form.save_m2m()
        
        # ✅ REGISTRAR MOVIMENTO
        ContractMovement.objects.create(
            contract=contract,
            movement_type='created',
            description=f'Contrato criado por {self.request.user.username}',
            performed_by=self.request.user
        )
        
        # ✅ ATUALIZAR CONTADOR NA EMPRESA
        if contract.company:
            contract.company.total_contracts = contract.company.contracts.filter(is_active=True).count()
            contract.company.save(update_fields=['total_contracts'])
        
        messages.success(self.request, f'✅ Contrato "{contract.title}" criado com sucesso!')
        return redirect(self.get_success_url())
    
    def form_invalid(self, form):
        messages.error(self.request, '❌ Erro ao criar contrato. Verifique os dados.')
        return super().form_invalid(form)


class ContractUpdateView(OwnerQuerysetMixin, OwnerObjectPermissionMixin, FuncionarioRequiredMixin, UpdateView):
    """UpdateView para contratos"""
    model = Contract
    form_class = ContractForm
    template_name = 'pages/forms/contract_form.html'
    success_url = reverse_lazy('contract-list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        contract = form.save(commit=False)
        contract.save()
        form.save_m2m()
        
        # ✅ REGISTRAR MOVIMENTO
        ContractMovement.objects.create(
            contract=contract,
            movement_type='updated',
            description=f'Contrato atualizado por {self.request.user.username}',
            performed_by=self.request.user
        )
        
        # ✅ ATUALIZAR CONTADOR NA EMPRESA
        if contract.company:
            contract.company.total_contracts = contract.company.contracts.filter(is_active=True).count()
            contract.company.save(update_fields=['total_contracts'])
        
        messages.success(self.request, f'✅ Contrato "{contract.title}" atualizado com sucesso!')
        return redirect(self.get_success_url())


class ContractDeleteView(OwnerQuerysetMixin, OwnerObjectPermissionMixin, FuncionarioRequiredMixin, DeleteView):
    """DeleteView para contratos"""
    model = Contract
    template_name = 'pages/confirm/contract_confirm_delete.html'
    success_url = reverse_lazy('contract-list')
    
    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        
        # ✅ REGISTRAR MOVIMENTO ANTES DE DELETAR
        ContractMovement.objects.create(
            contract=obj,
            movement_type='deleted',
            description=f'Contrato excluído por {request.user.username}',
            performed_by=request.user
        )
        
        # ✅ ATUALIZAR CONTADOR NA EMPRESA
        company = obj.company
        
        messages.success(request, f'✅ Contrato "{obj.title}" excluído com sucesso!')
        response = super().delete(request, *args, **kwargs)
        
        # Atualizar depois da exclusão
        if company:
            company.total_contracts = company.contracts.filter(is_active=True).count()
            company.save(update_fields=['total_contracts'])
        
        return response