
# PortoMaré

## Visão Geral

O **PortoMaré** é uma API backend desenvolvida em Python que consulta informações de maré para portos do estado de Pernambuco, identifica a próxima mudança de maré com base no horário atual e utiliza uma API de Inteligência Artificial para gerar uma frase informativa e descontraída sobre essa mudança.

O projeto foi desenvolvido com foco em simplicidade, clareza arquitetural e boas práticas, sem exposição de código-fonte, apenas disponibilizando a API em produção.

---

## Objetivo

Demonstrar a construção de uma API que:

- Consome dados reais de maré
- Processa regras de negócio no backend
- Utiliza IA apenas para geração de texto
- Disponibiliza um endpoint público
- Está hospedada no plano gratuito do Render

---

## Funcionalidades

- Consulta da tábua de maré do dia para portos de Pernambuco
- Identificação da próxima alteração de maré em relação ao horário atual
- Geração de frase automática via IA contendo:
  - Horário da próxima maré
  - Tipo da maré
  - Texto em tom leve e informativo
- Exposição dos dados via API REST

---

## Endpoint

### Obter mensagem da próxima maré

```
GET /tide-message?port=recife
```

#### Parâmetros

- `port` (string): nome do porto em Pernambuco

#### Exemplo de resposta

```json
{
  "state": "pe",
  "port_id": "pe01",
  "current_time": "19:17",
  "next_tide_change": {
    "time": "22:29",
    "level": 0.449999988079071,
    "type": "low"
  },
  "message": "Maré baixa: 0.4 metros às 22:29, a areia tá pedindo um descanso."
}
```

---

## Arquitetura

O projeto segue uma abordagem inspirada em Clean Architecture, separando claramente responsabilidades.

```
app/
├── api/
├── application/
├── domain/
├── infrastructure/
├── tests/
└── config/
```

### Camadas

- **Domain**: modelos e contratos centrais do negócio
- **Application**: casos de uso e regras de orquestração
- **Infrastructure**: integração com APIs externas (maré e IA)
- **API**: interface HTTP
- **Tests**: testes unitários das regras de negócio

A lógica de decisão nunca é delegada à IA.

---

## Integração com IA

A Inteligência Artificial é utilizada exclusivamente para geração de texto.

O backend envia dados estruturados como:
- Horário atual
- Horário da próxima maré
- Tipo e nível da maré
- Localização

A IA retorna apenas uma frase textual, sem tomar decisões de negócio.

---

## Testes

O projeto contempla testes unitários para:

- Identificação da próxima mudança de maré
- Fluxo dos casos de uso
- Validação de entradas

Integrações externas são mockadas durante os testes.

---

## Deploy

A aplicação está hospedada no **Render**, utilizando:

- FastAPI
- Uvicorn
- Variáveis de ambiente para chaves sensíveis

Comando de inicialização:

```
uvicorn app.main:app --host 0.0.0.0 --port 10000
```

---

## Considerações Finais

O PortoMaré demonstra como combinar dados reais, regras de negócio bem definidas e IA de forma responsável, mantendo o controle da lógica no backend e garantindo uma API simples, clara e fácil de evoluir.