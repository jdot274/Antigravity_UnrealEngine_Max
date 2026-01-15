# Command: /listar-especificacoes

## Description

Lista todas as especificações disponíveis com status, progresso e próximas ações.

## Usage

```
/listar-especificacoes [filter] [sort-by]
```

## Parameters

- `filter` (opcional): Filtro de status
  - `all` (padrão): Todas as especificações
  - `active`: Especificações em progresso
  - `pending`: Especificações não iniciadas
  - `completed`: Especificações finalizadas
  - `blocked`: Especificações com blockers
- `sort-by` (opcional): Ordenação
  - `recent` (padrão): Mais recentes primeiro
  - `progress`: Por % de progresso
  - `priority`: Por prioridade
  - `name`: Por nome alfabético

## What It Does

1. Escaneia `.prisma/projeto/especificacoes/` por todas as features
2. Lê status de cada especificação
3. Calcula progresso e health
4. Lista com formato visual
5. Sugere próximas ações

## Examples

```bash
# Listar todas especificações
/listar-especificacoes

# Especificações ativas
/listar-especificacoes active

# Especificações por progresso
/listar-especificacoes all progress

# Especificações bloqueadas
/listar-especificacoes blocked
```

## Expected Flow

```
User: /listar-especificacoes
Assistant: 📊 Especificações Disponíveis (3 especificações)

┌─────────────────────────────────────────────────┐
│ 🟢 export-markdown                       75%    │
├─────────────────────────────────────────────────┤
│ Phase: Implementation ⚙️                        │
│ Created: 2025-01-15 (3 days ago)                │
│ Health: Healthy                                 │
│ Tasks: 8/10 complete                            │
│ Next: Complete task 2.3                         │
│ Files: .prisma/projeto/especificacoes/export-markdown/           │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ 🟡 auth-integration                      45%    │
├─────────────────────────────────────────────────┤
│ Phase: Design 🎨                                │
│ Created: 2025-01-12 (6 days ago)                │
│ Health: Warning                                 │
│ Blocker: Design approval pending                │
│ Next: Resolve OAuth provider selection          │
│ Files: .prisma/projeto/especificacoes/auth-integration/          │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ 🔴 payment-gateway                       30%    │
├─────────────────────────────────────────────────┤
│ Phase: Requirements 📝                          │
│ Created: 2025-01-10 (8 days ago)                │
│ Health: Blocked                                 │
│ Blocker: 2 security concerns                    │
│ Next: Schedule security review                  │
│ Files: .prisma/projeto/especificacoes/payment-gateway/           │
└─────────────────────────────────────────────────┘

Summary:
- Total: 3 especificações
- Active: 2 in progress
- Blocked: 1 needs attention
- Average Progress: 50%

Quick Actions:
1. Continue export-markdown: /executar-tarefas export-markdown
2. Unblock auth-integration: /atualizar-especificacao auth-integration design
3. Review payment-gateway: /analisar-riscos payment-gateway security

What would you like to do?
```

## Compact View

```
User: /listar-especificacoes active
Assistant: 📋 Especificações Ativas (2)

🟢 export-markdown         [██████████████████░░] 75%  ⚙️  Healthy
🟡 auth-integration        [█████████░░░░░░░░░░░] 45%  🎨  Warning

Use /status-especificacao [name] for details
```

## Table View

```
┌──────────────────┬─────────┬────────────────┬──────────┬────────────┐
│ Feature          │ Phase   │ Progress       │ Health   │ Next       │
├──────────────────┼─────────┼────────────────┼──────────┼────────────┤
│ export-markdown  │ Impl    │ ████████░░ 75% │ 🟢        │ Task 2.3   │
│ auth-integration │ Design  │ █████░░░░░ 45% │ 🟡        │ OAuth      │
│ payment-gateway  │ Req     │ ███░░░░░░░ 30% │ 🔴        │ Security   │
└──────────────────┴─────────┴────────────────┴──────────┴────────────┘
```

## Integration Points

- Dashboard view para gerenciar múltiplas especificações
- Identifica especificações que precisam atenção
- Sugere próximas ações automaticamente
- Links para comandos relevantes

## Related Commands

- `/status-especificacao` - Detalhes de especificação específica
- `/nova-especificacao` - Criar nova especificação
- `/executar-tarefas` - Executar tarefas de especificação
- `/atualizar-especificacao` - Atualizar especificação existente
