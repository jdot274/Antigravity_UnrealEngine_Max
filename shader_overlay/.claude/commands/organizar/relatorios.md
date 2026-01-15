# Comando: /organizar-relatorios

## Propósito
Organizar automaticamente relatórios em `.prisma/relatorios/` categorizando por tipo e renomeando para kebab-case.

## Sintaxe
```
/organizar-relatorios [--dry-run]
```

## Parâmetros

### Opcionais
- `--dry-run`: Mostra o que seria feito sem aplicar mudanças

## Descrição

Este comando organiza relatórios soltos na raiz de `.prisma/relatorios/` movendo-os para subcategorias apropriadas e renomeando para kebab-case.

### Categorias Automáticas

O sistema identifica automaticamente a categoria baseado em palavras-chave:

| Categoria | Palavras-chave | Descrição |
|-----------|----------------|-----------|
| **execucao** | execucao, execution, task, completion | Relatórios de execução de tarefas |
| **auditoria** | auditoria, audit, scan, analysis, structure | Auditorias e análises estruturais |
| **correcoes** | fix, cleanup, correcoes, correction, removal | Correções e limpezas |
| **seguranca** | security, seguranca, auth, authentication | Segurança e autenticação |
| **revisao-codigo** | review, revisao, code-review | Revisões técnicas |
| **hydration** | hydration, html, nesting | Problemas de hydration React/Next.js |
| **agent-reports** | agent, autonomous, multi-agent | Execuções de agentes |
| **sumarios** | summary, sumario, resumo, executivo, status | Sumários executivos |
| **outros** | - | Não categorizados |

### Conversão para Kebab-Case

O comando automaticamente converte nomes de arquivo para kebab-case:

**Exemplos:**
- `AGENT-5-ENV-CLEANUP-REPORT.md` → `agent-5-env-cleanup-report.md`
- `AUTH-CLEANUP-EXECUTIVE-SUMMARY.md` → `auth-cleanup-executive-summary.md`
- `AUDITORIA-INDEX.md` → `auditoria-index.md`
- `execucao-tasks-35-40-2025-01-15.md` → `execucao-tasks-35-40-2025-01-15.md` ✓ (já correto)

**Regras:**
- Tudo em minúsculas
- Hífens como separadores
- Datas ISO preservadas (YYYY-MM-DD)
- Múltiplos hífens reduzidos a um único

### READMEs Automáticos

O comando gera/atualiza automaticamente:
- **README principal** em `.prisma/relatorios/README.md` com visão geral
- **README por categoria** listando todos os relatórios da categoria

## Uso

### Modo Dry-Run (Teste)
```bash
npm run organizar-relatorios:dry
```

**Output:**
```
🗂️  Organizando relatórios em .prisma/relatorios/

⚠️  MODO DRY-RUN (nenhuma alteração será feita)

[DRY-RUN] AGENT-5-ENV-CLEANUP-REPORT.md
  → correcoes/agent-5-env-cleanup-report.md

[DRY-RUN] AUTH-CLEANUP-EXECUTIVE-SUMMARY.md
  → correcoes/auth-cleanup-executive-summary.md

...

📊 Estatísticas:
  correcoes: 12 relatórios
  auditoria: 10 relatórios
  ...
```

### Modo Real (Aplicar)
```bash
npm run organizar-relatorios
```

**Output:**
```
🗂️  Organizando relatórios em .prisma/relatorios/

✅ AGENT-5-ENV-CLEANUP-REPORT.md
  → correcoes/agent-5-env-cleanup-report.md

✅ AUTH-CLEANUP-EXECUTIVE-SUMMARY.md
  → correcoes/auth-cleanup-executive-summary.md

...

📚 Criando READMEs por categoria...

📄 README criado: correcoes/README.md
📄 README criado: auditoria/README.md
...

📝 README principal atualizado

✅ Organização concluída com sucesso!
```

## Exemplos

### Exemplo 1: Teste antes de aplicar
```bash
# Testar organização sem modificar nada
npm run organizar-relatorios:dry
```

### Exemplo 2: Organizar novos relatórios
```bash
# Criar novo relatório na raiz
echo "# Relatório" > .prisma/relatorios/NOVO-RELATORIO-AUDIT.md

# Organizar automaticamente
npm run organizar-relatorios

# Resultado: movido para auditoria/novo-relatorio-audit.md
```

### Exemplo 3: Verificar estrutura
```bash
# Após organizar, ver estrutura
ls -R .prisma/relatorios/

# Ou ver README
cat .prisma/relatorios/README.md
```

## Estrutura Criada

```
.prisma/relatorios/
├── README.md                    # Índice principal
├── agent-reports/               # Execuções de agentes
│   ├── README.md
│   └── *.md
├── auditoria/                   # Auditorias estruturais
│   ├── README.md
│   └── *.md
├── correcoes/                   # Correções e limpezas
│   ├── README.md
│   └── *.md
├── execucao/                    # Execuções de tarefas
│   ├── README.md
│   └── *.md
├── hydration/                   # Problemas de hydration
│   ├── README.md
│   └── *.md
├── outros/                      # Não categorizados
│   ├── README.md
│   └── *.md
├── revisao-codigo/              # Revisões técnicas
│   ├── README.md
│   └── *.md
├── seguranca/                   # Segurança e auth
│   ├── README.md
│   └── *.md
└── sumarios/                    # Sumários executivos
    ├── README.md
    └── *.md
```

## Comportamento

### Detecção de Relatórios
O comando procura por arquivos `.md` na raiz de `.prisma/relatorios/` (não em subdiretórios).

### Categorização
1. Analisa nome do arquivo
2. Busca palavras-chave conhecidas
3. Atribui categoria baseado na primeira correspondência
4. Se nenhuma correspondência, move para `outros/`

### Renomeação
1. Detecta se já está em kebab-case
2. Se sim, mantém o nome
3. Se não, converte aplicando regras

### Colisão de Nomes
Se destino já existe, arquivo é pulado com warning:
```
⚠️  SKIP: RELATORIO.md (destino já existe)
```

### READMEs
- Sempre atualizados após organização
- Lista todos os relatórios da categoria
- Inclui links diretos
- Mostra contagem total

## Quando Usar

✅ **Use este comando quando:**
- Novos relatórios foram criados na raiz
- Nomes de arquivos estão inconsistentes
- Estrutura ficou desorganizada
- Após merge de branches com novos relatórios
- Periodicamente para manutenção

❌ **NÃO use este comando quando:**
- Arquivos já estão organizados
- Você quer mover manualmente para categoria específica
- Relatórios têm nomes customizados que não devem mudar

## Script Relacionado

**Localização:** `scripts/organizar-relatorios.ts`

**Funcionalidades:**
- Categorização automática
- Conversão kebab-case
- Geração de READMEs
- Modo dry-run
- Estatísticas de organização

## Integração com Agentes

### Agentes que Devem Usar

1. **Implementador**: Após criar novos relatórios
2. **Auditor**: Ao detectar relatórios desorganizados
3. **Conformista**: Validação de estrutura

### Recomendação

Agentes devem executar `npm run organizar-relatorios` após criar novos relatórios na raiz de `.prisma/relatorios/`.

**Exemplo no fluxo:**
```markdown
1. Criar relatório: `.prisma/relatorios/NOVO-AUDIT-REPORT.md`
2. Executar: `npm run organizar-relatorios`
3. Resultado: `.prisma/relatorios/auditoria/novo-audit-report.md`
```

## Customização

### Adicionar Nova Categoria

Edite `scripts/organizar-relatorios.ts`:

```typescript
const CATEGORIAS = {
  // ... categorias existentes
  'nova-categoria': ['palavra-chave-1', 'palavra-chave-2']
};
```

### Alterar Descrição de Categoria

Edite o objeto `descricoes` em `criarReadmeCategoria()`:

```typescript
const descricoes: Record<string, string> = {
  // ... descrições existentes
  'nova-categoria': 'Descrição da nova categoria'
};
```

## Troubleshooting

### Problema: Arquivo não foi categorizado corretamente

**Solução:**
1. Verifique palavras-chave em `CATEGORIAS`
2. Adicione palavra-chave relevante
3. Re-execute o comando

### Problema: Nome convertido incorretamente

**Solução:**
1. Verifique função `toKebabCase()` em `scripts/organizar-relatorios.ts`
2. Ajuste regex se necessário
3. Ou renomeie manualmente após organização

### Problema: README não atualizado

**Solução:**
1. Execute comando novamente (READMEs são sempre regenerados)
2. Ou delete README e re-execute

## Histórico

| Data | Versão | Mudança |
|------|--------|---------|
| 2025-01-15 | 1.0 | Criação inicial do comando |

## Referências

- **Script:** `scripts/organizar-relatorios.ts`
- **README Principal:** `.prisma/relatorios/README.md`
- **Relatório de Implementação:** `.prisma/relatorios/execucao/organizacao-relatorios-2025-01-15.md`

## Notas

- ✅ Comando é idempotente (pode ser executado múltiplas vezes)
- ✅ Sempre use dry-run primeiro para validar
- ✅ READMEs são regenerados automaticamente
- ✅ Datas ISO (YYYY-MM-DD) são preservadas
- ✅ Arquivos já organizados não são movidos novamente

---

**Criado:** 2025-01-15
**Status:** ✅ Ativo
**Manutenção:** Automática
