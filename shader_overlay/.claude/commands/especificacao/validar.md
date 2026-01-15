# Command: /validar-especificacao

## Description

Valida conformidade de especificações e implementação com regras, padrões e convenções usando o agente conformista.

## Usage

```
/validar-especificacao [nome-feature] [tipo-validacao]
```

## Parameters

- `nome-feature` (opcional): Nome da feature (kebab-case). Se não fornecido, valida última feature
- `tipo-validacao` (opcional): Tipo de validação
  - `completa` (padrão): Validação completa (docs + code + patterns)
  - `docs`: Apenas documentos de especificação (requirements, design, tasks)
  - `codigo`: Apenas código implementado
  - `padroes`: Apenas padrões e convenções
  - `nomenclatura`: Apenas convenções de nomenclatura

## What It Does

1. Lê documentos de especificação (.prisma/projeto/especificacoes/{nome-feature}/)
2. Analisa código implementado (se tipo-validacao incluir codigo)
3. Verifica contra:
   - Regras definidas em configurações
   - Padrões de arquitetura estabelecidos
   - Convenções de nomenclatura
   - Estrutura de diretórios esperada
   - Templates e formato de documentos
4. Gera relatório de conformidade
5. Identifica violações e sugere correções

## Validation Checks

### Documentation Compliance

- Formato EARS nos requirements
- Estrutura de seções conforme template
- Diagramas Mermaid válidos
- Cross-references corretos
- Metadata completo

### Code Compliance

- Arquitetura hexagonal seguida
- Naming conventions (kebab-case, camelCase, PascalCase)
- File structure conforme design
- Imports organizados
- Error handling patterns

### Process Compliance

- Workflow steps seguidos em ordem
- Aprovações documentadas
- Quality gates passados
- Testing strategy implementada

## Examples

```bash
# Validação completa
/validar-especificacao export-markdown

# Valida apenas documentos
/validar-especificacao export-markdown docs

# Valida apenas código
/validar-especificacao export-markdown codigo

# Valida padrões e convenções
/validar-especificacao export-markdown padroes
```

## Expected Flow

```
User: /validar-especificacao export-markdown
Assistant: Validando conformidade da especificação 'export-markdown'...

Documentos Encontrados:
- requirements.md (valid EARS format)
- design.md (complete sections)
- tasks.md (valid structure)

Executando agente conformista...

[Agente valida contra regras e padrões]

Relatório de Conformidade:

Documentation: 98%
  - EARS format correct
  - All sections present
  - 1 minor: Missing performance requirements

Code Structure: 95%
  - Hexagonal architecture followed
  - Naming conventions correct
  - 1 minor: Some files missing JSDoc

Process Compliance: 100%
  - All workflow steps documented
  - Quality gates passed
  - Approvals recorded

Violations:
1. [MINOR] requirements.md: Add performance requirement for export size
2. [MINOR] src/export/formatter.ts: Add JSDoc comments

Overall Score: 97.5% - Compliant

Deseja ver correções sugeridas? (sim/não)
```

## Compliance Scoring

- 95-100%: Compliant (proceed)
- 85-94%: Minor issues (fix recommended)
- 70-84%: Non-compliant (must fix)
- <70%: Critical (block progress)

## Integration Points

- Chamado automaticamente antes de revisar-implementacao
- Pode triggerar agente arquiteto para correções
- Bloqueia workflow se score < 70%
- Gera relatório em `.prisma/projeto/especificacoes/{nome-feature}/compliance-report.md`

## Related Commands

- `/revisar-implementacao` - Revisa código implementado
- `/analisar-riscos` - Análise de riscos
- `/auditar-especificacao` - Auditoria profunda
