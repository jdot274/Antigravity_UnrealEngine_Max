#!/bin/bash
# Script de Setup da Estrutura Prisma
# Cria toda a hierarquia de pastas necessária para o workflow

set -e

PROJECT_ROOT="$(pwd)"
PRISMA_DIR="$PROJECT_ROOT/.prisma"

echo "🚀 Iniciando setup da estrutura Prisma..."
echo ""

# Verificar se já existe
if [ -d "$PRISMA_DIR" ]; then
    echo "✅ Pasta .prisma já existe"
else
    echo "📁 Criando pasta .prisma..."
    mkdir -p "$PRISMA_DIR"
fi

cd "$PRISMA_DIR"

# ============================================================================
# NÍVEL 1: Pastas principais
# ============================================================================

echo ""
echo "📦 Criando pastas principais..."

mkdir -p agentes
mkdir -p checkpoints
mkdir -p comandos
mkdir -p configuracoes
mkdir -p melhorias
mkdir -p projeto
mkdir -p prompts
mkdir -p relatorios
mkdir -p templates
mkdir -p workflows

echo "  ✅ agentes/"
echo "  ✅ checkpoints/"
echo "  ✅ comandos/"
echo "  ✅ configuracoes/"
echo "  ✅ melhorias/"
echo "  ✅ projeto/"
echo "  ✅ prompts/"
echo "  ✅ relatorios/"
echo "  ✅ templates/"
echo "  ✅ workflows/"

# ============================================================================
# NÍVEL 2: Subpastas de comandos
# ============================================================================

echo ""
echo "📂 Criando subpastas de comandos..."

mkdir -p comandos/analisar
mkdir -p comandos/especificacao
mkdir -p comandos/implementacao
mkdir -p comandos/organizar
mkdir -p comandos/tarefa
mkdir -p comandos/testes

echo "  ✅ comandos/analisar/"
echo "  ✅ comandos/especificacao/"
echo "  ✅ comandos/implementacao/"
echo "  ✅ comandos/organizar/"
echo "  ✅ comandos/tarefa/"
echo "  ✅ comandos/testes/"

# ============================================================================
# NÍVEL 2: Subpastas de melhorias
# ============================================================================

echo ""
echo "📂 Criando subpastas de melhorias..."

mkdir -p melhorias/agentes
mkdir -p melhorias/prompts

echo "  ✅ melhorias/agentes/"
echo "  ✅ melhorias/prompts/"

# ============================================================================
# NÍVEL 2: Subpastas de projeto (PRINCIPAL)
# ============================================================================

echo ""
echo "📂 Criando subpastas de projeto..."

mkdir -p projeto/analises
mkdir -p projeto/aprendizado
mkdir -p projeto/arquitetura
mkdir -p projeto/auditoria
mkdir -p projeto/checklists
mkdir -p projeto/decisoes
mkdir -p projeto/diretrizes
mkdir -p projeto/especificacoes
mkdir -p projeto/historico
mkdir -p projeto/implementacao
mkdir -p projeto/mapa
mkdir -p projeto/outros
mkdir -p projeto/padroes
mkdir -p projeto/relatorios
mkdir -p projeto/revisoes
mkdir -p projeto/sumarios

echo "  ✅ projeto/analises/"
echo "  ✅ projeto/aprendizado/"
echo "  ✅ projeto/arquitetura/"
echo "  ✅ projeto/auditoria/"
echo "  ✅ projeto/checklists/"
echo "  ✅ projeto/decisoes/"
echo "  ✅ projeto/diretrizes/"
echo "  ✅ projeto/especificacoes/"
echo "  ✅ projeto/historico/"
echo "  ✅ projeto/implementacao/"
echo "  ✅ projeto/mapa/"
echo "  ✅ projeto/outros/"
echo "  ✅ projeto/padroes/"
echo "  ✅ projeto/relatorios/"
echo "  ✅ projeto/revisoes/"
echo "  ✅ projeto/sumarios/"

# ============================================================================
# NÍVEL 2: Subpastas de relatorios
# ============================================================================

echo ""
echo "📂 Criando subpastas de relatorios..."

mkdir -p relatorios/agent-reports
mkdir -p relatorios/auditoria
mkdir -p relatorios/correcoes
mkdir -p relatorios/execucao
mkdir -p relatorios/hydration
mkdir -p relatorios/outros
mkdir -p relatorios/revisao
mkdir -p relatorios/revisao-codigo
mkdir -p relatorios/seguranca
mkdir -p relatorios/sumarios

echo "  ✅ relatorios/agent-reports/"
echo "  ✅ relatorios/auditoria/"
echo "  ✅ relatorios/correcoes/"
echo "  ✅ relatorios/execucao/"
echo "  ✅ relatorios/hydration/"
echo "  ✅ relatorios/outros/"
echo "  ✅ relatorios/revisao/"
echo "  ✅ relatorios/revisao-codigo/"
echo "  ✅ relatorios/seguranca/"
echo "  ✅ relatorios/sumarios/"

# ============================================================================
# NÍVEL 3: Estrutura padrão de especificações (template)
# ============================================================================

echo ""
echo "📂 Criando template de estrutura para especificações..."

mkdir -p projeto/especificacoes/_template/{artifacts,decisions,reports}

echo "  ✅ projeto/especificacoes/_template/"
echo "  ✅ projeto/especificacoes/_template/artifacts/"
echo "  ✅ projeto/especificacoes/_template/decisions/"
echo "  ✅ projeto/especificacoes/_template/reports/"

# Criar README no template
cat > projeto/especificacoes/_template/README.md <<'EOF'
# Template de Especificação

Esta pasta contém a estrutura padrão para uma nova especificação Prisma.

## Estrutura Padrão

```
{feature-name}/
├── requirements.md    # Requisitos da feature (analista)
├── design.md          # Design técnico (designer)
├── tasks.md           # Tarefas de implementação (planejador)
├── artifacts/         # Artefatos de implementação
├── decisions/         # Decisões tomadas durante desenvolvimento
└── reports/           # Relatórios de QA, riscos, compliance
```

## Como Usar

1. Copie esta pasta: `cp -r _template {sua-feature-name}`
2. Renomeie para kebab-case: `minha-nova-feature`
3. Inicie workflow Prisma: agente analista criará requirements.md

## Arquivos Principais

### requirements.md
- Criado por: **analista**
- Formato: EARS (Easy Approach to Requirements Syntax)
- Aprovação obrigatória antes de prosseguir

### design.md
- Criado por: **designer**
- Contém: Arquitetura, componentes, diagramas Mermaid
- Aprovação obrigatória antes de prosseguir

### tasks.md
- Criado por: **planejador**
- Contém: Lista de tarefas com dependências
- Formato: Mermaid Gantt + tabela de tasks

## Subpastas

### artifacts/
Artefatos criados durante implementação:
- Protótipos
- Dumps de configuração
- Dados de teste
- Screenshots

### decisions/
Decisões arquiteturais e técnicas:
- Trade-offs considerados
- Alternativas avaliadas
- Justificativas de escolhas

### reports/
Relatórios de validação:
- QA reports (testador-specs)
- Risk assessment (avaliador-riscos)
- Compliance checks (conformista)
- Code reviews (revisor)

---

**Nota**: Não edite este template diretamente. Sempre copie para criar nova spec.
EOF

echo "  ✅ projeto/especificacoes/_template/README.md"

# ============================================================================
# READMEs informativos
# ============================================================================

echo ""
echo "📝 Criando READMEs informativos..."

# README principal do projeto
cat > projeto/README.md <<'EOF'
# Prisma - Documentação do Projeto

Esta pasta contém toda a documentação centralizada do projeto.

## Estrutura

- **analises/**: Análises de código, arquitetura, performance
- **aprendizado/**: Lições aprendidas, retrospectivas
- **arquitetura/**: Padrões arquiteturais, decisões técnicas
- **auditoria/**: Auditorias de qualidade, segurança, compliance
- **checklists/**: Checklists de validação e processo
- **decisoes/**: ADRs (Architecture Decision Records)
- **diretrizes/**: Guidelines de desenvolvimento
- **especificacoes/**: Especificações de features (requirements, design, tasks)
- **historico/**: Histórico de mudanças importantes
- **implementacao/**: Guias de implementação
- **mapa/**: Mapas do sistema (dependency graphs, visual maps)
- **outros/**: Documentação que não se encaixa em categorias acima
- **padroes/**: Padrões de código, testes, documentação
- **relatorios/**: Relatórios permanentes de projeto
- **revisoes/**: Revisões de código, arquitetura, processo
- **sumarios/**: Sumários executivos de projetos e fases

## Especificações vs Relatórios

- **projeto/especificacoes/**: Documentos PERMANENTES de features (versionados)
- **projeto/relatorios/**: Relatórios de ANÁLISE permanentes
- **.prisma/relatorios/**: Relatórios de EXECUÇÃO temporários (podem ser limpos)

## Como Navegar

1. **Para entender o projeto**: Comece por `arquitetura/`
2. **Para criar nova feature**: Use `especificacoes/_template/`
3. **Para decisões arquiteturais**: Consulte `decisoes/`
4. **Para padrões de código**: Consulte `padroes/`
EOF

# README de especificações
cat > projeto/especificacoes/README.md <<'EOF'
# Especificações de Features

Esta pasta contém todas as especificações de features do projeto.

## Estrutura de uma Especificação

Cada feature tem sua própria pasta com estrutura padronizada:

```
{feature-name}/
├── requirements.md    # Requisitos (analista)
├── design.md          # Design técnico (designer)
├── tasks.md           # Tarefas (planejador)
├── artifacts/         # Artefatos de implementação
├── decisions/         # Decisões durante desenvolvimento
└── reports/           # Relatórios de QA, riscos, compliance
```

## Workflow Prisma

1. **analista** → Cria `requirements.md`
2. **designer** → Cria `design.md`
3. **planejador** → Cria `tasks.md`
4. **implementador** → Executa tasks
5. **testador-specs** → Valida com testes
6. **revisor** → Revisa código
7. **conformista** → Valida compliance
8. **documentador** → Documenta em `/docs`

## Criar Nova Especificação

```bash
# Copiar template
cp -r _template minha-feature

# Iniciar workflow
# Invocar: "criar nova especificação para [descrição]"
```

## Convenções

- **Naming**: kebab-case (`payment-api`, `user-profile`)
- **Status**: Draft → In Progress → Complete
- **Approval**: Cada fase requer aprovação do usuário

## Ver Também

- Template: `_template/`
- Onboarding: `.prisma/comandos/onboarding.md`
- Workflow completo: `.prisma/prompts/prisma-prompt.md`
EOF

echo "  ✅ projeto/README.md"
echo "  ✅ projeto/especificacoes/README.md"

# ============================================================================
# .gitkeep para pastas vazias
# ============================================================================

echo ""
echo "📌 Criando .gitkeep para preservar estrutura no git..."

# Criar .gitkeep em todas as pastas vazias
find . -type d -empty -exec touch {}/.gitkeep \;

echo "  ✅ .gitkeep criado em pastas vazias"

# ============================================================================
# Finalização
# ============================================================================

echo ""
echo "✅ Setup completo!"
echo ""
echo "📊 Estrutura criada:"
echo "  - $(find . -type d | wc -l) pastas"
echo "  - $(find . -type f | wc -l) arquivos"
echo ""
echo "📁 Localização:"
echo "  $PRISMA_DIR"
echo ""
echo "🎯 Próximos passos:"
echo "  1. Verificar estrutura: tree .prisma -L 2"
echo "  2. Ler onboarding: cat .prisma/comandos/onboarding.md"
echo "  3. Iniciar primeira spec: Invocar workflow Prisma"
echo ""
echo "🎉 Pronto para usar o Prisma!"
