# Comandos Prisma - Guia de Referência

Sistema de comandos organizados hierarquicamente para o workflow Prisma.

## 📁 Estrutura de Diretórios

```
.prisma/comandos/
├── analisar/          # Comandos de análise
│   └── riscos.md      # Análise de riscos
├── especificacao/     # Gerenciamento de especificações
│   ├── atualizar.md   # Atualizar especificação existente
│   ├── auditar.md     # Auditar especificação
│   ├── listar.md      # Listar especificações
│   ├── nova.md        # Criar nova especificação
│   ├── status.md      # Status detalhado
│   └── validar.md     # Validar conformidade
├── implementacao/     # Comandos de implementação
│   ├── paralela.md    # Implementação paralela
│   └── revisar.md     # Revisar implementação
├── organizar/         # Comandos de organização
│   ├── documentacao.md              # Organizar documentação
│   ├── documentacao-v2-aggressive.md # Versão agressiva
│   └── relatorios.md                # Organizar relatórios
├── tarefa/            # Comandos de tarefas
│   └── executar.md    # Executar tarefas
├── testes/            # Comandos de testes
│   └── executar.md    # Executar testes
├── decidir.md         # Criar ADR (Architecture Decision Record)
└── prisma.md          # Comando principal do sistema
```

## 🎯 Mapeamento de Comandos

### Comandos Claude Code → Comandos Prisma

| Claude Code Command | Prisma Command Path | Descrição |
|---------------------|---------------------|-----------|
| **`/prisma:iniciar`** | **`.prisma/comandos/iniciar.md`** | **🚀 Inicializa sistema Prisma e carrega orquestrador principal** |
| `/prisma:analisar-riscos` | `.prisma/comandos/analisar/riscos.md` | Análise de riscos com spec-risk agent |
| `/prisma:especificacao-nova` | `.prisma/comandos/especificacao/nova.md` | Inicia criação de nova especificação |
| `/prisma:especificacao-atualizar` | `.prisma/comandos/especificacao/atualizar.md` | Atualiza especificação existente |
| `/prisma:especificacao-listar` | `.prisma/comandos/especificacao/listar.md` | Lista todas especificações |
| `/prisma:especificacao-status` | `.prisma/comandos/especificacao/status.md` | Status detalhado de especificação |
| `/prisma:especificacao-auditar` | `.prisma/comandos/especificacao/auditar.md` | Audita especificação |
| `/prisma:especificacao-validar` | `.prisma/comandos/especificacao/validar.md` | Valida conformidade |
| `/prisma:implementacao-paralela` | `.prisma/comandos/implementacao/paralela.md` | Implementação paralela com múltiplos agentes |
| `/prisma:implementacao-revisar` | `.prisma/comandos/implementacao/revisar.md` | Revisão de código implementado |
| `/prisma:tarefa-executar` | `.prisma/comandos/tarefa/executar.md` | Executa tarefas sequencialmente |
| `/prisma:testes-executar` | `.prisma/comandos/testes/executar.md` | Executa testes com spec-test agent |
| `/prisma:decidir` | `.prisma/comandos/decidir.md` | Cria ADR para decisões importantes |
| `/prisma:organizar-documentacao` | `.prisma/comandos/organizar/documentacao.md` | Organiza documentação |
| `/prisma:organizar-relatorios` | `.prisma/comandos/organizar/relatorios.md` | Organiza relatórios |

## 📋 Comandos por Categoria

### 🚀 Sistema Principal

#### `/prisma:iniciar`
**Caminho**: [iniciar.md](./iniciar.md)

**Comando de entrada principal do sistema Prisma.** Carrega o agente orquestrador e inicializa workflow completo.

**Use quando:**
- ✅ Primeira vez usando Prisma
- ✅ Iniciar nova feature
- ✅ Não sabe qual comando usar
- ✅ Retomar workflow interrompido

**Modos de execução:**
1. **Com feature name**: `/prisma:iniciar {feature-name}` - Inicia workflow para feature específica
2. **Sem parâmetro**: `/prisma:iniciar` - Modo menu interativo

**O que faz:**
1. Carrega system prompt do Prisma
2. Invoca agente orquestrador `prisma`
3. Detecta estado atual (nova feature ou continuar existente)
4. Guia usuário através do workflow completo

**Exemplo**:
```bash
# Nova feature
/prisma:iniciar payment-api

# Modo exploratório
/prisma:iniciar
```

---

### 🔍 Análise

#### `/prisma:analisar-riscos`
**Caminho**: [analisar/riscos.md](./analisar/riscos.md)

Análise profunda de riscos técnicos, arquiteturais e de negócio usando o agente `avaliador-riscos`.

**Uso**: Antes de decisões arquiteturais importantes, refatorações críticas, ou features de alta complexidade.

---

### 📝 Especificações

#### `/prisma:especificacao-nova`
**Caminho**: [especificacao/nova.md](./especificacao/nova.md)

Inicia o processo de criação de uma nova especificação guiando o usuário através de:
1. Requirements (com agente `analista`)
2. Design (com agente `designer`)
3. Tasks (com agente `planejador`)

#### `/prisma:especificacao-atualizar`
**Caminho**: [especificacao/atualizar.md](./especificacao/atualizar.md)

Atualiza especificação existente (requirements, design, ou tasks) com feedback iterativo.

#### `/prisma:especificacao-listar`
**Caminho**: [especificacao/listar.md](./especificacao/listar.md)

Lista todas as especificações com status, progresso e filtros.

#### `/prisma:especificacao-status`
**Caminho**: [especificacao/status.md](./especificacao/status.md)

Mostra status detalhado de uma especificação incluindo quality scores, tasks completadas e blockers.

#### `/prisma:especificacao-auditar`
**Caminho**: [especificacao/auditar.md](./especificacao/auditar.md)

Auditoria profunda pós-implementação usando agente `auditor` para identificar micro-melhorias e macro-mudanças.

#### `/prisma:especificacao-validar`
**Caminho**: [especificacao/validar.md](./especificacao/validar.md)

Valida conformidade da especificação com padrões Prisma usando agente `conformista`.

---

### ⚙️ Implementação

#### `/prisma:implementacao-paralela`
**Caminho**: [implementacao/paralela.md](./implementacao/paralela.md)

Executa múltiplas tasks em paralelo usando múltiplas instâncias do agente `implementador`.

**Vantagens**:
- 🚀 Até 5x mais rápido
- 🔄 Coordenação automática de dependências
- 📊 Dashboard de progresso em tempo real

#### `/prisma:implementacao-revisar`
**Caminho**: [implementacao/revisar.md](./implementacao/revisar.md)

Revisão de código implementado usando agente `revisor` com critérios objetivos de qualidade.

---

### ✅ Tarefas e Testes

#### `/prisma:tarefa-executar`
**Caminho**: [tarefa/executar.md](./tarefa/executar.md)

Executa tarefas sequencialmente ou em modo automático com agente `implementador`.

**Modos**:
- **sequential**: Uma task por vez com aprovação
- **auto**: Execução automática de tasks independentes

#### `/prisma:testes-executar`
**Caminho**: [testes/executar.md](./testes/executar.md)

Executa e cria testes usando agente `testador-specs` seguindo Test Trophy + Hexagonal Architecture.

---

### 🎯 Decisões

#### `/prisma:decidir`
**Caminho**: [decidir.md](./decidir.md)

Cria Architecture Decision Record (ADR) usando agente `decisor`.

**Quando usar**:
- Mudanças arquiteturais significativas
- Escolha de tecnologias/frameworks
- Trade-offs complexos
- Decisões que afetam múltiplas features

**Estrutura ADR**:
- Status (Proposed/Accepted/Deprecated)
- Context (situação)
- Decision (o que foi decidido)
- Options Considered (alternativas)
- Consequences (impactos)
- Trade-offs (compromissos)

---

### 📁 Organização

#### `/prisma:organizar-documentacao`
**Caminho**: [organizar/documentacao.md](./organizar/documentacao.md)

Varredura completa e organização automática de toda documentação segundo padrões Prisma.

**Funcionalidades**:
- 🔍 Varredura completa do repositório
- 📊 Classificação por tipo e audiência
- 📁 Organização automática
- 🗄️ Arquivamento de obsoletos
- 📝 Detecção de ADRs não documentados
- 🔗 Correção de links quebrados

#### `/prisma:organizar-relatorios`
**Caminho**: [organizar/relatorios.md](./organizar/relatorios.md)

Organiza relatórios de auditoria, execução e revisão em estrutura padronizada.

---

## 🔄 Fluxos de Trabalho

### Fluxo Padrão: Nova Feature

```bash
# 1. Criar especificação
/prisma:especificacao-nova

# 2. Analisar riscos (opcional mas recomendado)
/prisma:analisar-riscos [feature-name]

# 3. Criar ADR se necessário
/prisma:decidir [feature-name]

# 4. Implementar
/prisma:implementacao-paralela [feature-name]
# OU
/prisma:tarefa-executar [feature-name]

# 5. Executar testes
/prisma:testes-executar [feature-name]

# 6. Revisar implementação
/prisma:implementacao-revisar [feature-name]

# 7. Validar especificação
/prisma:especificacao-validar [feature-name]

# 8. Auditar (pós-conclusão)
/prisma:especificacao-auditar [feature-name]
```

### Fluxo Rápido: Feature Simples

```bash
/prisma:especificacao-nova
/prisma:tarefa-executar [feature-name]
/prisma:testes-executar [feature-name]
```

### Fluxo Complexo: Feature Crítica

```bash
/prisma:especificacao-nova
/prisma:analisar-riscos [feature-name]
/prisma:decidir [feature-name]
/prisma:especificacao-validar [feature-name]
/prisma:implementacao-paralela [feature-name]
/prisma:testes-executar [feature-name]
/prisma:implementacao-revisar [feature-name]
/prisma:especificacao-auditar [feature-name]
```

## 🎭 Agentes Utilizados

| Comando | Agente Principal | Agentes Secundários |
|---------|------------------|---------------------|
| `analisar/riscos` | `avaliador-riscos` | `auditor`, `conformista` |
| `especificacao/nova` | `elicitador`, `analista`, `designer`, `planejador` | `conformista`, `decisor` |
| `especificacao/atualizar` | `analista`, `designer`, `planejador` | `conformista` |
| `especificacao/auditar` | `auditor` | `revisor`, `conformista` |
| `especificacao/validar` | `conformista` | `auditor` |
| `implementacao/paralela` | `implementador` (múltiplos) | `regulador`, `decisor` |
| `implementacao/revisar` | `revisor` | `regulador` |
| `tarefa/executar` | `implementador` | `regulador` |
| `testes/executar` | `testador-specs` | `implementador` |
| `decidir` | `decisor` | `auditor`, `avaliador-riscos` |
| `organizar/documentacao` | `documentador` | `auditor`, `conformista`, `arquiteto` |

## 📊 Quality Gates

Cada fase tem critérios mínimos de qualidade:

| Fase | Quality Gate | Threshold | Comando Validador |
|------|--------------|-----------|-------------------|
| Requirements | Completude EARS | ≥95% | `especificacao/validar` |
| Design | Consistência Arquitetural | ≥90% | `especificacao/validar` |
| Tasks | Decomposição Clara | ≥95% | `especificacao/validar` |
| Implementation | Code Quality Score | ≥7/10 | `implementacao/revisar` |
| Tests | Coverage | ≥80% | `testes/executar` |
| Compliance | Aderência a Padrões | ≥95% | `especificacao/validar` |

## 🚀 Quick Reference

### Comandos Mais Usados

```bash
# 🚀 COMEÇAR AQUI - Inicializar Prisma
/prisma:iniciar [feature-name]

# Ou criar especificação diretamente
/prisma:especificacao-nova

# Ver todas as especificações
/prisma:especificacao-listar

# Status de uma feature
/prisma:especificacao-status [feature-name]

# Implementar rápido
/prisma:implementacao-paralela [feature-name]

# Validar qualidade
/prisma:testes-executar [feature-name]
/prisma:implementacao-revisar [feature-name]
```

### Quando Usar Cada Comando

**Use `/prisma:implementacao-paralela`** quando:
- ✅ Tasks independentes bem definidas
- ✅ Velocidade é prioridade
- ✅ Deadline apertado

**Use `/prisma:tarefa-executar`** quando:
- ✅ Quer controle interativo
- ✅ Tasks complexas que precisam supervisão
- ✅ Aprendendo o codebase

**Use `/prisma:analisar-riscos`** quando:
- ✅ Decisões arquiteturais importantes
- ✅ Features críticas (segurança, pagamentos)
- ✅ Antes de refatorações grandes

**Use `/prisma:decidir`** quando:
- ✅ Múltiplas opções viáveis
- ✅ Trade-offs precisam documentação
- ✅ Alinhamento de time necessário

**Use `/prisma:especificacao-auditar`** quando:
- ✅ Feature completamente implementada
- ✅ Pós-mortem de feature
- ✅ Review periódica (cada 5 features)

## 🔗 Sincronização com Claude Code

Os comandos Prisma são espelhados em `.claude/commands/prisma/` para integração com Claude Code:

- **Prisma**: `.prisma/comandos/` → Implementação completa dos comandos
- **Claude Code**: `.claude/commands/prisma/` → Pointers que carregam comandos Prisma

**Exemplo**:
```markdown
# .claude/commands/prisma/especificacao/nova.md
Este comando carrega as instruções de `.prisma/comandos/especificacao/nova.md`.

**Caminho**: `.prisma/comandos/especificacao/nova.md`
```

## 📚 Documentação Adicional

- **Agentes**: [.prisma/agentes/](../agentes/)
- **Templates**: [.prisma/templates/](../templates/)
- **Configurações**: [.prisma/configuracoes/prisma.yaml](../configuracoes/prisma.yaml)
- **Prompts**: [.prisma/prompts/](../prompts/)

---

**Precisa de Ajuda?**

1. **Primeiro contato?** → `/prisma:iniciar` (modo menu interativo)
2. **Quer explorar?** → `/prisma:especificacao-listar` (ver specs disponíveis)
3. **Feature específica?** → `/prisma:iniciar {feature-name}` (workflow guiado)
4. **Já sabe o que fazer?** → Use comando específico diretamente
5. **Dúvidas?** → Leia documentação individual de cada comando

**Fluxo Recomendado para Iniciantes:**
```bash
/prisma:iniciar                    # Passo 1: Inicializar sistema
# Sistema te guiará pelo resto!
```
