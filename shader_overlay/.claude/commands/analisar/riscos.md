# Command: /analyze-risks

## Description

Executa análise profunda de riscos técnicos, arquiteturais e de negócio usando avaliador-riscos agent.

## Usage

```
/analyze-risks [feature-name] [risk-category] [depth]
```

## Parameters

- `feature-name` (opcional): Nome da feature (kebab-case). Se não fornecido, analisa última feature
- `risk-category` (opcional): Categoria de risco
  - `all` (padrão): Análise completa de todos os riscos
  - `technical`: Riscos técnicos (performance, escalabilidade, débito técnico)
  - `security`: Riscos de segurança e vulnerabilidades
  - `architectural`: Riscos arquiteturais e design
  - `business`: Riscos de negócio e impacto
  - `operational`: Riscos operacionais (deploy, manutenção)
- `depth` (opcional): Profundidade da análise
  - `quick`: Análise rápida (5-10 min)
  - `standard` (padrão): Análise padrão (15-20 min)
  - `deep`: Análise profunda (30+ min)

## What It Does

1. Lê especificação completa (requisitos, design, tarefas)
2. Analisa código implementado (se existir)
3. Identifica riscos em:
   - **Técnicos**: Performance, escalabilidade, débito técnico
   - **Segurança**: Vulnerabilidades, exposições, data leaks
   - **Arquitetura**: Pontos de falha, coupling, complexity
   - **Negócio**: Impacto, viabilidade, ROI
   - **Operacional**: Deploy, rollback, monitoramento
4. Classifica riscos por severidade (Critical, High, Medium, Low)
5. Sugere estratégias de mitigação
6. Calcula risk score geral

## Risk Classification

### Severity Levels

- 🔴 **Critical** (9-10): Blocker, deve ser resolvido antes de prosseguir
- 🟠 **High** (7-8): Alto impacto, deve ser mitigado
- 🟡 **Medium** (4-6): Impacto moderado, mitigar se possível
- 🟢 **Low** (1-3): Baixo impacto, pode ser aceito

### Risk Dimensions

- **Likelihood**: Probabilidade de ocorrer (1-10)
- **Impact**: Impacto se ocorrer (1-10)
- **Risk Score**: Likelihood × Impact

## Examples

```bash
# Análise completa de riscos
/analyze-risks export-markdown

# Análise focada em segurança
/analyze-risks export-markdown security

# Análise técnica profunda
/analyze-risks export-markdown technical deep

# Análise rápida antes de decisão
/analyze-risks export-markdown all quick
```

## Expected Flow

```
User: /analyze-risks export-markdown
Assistant: Analisando riscos da feature 'export-markdown'...

📋 Contexto:
- Fase: Implementation (70% complete)
- Complexidade: Medium
- Dependências: 3 packages externos

🔍 Executando avaliador-riscos agent...

[Agente analisa riscos profundamente]

📊 Relatório de Análise de Riscos:

Overall Risk Score: 6.2/10 🟡 Medium Risk

🔴 Critical Risks (0):
(nenhum)

🟠 High Risks (2):
1. [H1] Security: Markdown rendering pode permitir XSS
   - Likelihood: 7/10
   - Impact: 8/10
   - Score: 56/100
   - Mitigation: Use sanitização com DOMPurify ou marked + sanitize

2. [H2] Performance: Export de workflows grandes (>10MB) pode travar
   - Likelihood: 6/10
   - Impact: 7/10
   - Score: 42/100
   - Mitigation: Implementar streaming ou chunking

🟡 Medium Risks (3):
1. [M1] Technical Debt: Template engine adiciona 150KB ao bundle
2. [M2] Operational: Rollback pode corromper exports parciais
3. [M3] Architectural: Tight coupling com formato Markdown

🟢 Low Risks (2):
1. [L1] Business: Baixa adoção inicial esperada
2. [L2] Maintenance: Documentação pode ficar desatualizada

📈 Risk Trends:
- Security risks aumentaram com adição de custom templates
- Performance risks estáveis
- Architectural risks diminuíram após refactoring

🎯 Recomendações Prioritárias:
1. [URGENT] Implementar sanitização XSS antes de release
2. [HIGH] Adicionar testes de performance para exports grandes
3. [MEDIUM] Documentar strategy de rollback

Deseja ver plano detalhado de mitigação? (sim/não)
```

## Risk Matrix

```
Impact
 10│         │         │    H2   │   H1 🔴
  9│         │         │         │
  8│         │         │    M3   │
  7│         │    M1   │    M2   │
  6│         │         │         │
  5│    L2   │         │         │
  4│         │         │         │
  3│    L1   │         │         │
  2│         │         │         │
  1│         │         │         │
   └─────────┴─────────┴─────────┴─────────
   1    2    3    4    5    6    7    8    9   10
                    Likelihood
```

## Integration Points

- Chamado proativamente em decisões críticas
- Triggera decisor para ADRs se necessário
- Bloqueia workflow se Critical risks não mitigados
- Atualiza risk register em `.prisma/projeto/especificacoes/{feature-name}/risk-register.md`

## Decision Triggers

Recomenda chamar decisor se:

- ≥1 Critical risk identificado
- ≥3 High risks relacionados
- Risk score geral > 7.0
- Arquitetura tem múltiplos pontos de falha

## Related Commands

- `/validar-spec` - Valida conformidade
- `/revisar-implementacao` - Revisa código
- `/tomar-decisao` - Cria ADR para decisão
- `/auditar-spec` - Auditoria profunda
