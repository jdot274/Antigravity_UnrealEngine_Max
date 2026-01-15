# Prisma - Guia de Onboarding

Sistema de desenvolvimento orientado a especificações para features complexas.

---

## 🚀 Quick Start (5 minutos)

### Passo 1: Verificar Setup ✅

**Estrutura Necessária:**

```bash
# Verificar estrutura
ls -la .prisma/

# Esperado:
.prisma/
├── agentes/                    # Agentes especializados
├── checkpoints/                # Checkpoints de execução
├── comandos/                   # Comandos slash disponíveis
├── configuracoes/              # Arquivos de configuração
├── melhorias/                  # Melhorias propostas
├── projeto/                    # ⭐ DOCUMENTAÇÃO CENTRALIZADA
│   ├── arquitetura/
│   ├── especificacoes/        # ⭐ Especificações de features (NOVO CAMINHO)
│   ├── decisoes/              # ADRs
│   ├── padroes/
│   └── ...
├── prompts/                    # System prompts principais
├── relatorios/                 # Relatórios de execução
├── templates/                  # Templates de documentos
└── workflows/                  # Workflows do sistema

# MUDANÇA IMPORTANTE: Especificações movidas para .prisma/projeto/especificacoes/
.prisma/
├── agentes/           # Agentes especializados
├── comandos/          # Comandos slash disponíveis
├── configuracoes/     # Arquivos de configuração
├── prompts/           # System prompts principais
├── templates/         # Templates de documentos
└── onboarding.md      # Este arquivo
```

**Checklist:**

- [ ] Pasta `.prisma/` existe
- [ ] Arquivo `.claude/CLAUDE.md` menciona Prisma
- [ ] `.prisma/agentes/` contém agentes especializados
- [ ] `.prisma/prompts/prisma-prompt.md` existe

### Passo 2: Invocar o Prisma 🔧

**Quando**: Primeira vez usando workflow OU início de nova feature

```
Usuário: "quero criar uma nova feature [descrição]"
Assistente: [invoca agente carregador] → [carrega prompt principal]
```

**O que acontece:**

- Carrega `.prisma/prompts/prisma-prompt.md`
- Mostra workflow completo
- Lista agentes disponíveis
- Inicia processo de especificação

### Passo 3: Criar Primeira Especificação 📝

**Escolha seu caminho:**

**Option A: Feature Simples** (recomendado para primeira vez)

- Exemplo: "botão de modo escuro"
- Tempo: 2-3 horas
- Processo: requisitos → design → tarefas → implementação

**Option B: Feature Complexa**

- Exemplo: "sistema de autenticação"
- Tempo: 8-12 horas
- Processo: elicitação → ideação → requisitos → design → tarefas → implementação

**Comando para iniciar:**

```
Usuário: "quero criar [descrição da feature]"
Assistente: [inicia workflow Prisma]
```

### Passo 4: Seguir Workflow 🎯

**Fase 1: Requisitos** (analista)

- Escreve requisitos em formato estruturado
- Valida com usuário
- Aprovação: "aprovado" ou "sim"

**Fase 2: Design** (designer)

- Cria design técnico com componentes
- Gera diagramas de arquitetura
- Valida com usuário

**Fase 3: Tarefas** (planejador)

- Gera lista de tarefas implementáveis
- Define dependências
- Valida com usuário

**Fase 4: Implementação** (implementador)

- Executa tarefas (padrão: uma por vez)
- Ou paralelo: "execute tarefa 2.1 e 2.2 em paralelo"

**Fase 5: Validação** (testador-specs, revisor, conformista)

- Testa implementação
- Revisa código
- Valida conformidade

### Passo 5: Commit & Celebrate 🎉

```bash
git add .
git commit -m "feat: implementa [feature] via Prisma workflow"
```

---

## 🎓 Learning Path

### Primeira Especificação (Feature Simples)

**Objetivo**: Entender workflow básico
**Feature Sugerida**: toggle de modo escuro
**Tempo**: 2-3 horas
**Foco**: Seguir processo, não complicar

### Segunda Especificação (Feature Moderada)

**Objetivo**: Praticar iteração
**Feature Sugerida**: edição de perfil de usuário
**Tempo**: 4-6 horas
**Foco**: Refinamento de requisitos, alternativas de design

### Terceira Especificação (Feature Complexa)

**Objetivo**: Dominar agentes avançados
**Feature Sugerida**: integração com pagamento
**Tempo**: 8-12 horas
**Foco**: Elicitação, ideação, arquitetura, decisões

---

## 🔧 Troubleshooting

### "Agente não responde"

**Causa**: System prompt não carregado
**Fix**: Invocar agente carregador primeiro

### "Não sei qual agente usar"

**Causa**: Falta contexto de ativação
**Fix**: Consultar `.prisma/agentes/[agente].md` seção "Quando Usar"

### "Requisitos muito vagos"

**Causa**: Formato estruturado não aplicado
**Fix**: Revisar template em `.prisma/templates/requisitos.md`

### "Design muito complexo"

**Causa**: Over-engineering
**Fix**: Consultar configurações e padrões do projeto

### "Tarefas muito granulares"

**Causa**: Decomposição excessiva
**Fix**: Guideline: 1 tarefa = 30-60 min de trabalho

---

## 📚 Key Resources

**Leitura Obrigatória** (antes da primeira spec):

- `.prisma/prompts/prisma-prompt.md` - Workflow completo
- `.prisma/onboarding.md` - Este documento
- `.prisma/configuracoes/prisma.yaml` - Configurações do sistema

**Referência** (durante specs):

- `.prisma/templates/` - Templates de documentos
- `.prisma/agentes/` - Documentação de cada agente
- `.prisma/comandos/` - Comandos disponíveis

**Avançado** (após 3+ specs):

- `.prisma/projeto/arquitetura/` - Padrões arquiteturais
- Agente meta - Melhorias no processo
- Agente auditor - Health checks profundos

---

## 🎯 Critérios de Sucesso

Você está onboarded quando:

- [ ] Completou 1 spec de feature simples (2-3h)
- [ ] Entende quando aprovar vs pedir mudanças
- [ ] Sabe invocar o workflow Prisma
- [ ] Conhece 5+ agentes principais
- [ ] Leu templates e configurações básicas

**Tempo para onboarding**: 4-6 horas (incluindo primeira spec)

---

## 🆘 Obtendo Ajuda

**Durante workflow:**

- Usuário: "explica [conceito]"
- Assistente: Explica sem sair do workflow

**Bloqueado?**

- Consultar documentação do agente relevante
- Invocar agente idealizador para explorar soluções
- Revisar este guia de onboarding

**Feedback:**

- Criar issue no repositório
- Documentar lições aprendidas no projeto

---

## 📋 Verificação de Setup

### Directory Structure ✅

```bash
# Verificar estrutura completa
tree .prisma -L 2

# Estrutura esperada:
.prisma/
├── agentes/
├── comandos/
├── configuracoes/
│   └── prisma.yaml
├── prompts/
│   └── prisma-prompt.md
├── templates/
│   ├── design.md
│   ├── requisitos.md
│   └── tarefas.md
└── onboarding.md
```

### Agentes Disponíveis ✅

```bash
# Listar agentes
ls .prisma/agentes/

# Principais agentes:
# - analista (requisitos)
# - designer (design técnico)
# - planejador (tarefas)
# - implementador (código)
# - testador, testador-specs (testes)
# - revisor (code review)
# - auditor (auditoria profunda)
# - conformista (compliance)
# - decisor (decisões de workflow)
# - arquiteto (documentação técnica)
# - elicitador (análise de alinhamento)
# - idealizador (brainstorming)
# - avaliador-riscos (análise de riscos)
# - juiz (seleção entre alternativas)
# - documentador (docs finais)
# - configurador (setup de projetos)
# - regulador (enforcement de padrões)
# - meta (otimização do sistema prisma)
# - carregador (loader do workflow)
```

### Configuração ✅

```bash
# Verificar configuração principal
cat .prisma/configuracoes/prisma.yaml | head -20

# Deve conter:
# - version
# - paths
# - agentes
# - workflow
# - quality standards
```

---

## ✅ Status: Pronto para Usar

Se todos os checks passaram:

- ✅ Estrutura de diretórios OK
- ✅ Agentes presentes
- ✅ Prompts disponíveis
- ✅ Configuração válida
- ✅ Templates prontos

**🎉 PRONTO PARA CRIAR ESPECIFICAÇÕES**

---

**Última Atualização**: 2025-10-14
**Sistema**: Prisma v1.0
**Status**: Ativo
