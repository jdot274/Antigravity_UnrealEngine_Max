# Command: /review-implementation

## Description

Executa revisão profissional do código implementado usando o agente revisor.

## Usage

```
/review-implementation [feature-name] [scope]
```

## Parameters

- `feature-name` (opcional): Nome da feature (kebab-case). Se não fornecido, revisa última feature
- `scope` (opcional): Escopo da revisão
  - `full` (padrão): Revisão completa de qualidade, segurança e performance
  - `quality`: Foco em qualidade de código
  - `security`: Foco em segurança
  - `performance`: Foco em performance
  - `standards`: Foco em padrões estabelecidos

## What It Does

1. Identifica arquivos implementados da feature
2. Lê tasks.md para entender contexto
3. Chama agente revisor com escopo apropriado
4. Gera relatório de revisão
5. Identifica issues críticos e sugestões

## Quality Gates

- ✅ Code Quality Score ≥ 7/10
- ✅ Security Issues = 0 (critical/high)
- ✅ Performance Issues = 0 (critical)
- ✅ Standards Compliance ≥ 90%

## Examples

```bash
# Revisão completa da última feature
/review-implementation

# Revisão de feature específica
/review-implementation export-markdown

# Revisão focada em segurança
/review-implementation export-markdown security

# Revisão de padrões
/review-implementation export-markdown standards
```

## Expected Flow

```
User: /review-implementation export-markdown
Assistant: Iniciando revisão de código para feature 'export-markdown'...

📋 Contexto da Feature:
- Tasks implementadas: 8/10
- Arquivos modificados: 12
- Linhas adicionadas: +842 / -156

🔍 Executando agente revisor...

[Agente analisa código]

📊 Relatório de Revisão:

Quality Score: 8.5/10 ✅
Security Issues: 0 critical ✅
Performance Issues: 1 minor ⚠️
Standards Compliance: 95% ✅

🎯 Issues Identificados:
1. [MINOR] Performance: Consider caching markdown templates
2. [INFO] Suggestion: Add JSDoc comments to public APIs

✅ Aprovado para próxima fase (testes)

Deseja ver detalhes completos? (sim/não)
```

## Integration Points

- Chamado automaticamente após implementação de tasks
- Integrado com conformista para validação de padrões
- Pode triggerar avaliador-riscos se issues críticos encontrados
- Gera relatório em `.prisma/projeto/especificacoes/{feature-name}/relatorio-revisao-codigo.md`

## Related Commands

- `/validar-especificacao` - Valida conformidade com specs
- `/analisar-riscos` - Análise de riscos técnicos
- `/executar-testes` - Executa testes após revisão
