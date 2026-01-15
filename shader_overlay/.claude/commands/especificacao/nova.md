# Command: /nova-especificacao

## Description

Invoca o agente **prisma** (orquestrador principal) para iniciar o workflow completo de criação de uma nova especificação.

## Usage

```
/nova-especificacao
```

## What It Does

1. **Invoca o agente prisma** (orquestrador central)
2. O agente prisma assume controle e:
   - Solicita descrição da feature
   - Cria estrutura de diretórios
   - Orquestra workflow completo (requirements → design → tasks → implementation)
   - Gerencia quality gates e aprovações
   - Coordena agentes especializados (analista, designer, planejador, etc.)

## Expected Flow

1. Usuário executa `/nova-especificacao`
2. **Agente prisma é invocado automaticamente**
3. Prisma solicita: "Descreva a feature que você quer criar"
4. Usuário fornece descrição
5. Prisma sugere nome de feature (kebab-case)
6. Prisma orquestra workflow completo com quality gates incrementais

## Example

```
User: /nova-especificacao

Claude Code: Invocando agente prisma (orquestrador principal)...

[Agente PRISMA ativado]

Prisma: Olá! Vou orquestrar a criação de uma nova especificação.

Descreva a feature que você quer criar:

User: Quero adicionar suporte para exportar workflows em formato Markdown

Prisma: Entendi. Sugiro o nome: `workflow-markdown-export`

Vou criar a estrutura:
.prisma/projeto/especificacoes/workflow-markdown-export/
├── requirements.md (pendente)
├── design.md (pendente)
├── tasks.md (pendente)
├── artifacts/
├── decisions/
└── reports/

Quantos agentes analistas deseja usar para criar requirements.md?
(1-128, recomendado: 1 para simples, 3-5 para complexo)

User: 3

Prisma: Perfeito! Invocando 3 analistas em paralelo...
[Workflow continua com orquestração completa]
```

## Implementation Details

**Código de invocação do agente:**

```markdown
Você deve invocar o agente **prisma** usando o Task tool:

- subagent_type: "prisma"
- prompt: "O usuário solicitou criar uma nova especificação. Por favor, assuma o papel de orquestrador e inicie o workflow completo conforme definido em .prisma/agentes/prisma.md"
```

## Why This Approach?

1. **Separação de responsabilidades**: Comando apenas invoca, agente orquestra
2. **Reutilização**: Agente prisma pode ser invocado por múltiplos comandos
3. **Manutenibilidade**: Lógica centralizada em um único agente
4. **Consistência**: Mesmo fluxo para todos os entry points (comando, natural language, etc.)

## Related Files

- [Agente Prisma](.prisma/agentes/prisma.md) - Especificação completa do orquestrador
- [Comando /iniciar](.prisma/comandos/iniciar.md) - Comando alternativo caso projeto não tenha .prisma/projeto configurado
- [Workflow Config](.prisma/configuracoes/prisma.yaml) - Configurações do workflow para entender linguagem do usuário e outras configurações
