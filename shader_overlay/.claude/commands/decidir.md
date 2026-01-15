# Command: /make-decision

## Description

Cria Architecture Decision Record (ADR) usando agente decisor para documentar decisões técnicas importantes.

## Usage

```
/make-decision [feature-name] [decision-context]
```

## Parameters

- `feature-name` (opcional): Nome da feature relacionada (kebab-case)
- `decision-context` (opcional): Contexto da decisão (será solicitado se não fornecido)

## What It Does

1. Coleta contexto da decisão
2. Identifica opções e trade-offs
3. Analisa impacto técnico e de negócio
4. Chama agente decisor para criar ADR
5. Documenta decisão em formato estruturado
6. Atualiza especificações relacionadas com referências

## ADR Structure

- **Status**: Proposed | Accepted | Deprecated | Superseded
- **Context**: Situação que requer decisão
- **Decision**: O que foi decidido
- **Options Considered**: Alternativas avaliadas
- **Consequences**: Impactos positivos e negativos
- **Trade-offs**: Análise de compromissos

## When to Create ADR

- Mudanças arquiteturais significativas
- Escolha de tecnologias ou frameworks
- Padrões de design importantes
- Trade-offs entre qualidade/performance/complexidade
- Decisões que afetam múltiplas features

## Examples

```bash
# Criar ADR interativo
/make-decision

# ADR para feature específica
/make-decision export-markdown

# ADR com contexto inicial
/make-decision export-markdown "escolha de template engine"
```

## Expected Flow

```
User: /make-decision export-markdown
Assistant: Vou ajudar a criar um ADR para 'export-markdown'.

Qual é a decisão que precisa ser documentada?

User: Decidir se implementamos export framework genérico agora ou entregamos MVP de markdown primeiro/usr/bin/bash: line 1: type: .claude\commands\make-decision-continuation.txt: not found

Assistant: Ótimo, vou criar um ADR para essa decisão estratégica.

🔍 Analisando contexto...
- Feature atual: export-markdown (75% complete)
- Decisão: MVP vs Framework approach
- Impacto: Arquitetura de longo prazo

📋 Coletando informações:
1. Opções identificadas: 2
2. Trade-offs: MVP (speed) vs Framework (reusability)
3. Stakeholders: Dev team, Product, Architecture

🎯 Chamando agente decisor...

[Agente cria ADR estruturado]

═══════════════════════════════════════════════════
📄 ADR-001: Export Framework vs Markdown MVP
═══════════════════════════════════════════════════

Status: 🟡 Proposed (awaiting decision)
Date: 2025-01-18
Deciders: [To be filled]
Feature: export-markdown

───────────────────────────────────────────────────
📋 CONTEXT
───────────────────────────────────────────────────

Current Situation:
- Implementing markdown export feature
- 75% complete with current approach
- Audit identified strategic opportunity for framework

Question:
Should we:
A) Continue with markdown-specific MVP and ship quickly
B) Pivot to generic export framework architecture

Triggers:
- Code audit (agente auditor) identified macro opportunity
- Template abstraction already suggested (MI-2)
- Future roadmap includes PDF, JSON exports

───────────────────────────────────────────────────
🎯 DECISION
───────────────────────────────────────────────────

[To be decided - options presented below]

───────────────────────────────────────────────────
📊 OPTIONS CONSIDERED
───────────────────────────────────────────────────

Option A: Ship Markdown MVP First
──────────────────────────────────

Description:
- Complete current markdown implementation
- Ship as standalone feature
- Refactor to framework later if needed

Pros:
✅ Fast time-to-market (1 day remaining)
✅ Lower immediate risk
✅ Delivers user value quickly
✅ Validates export demand
✅ Current code 75% done

Cons:
❌ Technical debt if we refactor later
❌ 60% more effort for future exports
❌ Missed opportunity for differentiation
❌ May require breaking changes later
❌ Template coupling remains (MI-2)

Effort: 6h remaining
Risk: Low
Time-to-Market: 1 day
Future Flexibility: Medium

Option B: Pivot to Export Framework
────────────────────────────────────

Description:
- Extract generic IExporter interface
- Refactor markdown as first plugin
- Create plugin architecture
- Add documentation for extensibility

Pros:
✅ Platform capability (not just feature)
✅ Future exports 60% faster to build
✅3rd-party ecosystem potential
✅ Product differentiation
✅ Cleaner architecture long-term
✅ Template abstraction included

Cons:
❌ Delays markdown release 5 days
❌ Higher complexity
❌ More testing required
❌ Over-engineering risk if no demand
❌ Throws away 20% of current work

Effort: 40h total (34h additional)
Risk: Medium
Time-to-Market: 6 days
Future Flexibility: Very High

Option C: Hybrid Approach
─────────────────────────

Description:
- Ship markdown MVP as planned (1 day)
- Design framework API in parallel
- Refactor to framework in next sprint
- Avoid breaking changes via careful API design

Pros:
✅ Fast initial delivery
✅ Validates demand first
✅ Framework architecture planned
✅ Lower risk of over-engineering
✅ Can recruit early adopters

Cons:
❌ Two rounds of changes
❌ Framework design may miss learnings
❌ Some rework inevitable
⚠️  Requires disciplined API design now

Effort: 6h + 30h (spread over time)
Risk: Medium
Time-to-Market: 1 day (MVP), 2 weeks (framework)
Future Flexibility: High

───────────────────────────────────────────────────
⚖️  TRADE-OFFS ANALYSIS
───────────────────────────────────────────────────

Speed vs Flexibility:
- A: Fast now, slower later
- B: Slow now, fast later
- C: Fast now, moderate cost later

Risk vs Reward:
- A: Low risk, moderate reward
- B: Medium risk, high reward
- C: Medium risk, high reward with validation

Technical Debt:
- A: Incurs debt if demand exists
- B: No debt, but upfront investment
- C: Minimal debt if API designed well

Product Strategy:
- A: Feature-first (tactical)
- B: Platform-first (strategic)
- C: Iterate to platform (lean)

───────────────────────────────────────────────────
📊 IMPACT ANALYSIS
───────────────────────────────────────────────────

                    │ Option A │ Option B │ Option C
────────────────────┼──────────┼──────────┼─────────
Time to MVP         │ 1 day ✅  │ 6 days ❌ │ 1 day ✅
Future Dev Speed    │ 5/10     │ 10/10 ✅  │ 9/10
Architecture        │ 6/10     │ 10/10 ✅  │ 8/10
Product Diff.       │ 5/10     │ 10/10 ✅  │ 9/10
Technical Risk      │ Low ✅    │ Med      │ Med
Business Risk       │ Low ✅    │ Med      │ Low ✅
Ecosystem Potential │ 0/10     │ 10/10 ✅  │ 8/10
Total Effort        │ 6h ✅     │ 40h      │ 36h

───────────────────────────────────────────────────
💡 RECOMMENDATION
───────────────────────────────────────────────────

Recommended: Option C (Hybrid Approach)

Rationale:
1. Delivers user value fastest (1 day)
2. Validates export demand with real users
3. Framework design informed by real usage
4. Lower risk of over-engineering
5. Good balance of speed and flexibility

Implementation Plan:
───────────────────

Phase 1 (This Sprint - 1 day):
- ✅ Ship markdown MVP
- ⚠️  Design IExporter API carefully (avoid breaking changes)
- 📝 Document framework intention in ADR

Phase 2 (Next Sprint - 2 weeks):
- 🔧 Extract IExporter interface
- 🔧 Refactor markdown as plugin
- 🔧 Add plugin registry
- 📚 Document plugin development

Phase 3 (Later - as needed):
- ➕ Add PDF exporter plugin
- ➕ Add JSON exporter plugin
- 🌍 Open 3rd-party plugin ecosystem

Success Criteria:
- Phase 1: Markdown export live in production
- Phase 1: >10 users actively using export
- Phase 2: Framework allows new format in <4h
- Phase 3: At least 1 community plugin created

───────────────────────────────────────────────────
🎯 DECISION REQUIRED
───────────────────────────────────────────────────

Please choose:
A) Ship Markdown MVP (Option A)
B) Pivot to Framework (Option B)
C) Hybrid Approach (Option C) [Recommended]

Or provide alternative approach.

───────────────────────────────────────────────────
📎 REFERENCES
───────────────────────────────────────────────────

- Audit Report: .prisma/projeto/especificacoes/export-markdown/audit-report.md
- Current Design: .prisma/projeto/especificacoes/export-markdown/design.md
- Micro-improvement MI-2: Extract template interface

═══════════════════════════════════════════════════

Your decision? (A/B/C or describe alternative)
```

## Related Commands

- `/auditar-especificacao` - Often triggers need for ADR
- `/analisar-riscos` - Informs decision analysis
- `/status-especificacao` - Context for decision timing
- `/executar-tarefas` - Implements decided approach
