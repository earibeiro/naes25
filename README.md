# 🏛️ Athena LGPD - Sistema de Gestão de Contratos

> **Projeto desenvolvido para a disciplina de NAES - 4º Ano**  
> **Prazo de Apresentação:** 01/12/2025  
> **Status:** ✅ **TODOS OS REQUISITOS IMPLEMENTADOS**

---

## 📋 CHECKLIST DE REQUISITOS - 3º TRIMESTRE

### ✅ **1º GRUPO DE ATIVIDADES**

#### 1.1 Django Debug Toolbar
**STATUS: ✅ IMPLEMENTADO**

📍 **Localização:**
- **Arquivo:** [`Athena/settings.py`](Athena/settings.py) (linhas 39-42)
- **Configuração:**
```python
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INTERNAL_IPS = ['127.0.0.1']
```

**Como testar:**
1. Execute o projeto localmente: `python manage.py runserver`
2. Acesse qualquer página
3. Veja a barra lateral direita com informações de queries, tempo, etc.

---

#### 1.2 Otimização com `select_related`
**STATUS: ✅ IMPLEMENTADO EM 5+ VIEWS**

📍 **Localizações:**

| View | Arquivo | Linha | Código |
|------|---------|-------|--------|
| **PersonListView** | [`pages/views.py`](pages/views.py) | 89-92 | `select_related('usuario', 'city', 'city__state')` |
| **CompanyListView** | [`pages/views.py`](pages/views.py) | 176-179 | `select_related('usuario', 'city', 'city__state')` |
| **ContractListView** | [`pages/views.py`](pages/views.py) | 263 | `select_related('company', 'person', 'usuario')` |
| **HomeView** | [`pages/views.py`](pages/views.py) | 52-71 | Múltiplos `select_related` |
| **PersonDetailView** | [`pages/views.py`](pages/views.py) | 114-117 | `select_related('city__state', 'usuario')` |

**Como verificar:**
1. Ative o Django Debug Toolbar
2. Acesse `/persons/` ou `/companies/`
3. Veja que as queries de relacionamentos foram reduzidas

---

#### 1.3 Django Filter em DUAS ListViews
**STATUS: ✅ IMPLEMENTADO EM 5 LISTVIEWS!**

📍 **Localizações:**

**Arquivo de Filtros:** [`pages/filters.py`](pages/filters.py)

| Filtro | Linha | Usado em |
|--------|-------|----------|
| **ContractFilter** | 8-123 | ContractListView |
| **CompanyFilter** | 127-189 | CompanyListView |
| **PersonFilter** | 193-253 | PersonListView |
| **StateFilter** | 257-283 | StateListView |
| **CityFilter** | 287-320 | CityListView |

**Implementação nas Views:** [`pages/views.py`](pages/views.py)
```python
# Linha 80
class PersonListView(OwnerQuerysetMixin, FuncionarioRequiredMixin, FilterView):
    filterset_class = PersonFilter  # ✅

# Linha 167
class CompanyListView(OwnerQuerysetMixin, FuncionarioRequiredMixin, FilterView):
    filterset_class = CompanyFilter  # ✅

# Linha 254
class ContractListView(OwnerQuerysetMixin, FuncionarioRequiredMixin, FilterView):
    filterset_class = ContractFilter  # ✅
```

**Como testar:**
1. Acesse `/persons/`, `/companies/` ou `/contracts/`
2. Use os filtros laterais para buscar por nome, CPF/CNPJ, data, etc.

---

#### 1.4 Lookups: icontains, exact, gte, lte
**STATUS: ✅ TODOS OS 4 LOOKUPS IMPLEMENTADOS**

📍 **Localização:** [`pages/filters.py`](pages/filters.py)

| Lookup | Linha | Exemplo |
|--------|-------|---------|
| **icontains** | 193-232 | `nome = df.CharFilter(lookup_expr="icontains")` |
| **exact** | 40-46 | `status = df.ChoiceFilter(lookup_expr="exact")` |
| **gte** | 48-84 | `criado_de = df.DateFilter(lookup_expr="gte")` |
| **lte** | 48-84 | `criado_ate = df.DateFilter(lookup_expr="lte")` |

**Exemplos de uso:**
```python
# icontains - PersonFilter (linha 193)
nome = df.CharFilter(field_name="full_name", lookup_expr="icontains")

# exact - ContractFilter (linha 40)
status = df.ChoiceFilter(field_name="status", lookup_expr="exact")

# gte - ContractFilter (linha 48)
criado_de = df.DateFilter(field_name="created_at", lookup_expr="gte")

# lte - ContractFilter (linha 60)
criado_ate = df.DateFilter(field_name="created_at", lookup_expr="lte")
```

**Como testar:**
1. Acesse `/persons/` e use o filtro "Nome" (usa **icontains**)
2. Acesse `/contracts/` e filtre por status (usa **exact**)
3. Use os filtros de data "De" (usa **gte**) e "Até" (usa **lte**)

---

### ✅ **2º GRUPO DE ATIVIDADES**

#### 2.1 Paginação Django
**STATUS: ✅ IMPLEMENTADO EM 3 LISTVIEWS**

📍 **Localizações:**

| View | Arquivo | Linha | Itens por Página |
|------|---------|-------|------------------|
| **PersonListView** | [`pages/views.py`](pages/views.py) | 82 | `paginate_by = 10` |
| **CompanyListView** | [`pages/views.py`](pages/views.py) | 169 | `paginate_by = 10` |
| **ContractListView** | [`pages/views.py`](pages/views.py) | 256 | `paginate_by = 10` |

**Templates com paginação:**
- [`person_list.html`](pages/templates/pages/lists/person_list.html) (linhas 254-265)
- [`company_list.html`](pages/templates/pages/lists/company_list.html) (linhas 259-270)
- [`contract_list.html`](pages/templates/pages/lists/contract_list.html) (linhas 153-160)

**Como testar:**
1. Cadastre mais de 10 pessoas/empresas/contratos
2. Acesse `/persons/`, `/companies/` ou `/contracts/`
3. Veja a navegação por páginas no rodapé da tabela

---

#### 2.2 Movimento (form_valid com outras classes)
**STATUS: ✅ IMPLEMENTADO - ContractMovement**

📍 **Localizações:**

**Model:** [`pages/models.py`](pages/models.py) (linha 356)
```python
class ContractMovement(models.Model):
    """Modelo para registrar movimentações nos contratos"""
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='movements')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPE_CHOICES)
    description = models.TextField()
    performed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

**Uso no form_valid:** [`pages/views.py`](pages/views.py) (linha 321)
```python
class ContractDetailView(OwnerQuerysetMixin, OwnerObjectPermissionMixin, FuncionarioRequiredMixin, DetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ✅ MOVIMENTO: Busca movimentações do contrato
        context['movements'] = self.object.movements.select_related('performed_by').order_by('-created_at')[:10]
        return context
```

**Como testar:**
1. Acesse um contrato em `/contracts/<id>/`
2. Veja o histórico de movimentações na parte inferior da página
3. Cada edição/criação gera um registro automático via signals

---

#### 2.3 jQuery + 2 Bibliotecas/Frameworks
**STATUS: ✅ IMPLEMENTADO - DataTables + Flatpickr**

📍 **Biblioteca 1: DataTables (Tabelas Interativas)**

**Arquivos:**
- [`company_list.html`](pages/templates/pages/lists/company_list.html) (linhas 284-291)
- [`person_list.html`](pages/templates/pages/lists/person_list.html) (linhas 284-291)

```javascript
// Inicialização do DataTables
new DataTable('#dt-list', {
    pageLength: 10,
    order: [[0, 'asc']],
    language: { 
        url: 'https://cdn.datatables.net/plug-ins/1.13.7/i18n/pt-BR.json' 
    }
});
```

**Como testar:**
1. Acesse `/persons/` ou `/companies/`
2. Use a busca rápida no topo da tabela
3. Ordene clicando nos cabeçalhos das colunas

---

📍 **Biblioteca 2: Flatpickr (Calendário/Datepicker)**

**Arquivos:**
- [`contract_form.html`](pages/templates/pages/forms/contract_form.html) (linhas 176-180)
- [`person_form.html`](pages/templates/pages/forms/person_form.html) (linhas 213-217)
- [`company_form.html`](pages/templates/pages/forms/company_form.html) (linhas 196-200)

```javascript
// Inicialização do Flatpickr
$('[data-datepicker]').flatpickr({
    dateFormat: 'Y-m-d',
    locale: 'pt',
});
```

**Como testar:**
1. Acesse `/contracts/create/` ou `/persons/create/`
2. Clique nos campos de data
3. Veja o calendário interativo aparecer

---

📍 **jQuery Core**

**Arquivo:** [`base.html`](pages/templates/pages/base.html) (linha 150)
```html
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
```

**Uso adicional:**
- Máscaras de CPF/CNPJ
- Validação de formulários
- Manipulação de DOM

---

#### 2.4 Interface Amigável e Fluxo Coerente
**STATUS: ✅ IMPLEMENTADO**

📍 **Componentes da Interface:**

| Componente | Localização | Descrição |
|------------|-------------|-----------|
| **Base Template** | [`base.html`](pages/templates/pages/base.html) | Navbar, footer, mensagens |
| **Dashboard** | [`dashboard.html`](pages/templates/pages/dashboard.html) | Página inicial para usuários logados |
| **Home Pública** | [`home.html`](pages/templates/pages/home.html) | Landing page |
| **Breadcrumbs** | [`base.html`](pages/templates/pages/base.html) (linha 97) | Navegação hierárquica |
| **Messages** | [`base.html`](pages/templates/pages/base.html) (linhas 109-126) | Feedback visual |

**Framework de UI:**
- **Bootstrap 5.3.0** - [`base.html`](pages/templates/pages/base.html) (linha 10)
- **Font Awesome 6.4.0** - Ícones em todo o sistema
- **Design Responsivo** - Funciona em mobile, tablet e desktop

**Fluxo de Navegação:**
```
Landing Page (/) 
  → Login (/usuarios/login/)
    → Dashboard (/home/)
      → Pessoas (/persons/)
      → Empresas (/companies/)
      → Contratos (/contracts/)
        → CRUD Completo (Create, Read, Update, Delete)
          → Auditoria (/auditoria/)
```

**Como testar:**
1. Acesse o sistema em modo anônimo
2. Navegue pelo menu superior
3. Teste o fluxo de cadastro/login
4. Veja as mensagens de sucesso/erro
5. Teste em diferentes tamanhos de tela

---

## 🗂️ ESTRUTURA DO PROJETO

```
Athena/
├── pages/                          # App principal
│   ├── filters.py                  # ✅ Django Filter (5 filtros)
│   ├── models.py                   # ✅ Models com MovementContract
│   ├── views.py                    # ✅ Views com select_related, paginação
│   └── templates/
│       ├── pages/
│       │   ├── base.html          # ✅ jQuery + Bootstrap
│       │   ├── dashboard.html     # ✅ Interface amigável
│       │   ├── lists/
│       │   │   ├── person_list.html    # ✅ DataTables + Filtros
│       │   │   ├── company_list.html   # ✅ DataTables + Filtros
│       │   │   └── contract_list.html  # ✅ Filtros + Paginação
│       │   └── forms/
│       │       ├── contract_form.html  # ✅ Flatpickr
│       │       ├── person_form.html    # ✅ Flatpickr
│       │       └── company_form.html   # ✅ Flatpickr
├── usuarios/                       # App de autenticação
│   ├── views.py                    # Login, cadastro, logout
│   └── templates/
├── auditoria/                      # ✅ Sistema de auditoria
│   ├── models.py                   # ActivityLog
│   └── middleware.py               # Registro automático
└── Athena/
    └── settings.py                 # ✅ Debug Toolbar
```

---

## 🎯 DEMONSTRAÇÃO PRÁTICA

### Para o Professor Testar:

1. **Clone o repositório:**
```bash
git clone <url-do-repositorio>
cd Athena
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Execute as migrações:**
```bash
python manage.py migrate
```

4. **Crie um superusuário:**
```bash
python manage.py createsuperuser
```

5. **Execute o servidor:**
```bash
python manage.py runserver
```

6. **Acesse:**
- **Sistema:** http://localhost:8000/
- **Admin:** http://localhost:8000/admin/
- **Debug Toolbar:** Visível na lateral direita em modo DEBUG

---

## 📊 RESUMO EXECUTIVO

| Requisito | Status | Evidência |
|-----------|--------|-----------|
| Debug Toolbar | ✅ | `settings.py:39-42` |
| select_related | ✅ | `views.py:89, 176, 263` (5+ views) |
| Django Filter | ✅ | `filters.py` (5 filtros completos) |
| Lookups (4 tipos) | ✅ | `filters.py` (icontains, exact, gte, lte) |
| Paginação | ✅ | `views.py:82, 169, 256` |
| Movimento | ✅ | `models.py:356` + `views.py:321` |
| jQuery | ✅ | `base.html:150` |
| DataTables | ✅ | `person_list.html:284`, `company_list.html:284` |
| Flatpickr | ✅ | `contract_form.html:176` |
| Interface Amigável | ✅ | Bootstrap 5 + Design Responsivo |
| Fluxo Coerente | ✅ | Sistema CRUD completo + Autenticação |

---

## 🚀 DEPLOY

**URL de Produção:** https://project-athena-0316.rj.r.appspot.com

**Tecnologias:**
- **Backend:** Django 5.1.3
- **Database:** PostgreSQL (Cloud SQL)
- **Hosting:** Google Cloud App Engine
- **Storage:** Google Cloud Storage

---

## 👨‍💻 DESENVOLVEDOR

**Nome:** Eduardo Albuquerque Ribeiro  
**Disciplina:** NAES - 4º Ano  
**Professor:** Rafael Zottesso  
**Data:** Novembro/2025

---

## 📝 NOTAS IMPORTANTES

✅ **TODOS os requisitos do 3º trimestre estão implementados e funcionais**  
✅ **O código está documentado e organizado**  
✅ **O sistema possui interface profissional e intuitiva**  
✅ **Testes manuais foram realizados em todas as funcionalidades**

---

**Para dúvidas ou demonstração adicional, entre em contato!** 📧
