# 🏛️ Athena — Sistema de Gestão LGPD

**Athena** é uma plataforma completa para gestão de contratos, autorizações e conformidade com a Lei Geral de Proteção de Dados (LGPD). Permite que empresas e funcionários gerenciem dados pessoais, contratos e documentações de forma segura e transparente.

## 🚀 **Stack Tecnológica**

- **Backend:** Python 3.11+ / Django 4.2+
- **Banco de Dados:** SQLite (desenvolvimento) / PostgreSQL (produção)
- **Frontend:** Django Templates + Bootstrap 5.2
- **Autenticação:** Django Auth + Grupos customizados
- **Deploy:** Docker ready
- **Logs:** Sistema de auditoria integrado

## ✅ **Funcionalidades Principais**

### 🔐 **Sistema de Autenticação**
- Login/Logout seguro (logout via POST)
- Cadastro de usuários (Pessoa Física/Jurídica)
- Controle de acesso por grupos (empresa_admin/funcionario)
- Alteração de senha integrada

### 👥 **Gestão de Dados**
- **Pessoas Físicas:** Cadastro completo com CPF, endereço, finalidade LGPD
- **Pessoas Jurídicas:** Registro de empresas com CNPJ e dados corporativos
- **Contratos:** Gestão completa de relacionamentos contratuais
- **Localização:** Estados e cidades para endereçamento

### 📊 **Dashboard e Relatórios**
- KPIs em tempo real (pessoas, empresas, contratos)
- Registros recentes e estatísticas
- Logs de auditoria para compliance
- Escopo por usuário (dados privados)

### 🛡️ **Conformidade LGPD**
- Documentação obrigatória de finalidade do tratamento
- Controle de consentimentos
- Auditoria de acesso aos dados
- Relatórios de compliance

## 🏗️ **Arquitetura do Sistema**

```
Athena/
├── 📁 Athena/              # Configurações do projeto
│   ├── settings.py         # Configurações Django
│   ├── urls.py            # URLs principais
│   └── wsgi.py            # WSGI para deploy
├── 📁 pages/              # App principal (CRUD)
│   ├── models.py          # Person, Company, Contract, State, City
│   ├── views.py           # Views com mixins de segurança
│   ├── forms.py           # Formulários customizados
│   ├── mixins.py          # Mixins de autorização
│   └── templates/         # Templates Bootstrap
├── 📁 usuarios/           # App de autenticação
│   ├── views.py           # Cadastro, login, grupos
│   ├── forms.py           # Formulários de usuário
│   └── templates/         # Templates de auth
├── 📁 auditoria/          # App de logs
│   ├── models.py          # ActivityLog
│   ├── views.py           # Visualização de logs
│   └── templates/         # Templates de auditoria
└── 📄 requirements.txt    # Dependências Python
```

## ⚙️ **Setup e Instalação**

### 1️⃣ **Clone o Repositório**
```bash
git clone https://github.com/seu-usuario/athena-lgpd.git
cd athena-lgpd
```

### 2️⃣ **Ambiente Virtual**
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/macOS  
python -m venv .venv
source .venv/bin/activate
```

### 3️⃣ **Instalar Dependências**
```bash
pip install -r requirements.txt
```

### 4️⃣ **Configurar Banco de Dados**
```bash
# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# (Opcional) Dados de demonstração
python manage.py seed_demo
```

### 5️⃣ **Executar Servidor**
```bash
python manage.py runserver
```

Acesse: **http://127.0.0.1:8000/**

## 🗺️ **Rotas Principais**

### 🏠 **Páginas Públicas**
| Rota | Descrição | Acesso |
|------|-----------|---------|
| `/` | Página inicial | 🌐 Público |
| `/sobre/` | Sobre o sistema | 🌐 Público |
| `/about/` | Redirect para `/sobre/` | 🌐 Público |

### 🔐 **Autenticação**
| Rota | Descrição | Acesso |
|------|-----------|---------|
| `/accounts/login/` | Login de usuários | 🌐 Público |
| `/accounts/logout/` | Logout (POST) | 🔒 Autenticado |
| `/usuarios/cadastro/` | Escolha tipo de cadastro | 🌐 Público |
| `/usuarios/cadastro/admin/` | Cadastro empresa admin | 🌐 Público |
| `/usuarios/cadastro/funcionario/` | Cadastro funcionário | 🌐 Público |
| `/usuarios/change-password/` | Alterar senha | 🔒 Autenticado |

### 📊 **Dashboard**
| Rota | Descrição | Acesso |
|------|-----------|---------|
| `/home/` | Dashboard principal | 🔒 Autenticado |
| `/auditoria/logs/` | Logs de atividade | 👥 Funcionário+ |

### 👥 **Gestão de Pessoas**
| Rota | Descrição | Acesso |
|------|-----------|---------|
| `/pessoas/` | Lista de pessoas | 👥 Funcionário+ |
| `/pessoas/criar/` | Cadastrar pessoa | 👥 Funcionário+ |
| `/pessoas/<id>/` | Detalhes da pessoa | 👥 Owner/Admin |
| `/pessoas/<id>/editar/` | Editar pessoa | 👥 Owner/Admin |
| `/pessoas/<id>/excluir/` | Excluir pessoa | 👥 Owner/Admin |

### 🏢 **Gestão de Empresas**
| Rota | Descrição | Acesso |
|------|-----------|---------|
| `/empresas/` | Lista de empresas | 👥 Funcionário+ |
| `/empresas/criar/` | Cadastrar empresa | 👥 Funcionário+ |
| `/empresas/<id>/` | Detalhes da empresa | 👥 Owner/Admin |
| `/empresas/<id>/editar/` | Editar empresa | 👥 Owner/Admin |
| `/empresas/<id>/excluir/` | Excluir empresa | 👥 Owner/Admin |

### 📋 **Gestão de Contratos**
| Rota | Descrição | Acesso |
|------|-----------|---------|
| `/contratos/` | Lista de contratos | 👥 Funcionário+ |
| `/contratos/criar/` | Cadastrar contrato | 👥 Funcionário+ |
| `/contratos/<id>/` | Detalhes do contrato | 👥 Owner/Admin |
| `/contratos/<id>/editar/` | Editar contrato | 👥 Owner/Admin |
| `/contratos/<id>/excluir/` | Excluir contrato | 👥 Owner/Admin |
| `/rascunho/contrato/` | Criar rascunho | 🌐 Público |
| `/rascunho/revisar/` | Revisar rascunho | 🌐 Público |
| `/rascunho/finalizar/` | Finalizar rascunho | 👥 Funcionário+ |

### 🌍 **Localização (Admin)**
| Rota | Descrição | Acesso |
|------|-----------|---------|
| `/estados/` | Lista de estados | 👑 Admin |
| `/estados/criar/` | Cadastrar estado | 👑 Admin |
| `/cidades/` | Lista de cidades | 👑 Admin |
| `/cidades/criar/` | Cadastrar cidade | 👑 Admin |

## 👥 **Grupos de Usuários**

### 👑 **empresa_admin**
- Acesso total ao sistema
- Pode gerenciar estados e cidades
- Vê todos os dados (sem escopo por usuário)
- Pode acessar logs de auditoria

### 👥 **funcionario**
- Acesso às funcionalidades principais
- Escopo limitado aos próprios dados
- Pode gerenciar pessoas, empresas e contratos
- Acesso limitado aos logs

### 🔒 **Usuário Comum**
- Acesso apenas aos próprios dados
- Funcionalidades básicas de visualização
- Dashboard personalizado

## 🔧 **Comandos de Gestão**

```bash
# Criar dados de demonstração
python manage.py seed_demo

# Verificar URLs quebradas
python manage.py check_urls

# Corrigir URLs automaticamente
python manage.py fix_urls --backup

# Verificar integridade do sistema
python manage.py check

# Limpar sessões expiradas
python manage.py clearsessions
```

## 🐳 **Deploy com Docker**

```bash
# Build da imagem
docker build -t athena-lgpd .

# Executar container
docker run -p 8000:8000 athena-lgpd

# Com docker-compose
docker-compose up -d
```

## 📚 **Dependências Principais**

```txt
Django>=4.2.0
django-crispy-forms>=2.0
django-crispy-bootstrap5>=0.7
Pillow>=10.0.0
python-decouple>=3.8
whitenoise>=6.5.0
gunicorn>=21.2.0
psycopg2-binary>=2.9.7  # Para PostgreSQL
```

## 🧪 **Testes**

```bash
# Executar todos os testes
python manage.py test

# Testes específicos
python manage.py test pages
python manage.py test usuarios
python manage.py test auditoria

# Coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## 📋 **Checklist de Desenvolvimento**

Ver [CHECKLIST.md](CHECKLIST.md) para status detalhado das entregas.

## 🛡️ **Segurança**

- ✅ Autenticação obrigatória para dados sensíveis
- ✅ Escopo por usuário (owner) implementado
- ✅ Grupos de permissão configurados
- ✅ Logs de auditoria para compliance
- ✅ Validação de dados em formulários
- ✅ CSRF protection habilitado
- ✅ Logout seguro via POST

## 🐛 **Problemas Conhecidos**

- [ ] Implementar rate limiting para APIs
- [ ] Adicionar testes automatizados
- [ ] Melhorar responsividade mobile
- [ ] Implementar notificações em tempo real

## 🤝 **Contribuição**

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 **Licença**

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 **Autores**

- **Equipe Athena** - Projeto NAES 2025
- **Universidade** - 4º Ano de Ciência da Computação

## 📞 **Contato**

- 📧 Email: athena@universidade.edu
- 🌐 Website: https://athena-lgpd.com
- 📱 Suporte: +55 (11) 99999-9999

---

**Athena LGPD** - Gestão inteligente de dados pessoais 🏛️✨
