# Command: /status-especificacao

## Description

Exibe status detalhado de uma especificação, incluindo progresso, quality gates e próximos passos.

## Usage

```
/status-especificacao [feature-name] [detail-level]
```

## Parameters

- `feature-name` (opcional): Nome da feature (kebab-case). Se não fornecido, mostra todas as especificações
- `detail-level` (opcional): Nível de detalhe
  - `summary` (padrão): Visão resumida
  - `detailed`: Detalhes completos
  - `metrics`: Foco em métricas e quality gates

## What It Does

1. Localiza especificação em `.prisma/projeto/especificacoes/{feature-name}/`
2. Lê todos os documentos (requisitos, design, tarefas)
3. Analisa progresso de implementação
4. Verifica quality gates
5. Identifica blockers
6. Sugere próximos passos

## Status Information

### Workflow Phase

- 📝 Requirements (0-25%)
- 🎨 Design (25-50%)
- 📋 Task Planning (50-60%)
- ⚙️ Implementation (60-90%)
- ✅ Testing & Review (90-100%)

### Quality Gates

- ✅ Requirements approved
- ✅ Design approved
- ✅ Tasks approved
- ✅ Code review passed
- ✅ Tests passing
- ✅ Compliance validated

### Health Indicators

- 🟢 Healthy: No blockers, on track
- 🟡 Warning: Minor issues, attention needed
- 🔴 Blocked: Critical issues, action required

## Examples

```bash
# Status resumido de todas especificações
/status-especificacao

# Status detalhado de uma especificação
/status-especificacao export-markdown detailed

# Métricas e quality gates
/status-especificacao export-markdown metrics
```

## Expected Flow - Summary Mode

```
User: /status-especificacao
Assistant: 📊 Status de Especificações

🟢 export-markdown (75% complete)
   Phase: Implementation ⚙️
   Health: Healthy
   Tasks: 8/10 complete
   Next: Complete task 2.3

🟡 auth-integration (45% complete)
   Phase: Design 🎨
   Health: Warning - Design approval pending
   Blockers: 1 open question on OAuth flow
   Next: Resolve OAuth provider selection

🔴 payment-gateway (30% complete)
   Phase: Requirements 📝
   Health: Blocked - Security review required
   Blockers: 2 critical security concerns
   Next: Schedule security review

Total: 3 especificações
Active: 2 in progress, 1 blocked
```

## Expected Flow - Detailed Mode

```
User: /status-especificacao export-markdown detailed
Assistant: 📊 Status da Especificação: export-markdown

═══════════════════════════════════════════════════
🎯 Overview
═══════════════════════════════════════════════════
Feature Name: export-markdown
Created: 2025-01-15
Phase: Implementation ⚙️ (75% complete)
Health: 🟢 Healthy
Estimated Time: 24h (18h spent, 6h remaining)

═══════════════════════════════════════════════════
📋 Documents
═══════════════════════════════════════════════════
✅ requirements.md (approved 2025-01-15)
   - 12 requirements (8 functional, 4 non-functional)
   - Format: EARS ✓
   - Compliance: 98%

✅ design.md (approved 2025-01-16)
   - Architecture: Hexagonal ✓
   - Components: 5 defined
   - Diagrams: 3 Mermaid diagrams
   - Compliance: 95%

✅ tasks.md (approved 2025-01-17)
   - Total Tasks: 10
   - Dependencies: Mapped ✓
   - Estimates: 24h total

═══════════════════════════════════════════════════
⚙️ Implementation Progress
═══════════════════════════════════════════════════
Completed: 8/10 tasks (80%)
In Progress: 1 task (2.3 - Template engine integration)
Pending: 1 task (3.1 - End-to-end tests)

Recent Activity:
- [2025-01-18 14:30] Completed task 2.2 (Export formatter)
- [2025-01-18 10:15] Started task 2.3 (Template engine)
- [2025-01-17 16:45] Completed task 2.1 (Data models)

═══════════════════════════════════════════════════
🎯 Quality Gates
═══════════════════════════════════════════════════
✅ Requirements Approved
✅ Design Approved
✅ Tasks Approved
⏳ Code Review (pending - after task 2.3)
⏳ Tests Passing (pending - after task 3.1)
⏳ Compliance Validated (pending)

═══════════════════════════════════════════════════
📊 Metrics
═══════════════════════════════════════════════════
Files Changed: 12 files
Lines Added: +842
Lines Removed: -156
Test Coverage: 78% (target: 80%)
Code Quality: 8.5/10
Complexity: Medium

═══════════════════════════════════════════════════
🚧 Blockers & Issues
═══════════════════════════════════════════════════
(nenhum blocker crítico)

⚠️ Warnings (2):
1. Test coverage slightly below target (78% vs 80%)
2. 1 dependency version conflict (marked@5 vs marked@4)

═══════════════════════════════════════════════════
🎯 Next Steps
═══════════════════════════════════════════════════
1. Complete task 2.3 (Template engine) - Est: 3h
2. Run code-review agent
3. Complete task 3.1 (E2E tests) - Est: 3h
4. Validate compliance
5. Deploy to staging

═══════════════════════════════════════════════════
📅 Timeline
═══════════════════════════════════════════════════
Started: 2025-01-15 (3 days ago)
Current: 2025-01-18 (Day 4)
Estimated Completion: 2025-01-19 (1 day remaining)
On Track: ✅ Yes

Deseja executar próxima ação? (sim/não)
```

## Status Dashboard

```
┌─────────────────────────────────────────────────┐
│ Especificação: export-markdown           🟢 75% │
├─────────────────────────────────────────────────┤
│ Phase                                           │
│ ████████████████████░░░░░░ Implementation       │
│                                                 │
│ Quality Gates                                   │
│ ✅ Requirements  ✅ Design  ✅ Tasks             │
│ ⏳ Code Review   ⏳ Tests   ⏳ Compliance         │
│                                                 │
│ Tasks (8/10)                                    │
│ ████████████████░░ 80%                          │
│                                                 │
│ Estimated Completion: 2025-01-19 (tomorrow)    │
└─────────────────────────────────────────────────┘
```

## Integration Points

- Atualizado automaticamente ao completar tasks
- Monitora quality gates automaticamente
- Sugere próximas ações baseado em estado
- Pode triggerar alertas se blockers detectados

## Related Commands

- `/executar-tarefas` - Executa próxima tarefa
- `/revisar-implementacao` - Revisa código atual
- `/validar-especificacao` - Valida conformidade
- `/analisar-riscos` - Analisa riscos atuais
