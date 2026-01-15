# Command: /execute-tasks

## Description

Executa tarefas de uma especificação criada.

## Usage

```
/execute-tasks [feature-name] [task-id] [mode]
```

## Parameters

- `feature-name`: Nome da feature (kebab-case)
- `task-id` (opcional): ID da tarefa específica (ex: 2.1). Se não fornecido, executa próxima tarefa pendente
- `mode` (opcional): Modo de execução
  - `sequential` (padrão): Uma tarefa por vez com aprovação
  - `parallel`: Executa tarefas específicas em paralelo
  - `auto`: Análise de dependências e execução automática

## What It Does

1. Lê tasks.md da feature
2. Identifica tarefa(s) a executar
3. Executa conforme o modo selecionado
4. Atualiza tasks.md marcando como completo
5. Roda testes se configurado

## Execution Modes

### Sequential (Default)

```
/execute-tasks export-markdown
```

Executa a próxima tarefa pendente, espera aprovação, continua.

### Specific Task

```
/execute-tasks export-markdown 2.1
```

Executa apenas a tarefa 2.1.

### Parallel Execution

```
/execute-tasks export-markdown 2.1,2.2 parallel
```

Executa tarefas 2.1 e 2.2 em paralelo usando agentes implementadores.

### Auto Mode

```
/execute-tasks export-markdown all auto
```

Analisa dependências em tasks.md e executa todas as tarefas automaticamente, respeitando dependências.

## Expected Flow

### Sequential Mode

```
User: /execute-tasks export-markdown
Assistant: Lendo tasks.md...

Próxima tarefa pendente:
[2.1] Implement data models
- Estimated Time: 3h
- Dependencies: 1.2
- Status: Not Started

Deseja executar esta tarefa? (sim/não)

User: sim
Assistant: [Executa tarefa 2.1]
[Atualiza tasks.md]

Tarefa 2.1 concluída!
Deseja executar a próxima tarefa (2.2)? (sim/não)
```

### Auto Mode

```
User: /execute-tasks export-markdown all auto
Assistant: Analisando dependências em tasks.md...

Plano de execução:
1. Paralelo: [1.1, 1.3]
2. Após 1.1: [1.2]
3. Após 1.2, 1.3: [2.1, 2.2]
...

Total estimado: 24h
Iniciar execução automática? (sim/não)

User: sim
Assistant: [Orquestra agentes implementadores conforme plano]
```
