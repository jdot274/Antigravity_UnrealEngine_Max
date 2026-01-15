# Command: /execute-tests

## Description

Executa testes de uma feature usando spec-test agent, garantindo qualidade e conformidade com requirements.

## Usage

```
/execute-tests [feature-name] [test-scope]
```

## Parameters

- `feature-name` (opcional): Nome da feature (kebab-case). Se não fornecido, testa última feature
- `test-scope` (opcional): Escopo dos testes
  - `all` (padrão): Todos os testes (unit + integration + e2e)
  - `unit`: Apenas testes unitários
  - `integration`: Apenas testes de integração
  - `e2e`: Apenas testes end-to-end
  - `coverage`: Análise de cobertura detalhada

## What It Does

1. Lê requirements e design da feature
2. Identifica código implementado
3. Chama agente testador-specs para criar/executar testes
4. Verifica cobertura de testes
5. Valida conformidade com requirements
6. Gera relatório de testes

## Test Strategy

- **Unit Tests**: Testa componentes isolados
- **Integration Tests**: Testa integração entre componentes
- **E2E Tests**: Testa fluxos completos de usuário
- **Coverage Target**: 80%+ line coverage

## Examples

```bash
# Executar todos os testes
/execute-tests export-markdown

# Apenas testes unitários
/execute-tests export-markdown unit

# Análise de cobertura
/execute-tests export-markdown coverage

# Executar testes de todas features
/execute-tests all
```

## Expected Flow

```
User: /execute-tests export-markdown
Assistant: Executando testes para 'export-markdown'...

📋 Contexto:
- Feature: export-markdown
- Requirements: 12 (8 functional, 4 non-functional)
- Implementação: 100% completa

🔍 Chamando agente testador-specs...

[Agente cria e executa testes]

═══════════════════════════════════════════════════
🧪 Relatório de Testes: export-markdown
═══════════════════════════════════════════════════

✅ Test Execution Summary
─────────────────────────

Total Tests: 47
✅ Passed: 46 (97.9%)
❌ Failed: 1 (2.1%)
⏭️  Skipped: 0

Execution Time: 4.2s

✅ Unit Tests (32 tests)
─────────────────────────
✅ 31 passed
❌ 1 failed
⏱️  2.1s

Suites:
✅ TemplateEngine (8/8 passed)
✅ MarkdownFormatter (10/10 passed)
❌ ExportService (13/14 passed) - 1 failure
✅ DataModels (1/1 passed)

Failures:
1. ExportService › should handle large workflows
   Expected: < 3s
   Actual: 3.8s
   File: src/export/service.test.ts:45

✅ Integration Tests (12 tests)
───────────────────────────────
✅ 12 passed
⏱️  1.8s

Suites:
✅ Export Pipeline (5/5 passed)
✅ Template Integration (4/4 passed)
✅ File System Integration (3/3 passed)

✅ E2E Tests (3 tests)
──────────────────────
✅ 3 passed
⏱️  0.3s

Scenarios:
✅ Complete export workflow
✅ Custom template usage
✅ Error handling

📊 Coverage Report
──────────────────

Overall Coverage: 82.5% ✅ (target: 80%)

File Coverage:
  src/export/
    ✅ TemplateEngine.ts     95% ██████████████████▌░
    ✅ MarkdownFormatter.ts  88% █████████████████▌░░
    ✅ ExportService.ts      78% ███████████████▌░░░░
    ✅ DataModels.ts         100% ████████████████████

  src/templates/
    ✅ DefaultTemplate.ts    90% ██████████████████░░
    ⚠️  CustomTemplate.ts    65% █████████████░░░░░░░

Uncovered Lines:
- src/export/ExportService.ts: 67-72 (error handling)
- src/templates/CustomTemplate.ts: 45-55 (edge cases)

📋 Requirements Coverage
────────────────────────

Functional Requirements (8):
✅ REQ-001: Export workflow to markdown ✓
✅ REQ-002: Support custom templates ✓
✅ REQ-003: Handle large workflows ⚠️ (performance issue)
✅ REQ-004: Preserve structure ✓
✅ REQ-005: Generate table of contents ✓
✅ REQ-006: Include metadata ✓
✅ REQ-007: Error handling ✓
✅ REQ-008: Progress reporting ✓

Non-Functional Requirements (4):
⚠️  NFR-001: Performance <3s (3.8s measured)
✅ NFR-002: Memory efficient ✓
✅ NFR-003: Extensible design ✓
✅ NFR-004: User-friendly errors ✓

Requirements Coverage: 11/12 ✅ (91.7%)

🎯 Issues Found
───────────────

🔴 Critical (0):
(nenhum)

🟡 Medium (2):
1. Performance: Large workflow export takes 3.8s (target: <3s)
   Location: src/export/ExportService.ts:123
   Requirement: NFR-001
   Suggestion: Implement streaming or optimize template rendering

2. Coverage: CustomTemplate edge cases not covered (65%)
   Location: src/templates/CustomTemplate.ts:45-55
   Suggestion: Add tests for malformed templates

🟢 Low (1):
1. Error handling paths not fully covered (src/export/ExportService.ts:67-72)

═══════════════════════════════════════════════════
✅ Test Results: PASS (with warnings)
═══════════════════════════════════════════════════

Overall Status: ⚠️ PASS with Performance Warning

Quality Gates:
✅ All critical tests pass
✅ Coverage ≥ 80% (82.5%)
⚠️  Performance requirement not met (3.8s vs <3s target)
✅ Requirements coverage ≥ 80% (91.7%)

Blockers: None critical
Recommendations:
1. Fix performance issue (Medium priority)
2. Add CustomTemplate edge case tests
3. Improve error handling coverage

Ready for code-review? (sim/não)
```

## Test Report Files

- Test results: `.prisma/projeto/especificacoes/{feature-name}/test-report.md`
- Coverage: `.prisma/projeto/especificacoes/{feature-name}/coverage-report.html`
- Failed tests: `.prisma/projeto/especificacoes/{feature-name}/test-failures.log`

## Quality Gates

Para passar nos quality gates:

- ✅ All critical tests must pass
- ✅ Coverage ≥ 80%
- ✅ Requirements coverage ≥ 80%
- ✅ No critical performance regressions

## Integration Points

- Executado automaticamente após implementação
- Bloqueia workflow se testes críticos falharem
- Triggera code-review após testes passarem
- Atualiza status em tasks.md

## Related Commands

- `/revisar-implementacao` - Próximo passo após testes
- `/executar-tarefas` - Implementa código testado
- `/validar-spec` - Valida conformidade
- `/analisar-riscos` - Analisa riscos se testes falharem
