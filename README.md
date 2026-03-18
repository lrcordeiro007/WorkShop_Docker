# 🐳 Workshop Docker — FastAPI + PostgreSQL

Bem-vindo ao workshop! O objetivo é aprender a containerizar uma aplicação **FastAPI** conectada ao **PostgreSQL** usando **Docker** e **Docker Compose**.

---

## 📁 Estrutura do Projeto

```
WorkShop_Docker/
├── backend/
│   ├── main.py          # Aplicação FastAPI
│   ├── models.py        # Modelos do banco de dados
│   ├── database.py      # Configuração da conexão com o banco
│   └── requirements.txt # Dependências Python
├── Dockerfile           # (você vai preencher!)
├── docker-compose.yml   # (você vai preencher!)
├── comandos.txt         # Referência de comandos Docker
└── README.md            # Este arquivo
```

---

## 🧩 Desafio 1 — Criando o Dockerfile

O `Dockerfile` define como a **imagem** da sua aplicação será construída.

### Dicas para construir o seu Dockerfile:

1. **Imagem base**: Você vai precisar de uma imagem Python. Pense em qual versão usar e se prefere a versão `slim` para economizar espaço.

2. **Diretório de trabalho**: Defina um diretório dentro do container onde o código vai ficar (ex: `/app`).

3. **Copiar dependências primeiro**: Uma boa prática é copiar o `requirements.txt` **antes** do restante do código. Por que? Pense em *cache de camadas* do Docker.

4. **Instalar dependências**: Use o `pip install` para instalar os pacotes do `requirements.txt`. Dica: use a flag `--no-cache-dir` para manter a imagem menor.

5. **Copiar o código**: Depois das dependências instaladas, copie o restante do código da pasta `backend/` para o container.

6. **Expor a porta**: A aplicação FastAPI roda por padrão na porta `8000`. Como você informa ao Docker que essa porta será utilizada?

7. **Comando de inicialização**: Para iniciar o servidor, o comando é:
   ```
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
   Como você define o comando padrão de execução no Dockerfile?

> 💡 **Palavras-chave úteis**: `FROM`, `WORKDIR`, `COPY`, `RUN`, `EXPOSE`, `CMD`

---

## 🧩 Desafio 2 — Criando o docker-compose.yml

O `docker-compose.yml` define e orquestra **múltiplos containers** que trabalham juntos.

Você precisará de **dois serviços**:

### Serviço 1: `db` (banco de dados)

- Use a imagem oficial do **PostgreSQL** (versão 15 ou similar).
- Defina as variáveis de ambiente necessárias para o banco:
  - Nome do banco de dados
  - Usuário
  - Senha
- Pense em como **persistir os dados** mesmo que o container seja reiniciado (volumes!).
- Qual porta do PostgreSQL você precisa mapear?

### Serviço 2: `backend` (sua aplicação FastAPI)

- Diga ao compose para **construir** a imagem a partir do `Dockerfile` que você criou.
- Mapeie a porta `8000` do container para a porta `8000` do seu computador.
- Passe as variáveis de ambiente para a aplicação se conectar ao banco:
  - `POSTGRES_USER`
  - `POSTGRES_PASSWORD`
  - `POSTGRES_HOST` → qual é o **nome do serviço** do banco no compose?
  - `POSTGRES_PORT`
  - `POSTGRES_DB`
- O backend **depende** do banco de dados. Como você expressa essa dependência no compose?

> 💡 **Palavras-chave úteis**: `services`, `image`, `build`, `ports`, `environment`, `volumes`, `depends_on`

---

## 🚀 Como rodar o projeto

Depois de preencher os arquivos, rode:

```bash
docker compose up --build
```

Acesse no navegador: [http://localhost:8000](http://localhost:8000)

Para parar:

```bash
docker compose down
```

---

## 🔍 Verificando se está funcionando

- A página inicial deve exibir um formulário para criar posts
- Após criar um post, ele deve aparecer na tela
- A API também está disponível em: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📖 Referência de comandos

Consulte o arquivo `comandos.txt` para os principais comandos do Docker.

---

> ⚠️ Não sabe por onde começar? Revise a documentação oficial do Docker: https://docs.docker.com