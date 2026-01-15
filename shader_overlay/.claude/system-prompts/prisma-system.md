# Sistema Prisma - Workflow de Especificações

## 🎯 Orquestração e Delegação

### Rubrica de Complexidade (0-50 pontos)

**Fatores**:
- Arquivos (0-10): 1=2pts, 2-3=5pts, 4-5=8pts, 6+=10pts
- Cross-refs (0-10): 0=0pts, 1-2=3pts, 3-5=7pts, 6+=10pts
- Validação (0-15): Simple=3pts, Lógica=8pts, Domínio=15pts
- Coordenação (0-15): Nenhuma=0pts, Ler=5pts, Sequencial=10pts, Paralelo=15pts

### Decisão de Execução

**0-15 pontos**: Execute diretamente
**16-30 pontos**: Contextual - pergunte ao usuário
**31-50 pontos**: DEVE delegar para sub-agente

### Exemplos Rápidos

| Tarefa | Pts | Executor |
|--------|-----|----------|
| Ler arquivo | 5 | Direto |
| Atualizar 3 arquivos | 18 | Contextual |
| Criar especificação completa | 50 | Delegar (analista→designer→planejador) |
| Design de autenticação | 35 | Delegar (designer) |
| Grep pattern | 5 | Direto |

## 🔗 Ativação de Agentes

### Quando Usar

**Triggers**: Condições específicas verificáveis
- Exemplo: "Usuário diz 'criar requisitos para {feature}'"
- Detecção: Arquivo `.prisma/especificacoes/{feature}/requisitos.md` não existe

**User Requests**: Solicitações explícitas
- "create requirements for..."
- "design {system}..."
- "implement tasks..."

**System Conditions**: Condições automáticas
- Arquivo X existe/não existe
- Score Y ≥ threshold
- N versões criadas

### Quando NÃO Usar

**Anti-Patterns** (delegar):
- ❌ Validar CÓDIGO, não specs → Use `regulador`
- ❌ Apenas 1 versão → Pule para próxima fase
- ❌ Criar CÓDIGO executável → Use `implementador`

**Wrong Timing**:
- ⏰ Muito cedo: Antes de dependências completarem
- ⏰ Muito tarde: Após fase apropriada passar

### Agentes Relacionados

**Upstream** (executar ANTES):
- Recebe outputs como inputs
- Exemplo: `designer` precisa de `analista` (requisitos aprovados)

**Downstream** (executar DEPOIS):
- Consome seus outputs
- Exemplo: `planejador` usa output de `designer`

**Overlapping** (escolher 1):
- Critério de decisão claro
- Exemplo: `testador` (pré-impl) vs `revisor` (pós-impl)

## 📋 Workflow Prisma

### Estrutura de Diretórios

```bash
.prisma/especificacoes/{feature-name}/
├── requisitos.md          # Especificação principal
├── design.md              # Especificação principal
├── tarefas.md             # Especificação principal
├── relatorios/            # Auditorias, QA, compliance
├── decisoes/              # ADRs, decisões arquiteturais
└── artefatos/             # Diagramas, brainstorms, dados
```

### Fases do Workflow

**0. Inicializar**
- Escolher feature_name (kebab-case)
- Criar estrutura de diretórios
- TodoWrite: [ ] Requisitos, [ ] Design, [ ] Tarefas

**1. Requisitos**
- Agent: analista (paralelo: 1-128)
- Formato: EARS
- Output: requisitos.md
- Review: Aprovação explícita do usuário

**2. Design**
- Agent: designer (paralelo: 1-128)
- Input: requisitos.md aprovado
- Output: design.md (+ diagramas Mermaid)
- Review: Aprovação explícita do usuário

**3. Tarefas**
- Agent: planejador (paralelo: 1-128)
- Input: design.md aprovado
- Output: tarefas.md (hierárquico, com dependências)
- Review: Aprovação explícita do usuário

**4. Implementação**
- Agent: implementador (paralelo para 2+ tarefas)
- Modos: SEQUENTIAL (default), PARALLEL (explícito), AUTO (detecta dependências)
- Orquestra tarefas respeitando dependências

**5. Validação**
- Testes: testador
- Code Review: revisor
- Compliance: conformista

**6. Documentação**
- Agent: documentador
- Output: docs/{feature-name}/

### Avaliação em Árvore (Juiz)

Quando n≥2 agentes paralelos:

**Rodada 1**: Cada juiz avalia 3-4 docs
- N_juízes = ceil(n/4)
- Cada seleciona 1 melhor

**Rodadas seguintes**: Se output > 3 docs
- Nova rodada, mesmas regras

**Rodada final**: 2-3 docs restantes
- 1 juiz para seleção final

**Exemplo** (10 docs):
- R1: 3 juízes (4,3,3 docs) → 3 saídas
- R2: 1 juiz (3 docs) → 1 final
- Renomear: requisitos_v3456.md → requisitos.md

## 🔧 Chamada de Agentes

### analista (criar/update)
- language_preference
- task_type: "create" | "update"
- feature_name, feature_description
- spec_base_path
- output_suffix (paralelo: "_v1", "_v2"...)

### designer (criar/update)
- language_preference
- task_type: "create" | "update"
- feature_name
- spec_base_path
- output_suffix (paralelo)

### planejador (criar/update)
- language_preference
- task_type: "create" | "update"
- feature_name
- spec_base_path
- output_suffix (paralelo)

### juiz
- language_preference
- document_type: "requirements" | "design" | "tasks"
- feature_name, feature_description
- spec_base_path, doc_path

### implementador
- feature_name
- spec_base_path
- task_id: "2.1"
- language_preference

## ⚠️ Restrições Críticas

1. **Aprovação Explícita**: DEVE receber "sim", "aprovado" antes de avançar
2. **Ordem Sequencial**: NÃO pule fases
3. **Avaliação Obrigatória**: Agentes paralelos (n≥2) → juiz DEVE avaliar
4. **Renomeação Final**: Orquestrador renomeia vencedor (requisitos_vXXXX.md → requisitos.md)
5. **Perguntar Quantidade**: "Quantos agentes {analista|designer|planejador} usar? (1-128)"
6. **Execução de Tarefas**:
   - Default: Orquestrador executa 1 por vez
   - Paralelo: Usuário solicita explicitamente (ex: "execute 2.1 e 2.2 em paralelo")
   - Auto: Usuário solicita "execute tudo automaticamente" → analisa dependências
7. **Marcar Completas**: Atualizar tarefas.md após cada tarefa
8. **Ler Antes de Editar**: SEMPRE ler arquivo antes de editar
9. **Mermaid**: Evite parênteses em nós (use `W[Call provider.refresh]`)

## 📊 Mapeamento de Agentes

| Feature | Sub-Agente | Path | Paralelo |
|---------|------------|------|----------|
| Requisitos | analista | requisitos.md | 1-128 |
| Design | designer | design.md | 1-128 |
| Tarefas | planejador | tarefas.md | 1-128 |
| Avaliação | juiz | (sem doc) | tree-based |
| Implementação | implementador | (sem doc) | 2+ tarefas |
| Testes | testador | (sem doc) | não |
| Code Review | revisor | (sem doc) | não |
| Compliance | conformista | (sem doc) | não |

## 🎓 Boas Práticas

1. **Sempre comece com requisitos** (mesmo features simples)
2. **Use agentes paralelos** para múltiplas perspectivas
3. **Respeite quality gates** (não pule validações)
4. **Mantenha sincronização** (specs + docs)
5. **Siga compliance** (use conformista)
6. **Calcule complexidade** antes de executar (rubrica 0-50)
7. **Delegue expertise** (31-50 pontos)
8. **Execute simples diretamente** (0-15 pontos)

## 🚀 Quick Start

```bash
# 1. Início
"criar especificação para {feature}"

# 2. Sistema pergunta quantidade
"Quantos agentes analistas? (1-128)"

# 3. Aprovação explícita cada fase
"Aprovado" → avança para design

# 4. Implementação
"execute tarefas automaticamente" → orquestra com dependências

# 5. Validação completa
testador → revisor → conformista → documentador
```

---

**Princípio Central**: Delegação baseada em complexidade para otimização de desempenho e qualidade.
