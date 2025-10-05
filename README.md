# NebulaX API

API backend para análise de exoplanetas e curvas de luz desenvolvida com FastAPI.

## Funcionalidades

- Gerenciamento de catálogo de exoplanetas 
- Análise de curvas de luz para detecção de trânsitos
- Modelo de classificação para candidatos a exoplanetas
- Cache de respostas para otimização
- CORS configurável para desenvolvimento

## Requisitos

- Python 3.12+
- FastAPI
- Uvicorn
- Pydantic

## Instalação

1. Clone o repositório:
```sh
git clone https://github.com/seu-usuario/nebula-x-backend.git
cd nebula-x-backend
```

2. Instale as dependências:
```sh 
pip install -r requirements.txt
```

## Executando

Para iniciar o servidor de desenvolvimento:

```sh
uvicorn app.main:app --reload
```

O servidor estará disponível em `http://localhost:8000`

## Endpoints

### Saúde da API
- `GET /health` - Verifica status da API
- `GET /version` - Retorna versão atual

### Exoplanetas 
- `GET /exoplanets` - Lista exoplanetas com filtros
- `GET /exoplanets/refresh` - Atualiza catálogo

### Análise
- `POST /analysis/lightcurve` - Analisa curva de luz
- `POST /analysis/train` - Treina modelo de classificação

## Documentação

A documentação interativa da API está disponível em:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Configuração

As configurações principais podem ser encontradas em `app/core/config.py`:

- `API_NAME` - Nome da API
- `API_VERSION` - Versão atual
- `ALLOWED_ORIGINS` - URLs permitidas para CORS

## Licença

MIT