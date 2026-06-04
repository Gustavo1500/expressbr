# 🚀 ExpressBR - API de Gestão de Entregas Urbanas

O **ExpressBR** é uma API RESTful de alta performance desenvolvida para gerenciar entregadores parceiros e ordens de serviço de logística urbana. O projeto foi estruturado utilizando boas práticas de desenvolvimento backend, segurança com tokens stateless e testes automatizados.

Este projeto foi construído focado em resolver problemas reais do ecossistema de logtechs e e-commerces no mercado brasileiro.

---

## 🛠️ Tecnologias e Ferramentas Utilizadas

*   **Linguagem:** Python 3.13
*   **Framework:** FastAPI (Assíncrono e de alta performance)
*   **Banco de Dados:** PostgreSQL (Rodando em container isolado via Docker)
*   **ORM:** SQLAlchemy 2.0 (Mapeamento Relacional e tratamento de transações)
*   **Segurança:** JWT (JSON Web Tokens) com hashing de senhas via `bcrypt`
*   **Validação de Dados:** Pydantic V2 (Garantia de integridade das entradas)
*   **Testes Automatizados:** Pytest (Testes de unidade e de integração)
*   **Gerenciador de Dependências:** Poetry

---

## 🎯 Diferenciais Técnicos implementados (Nível Produção)

1.  **Regras de Negócio Brasileiras (Custom Validators):**
    *   Validador customizado de **CNPJ** impedindo registros inválidos no banco de dados.
    *   Validador inteligente de **CEP** aceitando formatos com ou sem hífen (`XXXXX-XXX`).
2.  **Segurança e Autenticação Robusta:**
    *   As senhas dos entregadores são salvas no banco apenas na forma de criptografia irreversível (Hash).
    *   Criação de dependência injetada (`Depends`) de segurança para proteção de rotas privadas usando JWT.
3.  **Cálculo Dinâmico de Frete:**
    *   Lógica automática de precificação de corridas com base no peso do pacote (R$ 10,00 fixo + R$ 2,50/kg).
4.  **Banco de Dados Relacional (1-to-Many):**
    *   Tabelas de entregadores e pedidos atreladas de forma íntegra via Chave Estrangeira (ForeignKey).

---

## 🚀 Como Executar o Projeto Localmente

### Pré-requisitos
Você precisará ter instalado na sua máquina: **Python 3.12+**, **Poetry** e **Docker Desktop**.

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/seu-usuario/expressbr.git
    cd expressbr
    ```

2.  **Instale as dependências com o Poetry:**
    ```bash
    poetry install
    ```

3.  **Suba o banco de dados PostgreSQL via Docker Compose:**
    ```bash
    docker compose up -d
    ```

4.  **Inicie a aplicação:**
    ```bash
    poetry run uvicorn main:app --reload
    ```

5.  **Acesse a documentação interativa:**
    Abra `http://127.0.0.1:8000/docs` no seu navegador para interagir e testar as rotas através do Swagger.

---

## 🧪 Rodando os Testes Automatizados

O projeto conta com cobertura de testes de unidade (para validações de formato) e testes de integração (para regras de negócio). Para rodá-los:

```bash
poetry run pytest -v
