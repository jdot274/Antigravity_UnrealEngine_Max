# Comando: /auditar-especificacao

## Descrição

Executa auditoria profunda meta-analítica de especificações usando o agente auditor para identificar micro-melhorias e mudanças macro estratégicas.

## Uso

```
/auditar-especificacao [nome-feature] [escopo-auditoria] [formato-saida]
```

## Parâmetros

- `nome-feature` (opcional): Nome da feature (kebab-case). Se não fornecido, audita todas especificações ativas
- `escopo-auditoria` (opcional): Escopo da auditoria
  - `completo` (padrão): Auditoria completa (documentação + código + processo)
  - `documentacao`: Apenas documentos de especificação
  - `implementacao`: Apenas código implementado
  - `processo`: Apenas aderência ao workflow
  - `qualidade`: Foco em qualidade e padrões
- `formato-saida` (opcional): Formato do relatório
  - `detalhado` (padrão): Relatório completo com análise profunda
  - `executivo`: Resumo executivo para decisões
  - `acionavel`: Lista de ações prioritizadas

## O Que Faz

1. Análise cirúrgica do contexto completo da especificação
2. Identifica micro-melhorias implementáveis imediatamente
3. Detecta mudanças macro estratégicas necessárias
4. Avalia aderência a padrões e best practices
5. Analisa débito técnico e arquitetural
6. Sugere otimizações e refatorações
7. Gera relatório priorizado por impacto

## Dimensões da Auditoria

### Qualidade da Documentação

- Clareza e completude
- Consistência entre documentos
- Rastreabilidade (requisitos → design → tarefas → código)
- Atualização e manutenção

### Qualidade do Código

- Arquitetura e design patterns
- Qualidade e manutenibilidade
- Débito técnico
- Cobertura de testes e qualidade de testes

### Aderência ao Processo

- Etapas do workflow seguidas
- Quality gates validados
- Aprovações documentadas
- Lições aprendidas capturadas

### Alinhamento Estratégico

- Alinhamento com objetivos
- Trade-offs documentados
- Riscos gerenciados
- ROI e valor entregue

## Exemplos

```bash
# Auditoria completa
/auditar-especificacao export-markdown

# Auditoria focada em documentação
/auditar-especificacao export-markdown documentacao

# Auditoria de implementação com ações
/auditar-especificacao export-markdown implementacao acionavel

# Resumo executivo de todas especificações
/auditar-especificacao todas completo executivo
```

## Fluxo Esperado - Relatório Detalhado

```
User: /auditar-especificacao export-markdown
Assistant: Iniciando auditoria profunda de 'export-markdown'...

📋 Contexto:
- Feature: export-markdown
- Fase: Implementação (75% completo)
- Criada: 2025-01-15 (3 dias atrás)
- Arquivos: 12 modificados (+842/-156 linhas)

🔍 Executando agente auditor (análise meta-analítica)...

[Agente executa análise cirúrgica completa]

╔══════════════════════════════════════════════════╗
║      RELATÓRIO DE AUDITORIA: export-markdown     ║
╚══════════════════════════════════════════════════╝

📊 Pontuação Geral: 8.2/10 (Muito Bom)

══════════════════════════════════════════════════
🎯 RESUMO EXECUTIVO
══════════════════════════════════════════════════

Qualidade da Especificação: 🟢 Forte
- Documentação bem estruturada (98% conforme)
- Requisitos claros com boa rastreabilidade
- Implementação em andamento (75% completo)

Principais Achados:
- 3 micro-melhorias identificadas (ganhos rápidos)
- 1 oportunidade estratégica macro detectada
- Especificação saudável no geral com pequenas otimizações

Recomendação: Prosseguir com abordagem atual + aplicar
micro-melhorias durante implementação restante.

══════════════════════════════════════════════════
🔬 MICRO-MELHORIAS (Implementáveis Agora)
══════════════════════════════════════════════════

🟢 MM-1: Adicionar Orçamento de Performance aos Requisitos
   Impacto: Médio | Esforço: Baixo (30 min)

   Estado Atual:
   - requirements.md menciona "performance" genericamente
   - Sem métricas específicas ou orçamentos definidos

   Melhoria:
   + Adicionar requisito: "Export deve completar em <3s
     para workflows <1000 nodes"
   + Define critério de sucesso mensurável

   Implementação:
   - Atualizar requirements.md seção 3.2
   - Adicionar critério de aceitação à tarefa 3.1

🟡 MM-2: Extrair Interface do Motor de Templates
   Impacto: Alto | Esforço: Médio (2h)

   Estado Atual:
   - Lógica de template fortemente acoplada ao formatter
   - Dificulta testes e extensibilidade

   Melhoria:
   + Extrair interface ITemplateEngine
   + Permite plugin de templates customizados
   + Melhora testabilidade

   Implementação:
   - Criar src/templates/ITemplateEngine.ts
   - Refatorar src/export/formatter.ts
   - Adicionar testes unitários para abstração de template

🟢 MM-3: Documentar Estratégia de Rollback
   Impacto: Médio | Esforço: Baixo (45 min)

   Estado Atual:
   - design.md não menciona rollback
   - Risco operacional não endereçado

   Melhoria:
   + Adicionar seção de rollback ao design.md
   + Documentar procedimentos de recuperação
   + Definir gatilhos de rollback

   Implementação:
   - Atualizar design.md seção 5 (Operações)
   - Adicionar tarefa de rollback ao tasks.md

══════════════════════════════════════════════════
🚀 OPORTUNIDADES ESTRATÉGICAS MACRO
══════════════════════════════════════════════════

OEM-1: Generalizar Framework de Exportação
   Impacto: 🔥 Muito Alto | Esforço: Alto (40h)
   Valor Estratégico: Capacidade de plataforma

   Abordagem Atual:
   - Feature de export específica para Markdown
   - Lógica fortemente acoplada ao formato

   Oportunidade Estratégica:
   🎯 Transformar em framework de exportação plugável

   Visão:
   - Interface IExporter genérica
   - Arquitetura de plugins (Markdown, PDF, JSON, etc.)
   - Reutilizável em múltiplas features

   Benefícios:
   + Capacidade de plataforma (não apenas feature)
   + Reduz tempo de desenvolvimento futuro em 60%
   + Abre ecossistema para exportadores de terceiros
   + Aumenta diferenciação do produto

   Caminho de Implementação:
   Fase 1: Extrair abstração (8h)
   - Criar interface src/export/IExporter.ts
   - Refatorar markdown exporter como plugin

   Fase 2: Sistema de plugins (16h)
   - Adicionar registro de plugins
   - Implementar carregamento de plugins
   - Criar documentação de plugins

   Fase 3: Formatos adicionais (16h)
   - Plugin exportador PDF
   - Plugin exportador JSON
   - Plugin exportador CSV

   Decisão Necessária:
   🤔 Devemos pivotar para abordagem de framework agora ou
      entregar MVP markdown primeiro e refatorar depois?

   Recomendação: Criar ADR com agente decisor

══════════════════════════════════════════════════
📐 ANÁLISE DE ARQUITETURA
══════════════════════════════════════════════════

✅ Pontos Fortes:
1. Arquitetura hexagonal bem aplicada
2. Separação clara de responsabilidades
3. Bom uso de injeção de dependências
4. Interfaces bem definidas

⚠️  Oportunidades:
1. Acoplamento de template (endereçado em MM-2)
2. Generalização do framework de exportação (endereçado em OEM-1)
3. Tratamento de erros pode ser mais robusto

Pontuação de Débito Técnico: 2.5/10 (Baixo) 🟢
- Débito mínimo introduzido
- Maioria dos atalhos documentados
- Caminho de refatoração claro

══════════════════════════════════════════════════
📋 ANÁLISE DE DOCUMENTAÇÃO
══════════════════════════════════════════════════

Requisitos (requirements.md): 9.5/10
✅ Excelente formato EARS
✅ Boa rastreabilidade
⚠️  Faltam orçamentos de performance (MM-1)

Design (design.md): 8.5/10
✅ Arquitetura abrangente
✅ Bons diagramas
⚠️  Faltam seções operacionais (MM-3)

Tarefas (tasks.md): 9.0/10
✅ Decomposição bem estruturada
✅ Dependências claras
✅ Boas estimativas

Consistência Entre Documentos: 95% ✅

══════════════════════════════════════════════════
🧪 ANÁLISE DE QUALIDADE DO CÓDIGO
══════════════════════════════════════════════════

Código Implementado: 8.5/10

Pontos Fortes:
+ Código limpo e legível
+ Bom uso de TypeScript
+ Tratamento de erros adequado
+ Segue padrões estabelecidos

Áreas para Melhoria:
- Cobertura de testes: 78% (meta: 80%)
- Algumas funções >50 linhas
- Falta JSDoc em APIs públicas

Métricas de Complexidade:
- Complexidade Ciclomática: 4.2 média (boa)
- Complexidade Cognitiva: 6.8 média (aceitável)
- Índice de Manutenibilidade: 82/100 (bom)

══════════════════════════════════════════════════
📈 PROGRESS & VELOCITY ANALYSIS
══════════════════════════════════════════════════

Velocity: 🟢 Healthy
- 8/10 tasks complete (80%)
- 3 days elapsed, 1 day remaining
- On track for estimated completion

Blockers: None critical
Quality Gates: 3/6 passed

Projection:
✅ Will complete implementation on time
✅ Quality gates achievable
⚠️  Recommend scheduling tech debt review post-launch

══════════════════════════════════════════════════
🎯 PRIORITIZED ACTION PLAN
══════════════════════════════════════════════════

Immediate (This Sprint):
1. [30 min] MI-1: Add performance budget to requirements
2. [45 min] MI-3: Document rollback strategy
3. [3h] Complete remaining tasks (2.3, 3.1)

Short-term (Next Sprint):
4. [2h] MI-2: Extract template engine interface
5. [2h] Increase test coverage to 80%+
6. [1h] Add JSDoc to public APIs

Strategic (Next Quarter):
7. [40h] MS-1: Evaluate export framework approach
   → Create ADR with spec-decision agent
   → Present to architecture review
   → Plan Phase 1 if approved

══════════════════════════════════════════════════
🏆 LESSONS LEARNED
══════════════════════════════════════════════════

What Went Well:
✅ Clear requirements prevented scope creep
✅ Hexagonal architecture enabled clean code
✅ Task breakdown was accurate

What Could Improve:
💡 Define performance budgets upfront
💡 Consider operational concerns in design phase
💡 Explore strategic opportunities earlier

Transferable Insights:
🎓 Template abstraction pattern useful for other features
🎓 Export framework could become platform capability
🎓 Early performance budgets prevent late surprises

══════════════════════════════════════════════════
📊 AUDIT METADATA
══════════════════════════════════════════════════

Audit Date: 2025-01-18 15:30
Auditor: code-audit agent
Scope: Full (documentation + code + process)
Depth: Deep analysis
Files Analyzed: 15
Time Spent: 45 minutes

Next Audit: Recommended after completion (2025-01-20)

╔══════════════════════════════════════════════════╗
║           END OF AUDIT REPORT                    ║
╚══════════════════════════════════════════════════╝

Deseja:
1. Aplicar micro-improvements agora? (sim/não)
2. Criar ADR para decisão macro estratégica? (sim/não)
3. Exportar relatório para markdown? (sim/não)
```

## Fluxo Esperado - Formato Acionável

```
User: /auditar-especificacao export-markdown implementacao acionavel
Assistant: 🎯 Auditoria Acionável: export-markdown

═══════════════════════════════════════════════════
⚡ QUICK WINS (< 1h cada)
═══════════════════════════════════════════════════

[ ] Add performance budget to requirements.md
    Time: 30 min | Impact: Medium
    File: .claude/specs/export-markdown/requirements.md
    Action: Add section 3.2 with metric "<3s for <1000 nodes"

[ ] Document rollback strategy in design.md
    Time: 45 min | Impact: Medium
    File: .claude/specs/export-markdown/design.md
    Action: Add section 5 (Operations) with rollback procedures

═══════════════════════════════════════════════════
🔧 REFACTORINGS (1-3h cada)
═══════════════════════════════════════════════════

[ ] Extract ITemplateEngine interface
    Time: 2h | Impact: High
    Files: src/templates/, src/export/formatter.ts
    Action: Create abstraction + refactor + tests

[ ] Increase test coverage to 80%
    Time: 2h | Impact: Medium
    Files: src/**/*.test.ts
    Action: Add missing unit tests (currently 78%)

═══════════════════════════════════════════════════
🚀 STRATEGIC DECISIONS (Requires ADR)
═══════════════════════════════════════════════════

[ ] Evaluate Export Framework generalization
    Impact: Very High | Effort: 40h
    Decision: Ship MVP first or pivot to framework?
    Next: Create ADR with /make-decision

═══════════════════════════════════════════════════

Total Actions: 5
Estimated Time: 7.25h
Priority: Complete quick wins before launch

Executar ganhos rápidos agora? (sim/não)
```

## Detalhamento da Pontuação de Auditoria

```
Pontuação Geral: 8.2/10

Qualidade da Documentação:  9.0/10 ⭐⭐⭐⭐⭐
Qualidade do Código:        8.5/10 ⭐⭐⭐⭐
Aderência ao Processo:      8.0/10 ⭐⭐⭐⭐
Alinhamento Estratégico:    7.5/10 ⭐⭐⭐⭐

Micro-melhorias:            3 encontradas
Oportunidades macro:        1 encontrada
Débito Técnico:             2.5/10 (Baixo) ✅
```

## Pontos de Integração

- Pode acionar agente decisor para decisões estratégicas
- Sugere chamadas ao agente revisor ou conformista
- Atualiza lições aprendidas na especificação
- Gera relatório em `.prisma/projeto/especificacoes/{nome-feature}/relatorio-auditoria.md`

## Gatilhos de Auditoria

Recomenda auditoria quando:

- Especificação atinge 50% de implementação (ponto médio)
- Antes de decisões arquiteturais críticas
- Após mudanças significativas de escopo
- Post-mortem após conclusão
- Periodicamente (trimestral) para especificações de longa duração

## Comandos Relacionados

- `/analisar-riscos` - Análise de riscos específica
- `/validar-especificacao` - Validação de conformidade
- `/revisar-implementacao` - Revisão de código
- `/tomar-decisao` - Criar ADR para decisões
