# Comando: /prisma:iniciar

## Descrição

Inicializa o sistema Prisma e carrega o agente orquestrador principal para gerenciar workflow completo de especificações.

## Uso

```bash
/prisma:iniciar [feature-name]
```

## Parâmetros

- `feature-name` (opcional): Nome da feature em kebab-case
  - Se fornecido: Inicia workflow para essa feature específica
  - Se omitido: Modo interativo, pergunta o que usuário quer fazer

## O Que Este Comando Faz

1. **Carrega System Prompt**: Lê `.prisma/prompts/prisma-system.md`
2. **Invoca Agente Orquestrador**: Chama agente `prisma` (`.prisma/agentes/prisma.md`)
3. **Inicializa Workflow**: Prepara estrutura para nova feature ou continua existente
4. **Apresenta Opções**: Mostra menu de ações disponíveis

## Quando Usar

### Use Este Comando Quando:

✅ **Iniciar nova feature**
```bash
/prisma:iniciar payment-api
```

✅ **Primeiro contato com Prisma**
```bash
/prisma:iniciar
# Sistema perguntará o que você quer fazer
```

✅ **Retomar workflow interrompido**
```bash
/prisma:iniciar user-authentication
# Detecta estado atual e oferece continuar
```

✅ **Não sabe qual agente usar**
```bash
/prisma:iniciar
# Orquestrador te guiará
```

### NÃO Use Este Comando Quando:

❌ **Quer apenas criar requisitos**: Use `/prisma:especificacao-nova` ou chame `analista` diretamente

❌ **Já está no meio de workflow**: Continue usando comandos específicos da fase

❌ **Apenas quer consultar specs**: Use `/prisma:especificacao-listar` ou `/prisma:especificacao-status`

## Fluxo de Execução

### Cenário 1: Nova Feature

```yaml
User: /prisma:iniciar payment-gateway

System:
  1. Carrega agente prisma
  2. Verifica se .prisma/projeto/especificacoes/payment-gateway/ existe
  3. Se não existe: Oferece criar nova especificação
  4. Se existe: Mostra status atual e oferece continuar

Prisma:
  "🚀 Iniciando Prisma para feature: payment-gateway

  📁 Criando estrutura:
     .prisma/projeto/especificacoes/payment-gateway/
     ├── requirements.md (pendente)
     ├── design.md (pendente)
     ├── tasks.md (pendente)
     ├── artifacts/
     ├── decisions/
     └── reports/

  📋 Workflow Prisma (8 fases):
     [ ] 1. Requisitos (analista)
     [ ] 2. Design (designer)
     [ ] 3. Tasks (planejador)
     [ ] 4. Implementação (implementador)
     [ ] 5. Testes (testador-specs)
     [ ] 6. Revisão (revisor)
     [ ] 7. Compliance (conformista)
     [ ] 8. Documentação (documentador)

  ❓ Esta é uma feature complexa? (pagamentos geralmente são)

     Se sim: Vou invocar elicitador para análise de alinhamento arquitetural
     Se não: Vamos direto para requisitos

  Responda: sim / não"
```

### Cenário 2: Sem Feature Name

```yaml
User: /prisma:iniciar

Prisma:
  "🎯 Sistema Prisma Carregado

  O que você gostaria de fazer?

  1️⃣  Criar nova especificação
  2️⃣  Continuar especificação existente
  3️⃣  Listar especificações disponíveis
  4️⃣  Ver documentação do Prisma
  5️⃣  Executar tarefa específica

  Digite o número ou descreva o que precisa."
```

### Cenário 3: Feature Existente

```yaml
User: /prisma:iniciar user-authentication

System: Detecta que user-authentication já existe

Prisma:
  "📍 Feature: user-authentication (existente)

  📊 Status Atual:
     ✅ Requisitos: completo (requirements.md)
     ✅ Design: completo (design.md)
     🔄 Tasks: em progresso (tasks.md)
        - 5/10 tarefas completas (50%)
     ⏸️ Implementação: pausada

  🎯 Próximas Ações Disponíveis:

  1️⃣  Continuar implementação (executar próxima tarefa)
  2️⃣  Ver detalhes das tarefas pendentes
  3️⃣  Revisar código implementado até agora
  4️⃣  Atualizar design (se mudanças necessárias)
  5️⃣  Ver histórico de mudanças

  O que você gostaria de fazer?"
```

## Outputs Esperados

### Output 1: Feature Nova

```markdown
✅ Estrutura criada: .prisma/projeto/especificacoes/{feature-name}/
✅ TodoList inicializado: 8 fases
✅ Agente prisma ativado: pronto para orquestrar
⏭️  Próximo: Análise de complexidade e início de requisitos
```

### Output 2: Feature Existente

```markdown
📍 Status: {fase-atual}
📊 Progresso: {X/8} fases completas
⏭️  Próximo: {ação-sugerida}
🎯 Aguardando: {input-do-usuário}
```

### Output 3: Modo Menu

```markdown
🎯 Prisma Menu Principal:
   - Opções numeradas
   - Comandos disponíveis
   - Links para docs
```

## Integração com Outros Comandos

### Comandos que Este Invoca:

- **Internamente**: Carrega `.prisma/prompts/prisma-system.md`
- **Agente**: Invoca `.prisma/agentes/prisma.md`
- **Opcional**: Pode invocar `elicitador` se feature complexa

### Comandos Relacionados:

- `/prisma:especificacao-nova` - Criar apenas especificação
- `/prisma:especificacao-status` - Ver status de spec
- `/prisma:especificacao-listar` - Listar todas as specs
- `/prisma:tarefa-executar` - Executar tarefa específica

## Exemplos de Uso

### Exemplo 1: Nova Feature Simples

```bash
User: /prisma:iniciar dark-mode-toggle

Prisma:
  "Feature: dark-mode-toggle
   Complexidade detectada: BAIXA (UI simples)

   Vamos começar com requisitos.
   Quantos agentes analistas usar? (recomendado: 1)"

User: 1

Prisma:
  "Invocando analista...
   📝 Criando requirements.md..."
```

### Exemplo 2: Nova Feature Complexa

```bash
User: /prisma:iniciar oauth-integration

Prisma:
  "Feature: oauth-integration
   Complexidade detectada: ALTA (integração, segurança)

   🔍 Recomendo análise de alinhamento arquitetural.
   Invocar elicitador? (sim/não)"

User: sim

Prisma:
  "Invocando elicitador...
   🔍 Analisando alinhamento com arquitetura existente..."
```

### Exemplo 3: Continuar Feature

```bash
User: /prisma:iniciar payment-api

Prisma:
  "Feature: payment-api
   Status: Design aprovado ✅
   Próxima fase: Criar tasks (planejador)

   Continuar? (sim/não)"

User: sim

Prisma:
  "Quantos agentes planejadores usar? (recomendado: 2)"
```

### Exemplo 4: Modo Exploratório

```bash
User: /prisma:iniciar

Prisma:
  "O que você quer fazer?"

User: "ver o que tem disponível"

Prisma:
  "📋 Especificações Disponíveis:

   1. payment-api (in progress - 60%)
   2. user-authentication (complete - 100%)
   3. dark-mode (in progress - 30%)

   Quer continuar alguma dessas ou criar nova?"
```

## Troubleshooting

### Problema: "Agente prisma não encontrado"

**Causa**: Arquivo `.prisma/agentes/prisma.md` não existe
**Fix**: Executar setup ou criar manualmente

### Problema: "System prompt não carregado"

**Causa**: Arquivo `.prisma/prompts/prisma-system.md` não existe
**Fix**: Verificar estrutura de pastas com `ls .prisma/prompts/`

### Problema: "Estrutura de pastas incorreta"

**Causa**: Projeto não foi inicializado
**Fix**: Executar `bash .prisma/comandos/setup-structure.sh`

### Problema: "Feature já existe mas não é detectada"

**Causa**: Nome diferente (case-sensitive ou typo)
**Fix**: Listar specs com `/prisma:especificacao-listar`

## Quality Gates

Este comando NÃO tem quality gates próprios, mas:

- ✅ Valida que estrutura `.prisma/` existe
- ✅ Valida que agente `prisma` está disponível
- ✅ Valida que system prompt existe
- ⚠️ Avisa se configurações ausentes

## Configuration

**Lê de `.prisma/configuracoes/prisma.yaml`**:

```yaml
workflow:
  auto_advance: false     # Se true, não pergunta confirmação
  show_menu: true         # Se false, modo direto

startup:
  load_system_prompt: true
  show_welcome: true
  check_structure: true
```

## Ver Também

- **Onboarding**: `.prisma/comandos/onboarding.md`
- **System Prompt**: `.prisma/prompts/prisma-system.md`
- **Agente Orquestrador**: `.prisma/agentes/prisma.md`
- **Comandos relacionados**: `/prisma:especificacao-*`, `/prisma:tarefa-*`

---

**Nota**: Este é o ponto de entrada principal do sistema Prisma. Use-o quando não souber por onde começar ou quiser iniciar workflow completo.

**Última Atualização**: 2025-01-15
**Versão**: 1.1.0
**Status**: Ativo
