# Base de Conhecimento — Ferramentas Anthropic

Este arquivo contém conhecimento detalhado sobre as ferramentas do ecossistema Anthropic para uso na criação de cursos. Consulte as seções relevantes ao tema do curso.

## Índice

1. [Claude Code — Visão Completa](#claude-code)
2. [Claude Cowork — Visão Completa](#claude-cowork)
3. [MCP (Model Context Protocol)](#mcp)
4. [Plugins e Skills](#plugins-e-skills)
5. [Comparação entre Ferramentas](#comparacao)

---

## Claude Code

### O que é
Assistente de código agêntico da Anthropic que roda nativamente no terminal. Diferente de chatbots, tem acesso direto ao codebase, pode ler arquivos, rodar comandos, fazer edições e trabalhar autonomamente.

### Instalação
- **macOS/Linux/WSL:** `curl -fsSL https://claude.ai/install.sh | bash`
- **Windows PowerShell:** `irm https://claude.ai/install.ps1 | iex`
- **Homebrew:** `brew install --cask claude-code`
- **WinGet:** `winget install Anthropic.ClaudeCode`
- **Requisitos:** macOS 13+, Windows 10+, Ubuntu 20.04+, 4GB RAM

### Pós-instalação
1. `claude --version` — verificar
2. `claude doctor` — diagnóstico
3. `cd seu-projeto && claude` — primeira autenticação via browser

### Plataformas
- Terminal CLI (mais completo)
- VS Code Extension (diffs inline, sidebar)
- JetBrains IDEs (IntelliJ, PyCharm, WebStorm)
- Desktop App (visual, sessões paralelas)
- Web (cloud, sem setup local)

### Comandos Principais
| Comando | O que faz |
|---------|-----------|
| `/plan` | Modo planejamento — revisa antes de executar |
| `/compact` | Resume histórico para liberar contexto |
| `/clear` | Limpa contexto, começa do zero |
| `/rewind` | Volta ao estado anterior |
| `/context` | Mostra uso da janela de contexto |
| `/batch` | Refatoração paralela (precisa de git) |
| `/ultrathink` | Modo raciocínio estendido |
| `/init` | Gera CLAUDE.md inicial |
| `/model` | Troca modelo na sessão |
| `/effort` | Ajusta nível de raciocínio |

### CLI Flags Importantes
```bash
claude -p "prompt"                    # Modo não-interativo
claude -p "prompt" --output-format json  # Saída JSON
claude --continue                     # Retoma última sessão
claude --resume                       # Seleciona sessão para retomar
claude --worktree feature-branch      # Cria worktree isolado
claude --add-dir /path/to/code        # Inclui diretório adicional
claude mcp add --transport http name url  # Adiciona MCP server
```

### CLAUDE.md — O Arquivo Mais Importante
O CLAUDE.md é a "memória" do Claude Code. Ele lê automaticamente ao iniciar.

**Locais por escopo:**
| Escopo | Local | Compartilhado? |
|--------|-------|----------------|
| Usuário | `~/.claude/CLAUDE.md` | Não |
| Projeto | `./CLAUDE.md` na raiz | Sim (via git) |
| Local | `.claude/settings.local.json` | Não |

**O que colocar:**
- Stack tecnológico do projeto
- Convenções de código (naming, estilo)
- Comandos para rodar testes
- Arquitetura do projeto
- Regras específicas ("nunca use any em TypeScript")
- Padrões de design preferidos

### Features Avançadas

**Agentes Paralelos:**
- Spawn múltiplas instâncias coordenadas
- Git Worktrees para isolamento
- Subagentes para pesquisa
- `/batch` para fan-out (5-30 unidades paralelas)

**Hooks:**
- Eventos de ciclo de vida (pre-commit, post-edit, etc.)
- Handlers: command, HTTP, prompt, agent
- Automação de validação, testes, formatação

**Integração CI/CD:**
- Flag `-p` para pipelines
- Automação de code review
- Geração de release notes
- GitHub Actions e GitLab CI/CD

### Atalhos VS Code
| Atalho | Ação |
|--------|------|
| `Cmd+Esc` / `Ctrl+Esc` | Alternar foco editor ↔ Claude |
| `Option+K` / `Alt+K` | @-mention com seleção |
| `Cmd+N` / `Ctrl+N` | Nova conversa |
| `Shift+Enter` | Input multi-linha |

### Modos de Permissão
- `default`: Pede para cada ação
- `plan`: Mostra plano, espera aprovação
- `acceptEdits`: Aprova edits, pede para comandos perigosos
- `bypassPermissions`: Sem prompts (cuidado extremo)

---

## Claude Cowork

### O que é
Feature do Claude Desktop que transforma Claude de chatbot em agente autônomo para trabalho de conhecimento. Lê/escreve arquivos locais, executa tarefas multi-step sem supervisão constante.

### Como Acessar
1. Abrir Claude Desktop
2. Ir na aba Cowork/Tasks
3. Selecionar pasta de trabalho
4. Descrever a tarefa

### Requisitos
- **macOS:** Apple Silicon (M1+) obrigatório. Intel NÃO suportado
- **Windows:** Windows 11 Pro/Enterprise (Hyper-V necessário). Home NÃO suportado
- **RAM:** 8GB recomendado
- **Plano:** Pro, Max, Team ou Enterprise

### Capacidades Principais
- Execução autônoma de tarefas complexas
- Acesso a arquivos locais (com permissão)
- Processamento estendido sem timeouts
- Coordenação de agentes paralelos
- Criação de documentos profissionais (docx, pptx, xlsx, pdf)
- Transparência — mostra raciocínio e progresso

### Sistema de Skills
Skills são instruções markdown reutilizáveis que transformam Claude em especialista.

**Estrutura de uma Skill:**
```
skill-name/
├── SKILL.md (obrigatório)
│   ├── YAML frontmatter (name, description)
│   └── Instruções markdown
└── Recursos (opcional)
    ├── scripts/     — Código executável
    ├── references/  — Docs carregados sob demanda
    └── assets/      — Templates, ícones, fontes
```

**Como criar:** Descrever workflow em linguagem natural → Claude gera a skill → Revisar → Salvar

**Boas práticas:**
- Voz imperativa ("Leia o arquivo", não "O arquivo deve ser lido")
- Exemplos concretos valem mais que descrições longas
- Skills compartilham ~2% da janela de contexto

### Sistema de Plugins
Plugins empacotam: Skills + Conectores + Sub-agentes + Slash Commands

**15+ plugins oficiais da Anthropic:** Sales, Finance, Legal, Marketing, HR, Engineering, Design, Operations, Data Analysis

**Instalação:** Cowork tab → Customize → Browse plugins → Install

### Conectores (38+ ferramentas)
- **Comunicação:** Slack, Email
- **Produtividade:** Notion, Google Drive, Docs, Sheets, Slides
- **Desenvolvimento:** GitHub, Linear
- **Enterprise:** Salesforce, HubSpot, Jira, Snowflake
- **Autenticação:** OAuth ou API keys
- **Setup:** Menos de 1 minuto cada

### Tarefas Agendadas
- Rodar tarefas automaticamente (diário, semanal, por hora)
- App precisa estar aberto
- Se computador dormir, tarefa é pulada

### Projetos no Cowork
- Workspaces persistentes com pasta, arquivos, contexto
- Memória própria por projeto
- Instruções e configurações isoladas

### Limitações Conhecidas
- Desktop only (sem web/mobile)
- App precisa ficar aberto
- Intel Mac não suportado
- Windows Home não suportado (precisa Hyper-V)
- MCP all-or-nothing (consome contexto)
- Sem audit trail enterprise
- Tarefas puladas se PC dormir

---

## MCP (Model Context Protocol)

### O que é
Protocolo aberto criado pela Anthropic que conecta Claude a ferramentas e serviços externos de forma segura. Cada MCP server expõe "ferramentas" que Claude pode chamar.

### Como Configurar
```bash
# Adicionar server HTTP
claude mcp add --transport http nome-server https://url-do-server

# Adicionar server stdio
claude mcp add --transport stdio nome-server -- comando args

# Listar servers
claude mcp list
```

### Servers Populares
- **GitHub:** Gerenciar repos, PRs, issues
- **Notion:** Ler/escrever páginas e databases
- **Figma:** Acessar designs e componentes
- **Slack:** Buscar mensagens, postar
- **Banco de dados:** PostgreSQL, MySQL, SQLite
- **APIs custom:** Qualquer API REST/GraphQL

### Impacto no Contexto
- Cada MCP server consome parte da janela de contexto
- Configuração é global (afeta todos os projetos)
- Recomendação: ativar apenas o necessário

---

## Plugins e Skills

### Skills vs Plugins
| Aspecto | Skill | Plugin |
|---------|-------|--------|
| Formato | SKILL.md individual | Pacote com múltiplas skills |
| Escopo | Uma tarefa/workflow | Workflow completo |
| Distribuição | Local | Marketplace/compartilhável |
| Componentes | Instruções + referências | Skills + conectores + sub-agentes |

### Criar Plugin Custom
1. Usar "Plugin Create" no Cowork
2. Definir skills, conectores e comandos
3. Empacotar como .plugin
4. Distribuir via marketplace ou upload

---

## Comparação entre Ferramentas

### Quando usar Claude Code
- Desenvolvimento de software
- Projetos com codebase existente
- CI/CD e automação de deploy
- Tarefas que precisam de terminal/git
- Performance e precisão máximas

### Quando usar Cowork
- Trabalho com documentos (Word, PowerPoint, Excel)
- Organização de arquivos
- Pesquisa e síntese de informações
- Automação de tarefas de escritório
- Usuários não-técnicos

### Quando usar ambos
- Criar app (Code) + criar marketing (Cowork)
- Desenvolver (Code) + documentar (Cowork)
- Automatizar desenvolvimento (Code) + automatizar processos (Cowork)

### Claude Code vs Concorrentes
| Ferramenta | Força | Fraqueza |
|-----------|-------|----------|
| Claude Code | Tarefas complexas, multi-arquivo | Curva de aprendizado |
| GitHub Copilot | Integração editor, enterprise | Limitado em tarefas agênticas |
| Cursor | UI amigável, multi-arquivo | Menos autônomo |
