# refAIne

A FastAPI microservice that transforms casual user prompts into expert-level AI engineering prompts using your choice of LLM provider (Anthropic Claude, OpenAI, Ollama, Groq, and more).

## Features

- Single endpoint POST `/refine` for prompt transformation
- **Multi-provider support**: Choose from cloud or local LLMs
  - **Free options**: Ollama (local), Groq (cloud free tier), LM Studio (local)
  - **Paid options**: Anthropic Claude, OpenAI, or any OpenAI-compatible API
- Adds software development context and specificity
- Includes best practices, error handling, and edge cases
- Production-ready with Docker support
- Simple environment variable-based provider switching
- **Test locally for free** with Ollama before using paid APIs

## Quick Start

### 🚀 Fastest Way: Test with Ollama (Free, 2 minutes)

```bash
# 1. Install Ollama (if not already installed)
# Visit https://ollama.ai or run: curl -fsSL https://ollama.com/install.sh | sh

# 2. Pull a model
ollama pull llama3.1

# 3. Clone and setup RefAIne
git clone <repo-url>
cd RefAIne

# 4. Create .env file
cat > .env << EOF
LLM_PROVIDER=openai
OPENAI_BASE_URL=http://localhost:11434/v1
OPENAI_API_KEY=ollama
OPENAI_MODEL=llama3.1
EOF

# 5. Install and run
uv pip install -r pyproject.toml
uvicorn main:app --reload

# 6. Test it!
curl -X POST http://localhost:8000/refine \
  -H "Content-Type: application/json" \
  -d '{"prompt": "create a REST API"}'
```

### Prerequisites

- Python 3.12+
- uv package manager
- LLM provider of your choice:
  - **Ollama** (free, local) - recommended for testing
  - **Groq** (free tier, cloud) - fast inference
  - **Anthropic Claude** (paid, cloud) - high quality
  - **OpenAI** (paid, cloud) - widely compatible
  - Or any OpenAI-compatible API

### Local Development

1. **Clone and setup**
```bash
git clone <repo-url>
cd RefAIne
```

2. **Configure environment**

**Option A: Using Ollama (Free, Local):**
```bash
# Install Ollama from https://ollama.ai
ollama pull llama3.1

# Create .env file
cp .env.example .env
# Edit .env and set:
# LLM_PROVIDER=openai
# OPENAI_BASE_URL=http://localhost:11434/v1
# OPENAI_API_KEY=ollama
# OPENAI_MODEL=llama3.1
```

**Option B: Using Anthropic Claude:**
```bash
cp .env.example .env
# Edit .env and set:
# LLM_PROVIDER=anthropic
# ANTHROPIC_API_KEY=your_api_key_here
```

**Option C: Using Groq (Free Tier):**
```bash
cp .env.example .env
# Edit .env and set:
# LLM_PROVIDER=openai
# OPENAI_BASE_URL=https://api.groq.com/openai/v1
# OPENAI_API_KEY=your_groq_api_key
# OPENAI_MODEL=llama-3.3-70b-versatile
```

3. **Install dependencies**
```bash
uv pip install -r pyproject.toml
```

4. **Run the service**
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Docker Deployment

1. **Configure your .env file** with your chosen provider (see Configuration section below)

2. **Build and run with docker-compose**
```bash
docker-compose up -d
```

3. **Or build manually**
```bash
docker build -t refaine .

# For Anthropic Claude
docker run -p 8000:8000 -e LLM_PROVIDER=anthropic -e ANTHROPIC_API_KEY=your_key refaine

# For Groq
docker run -p 8000:8000 -e LLM_PROVIDER=openai -e OPENAI_BASE_URL=https://api.groq.com/openai/v1 -e OPENAI_API_KEY=your_key -e OPENAI_MODEL=llama-3.3-70b-versatile refaine
```

## API Usage

### Health Check
```bash
curl http://localhost:8000/
```

Response:
```json
{
  "service": "refAIne",
  "status": "healthy",
  "version": "1.0.0"
}
```

### Refine a Prompt

**Endpoint:** `POST /refine`

**Request:**
```bash
curl -X POST http://localhost:8000/refine \
  -H "Content-Type: application/json" \
  -d '{"prompt": "make a function to sort a list"}'
```

**Response (example from Ollama with llama3.1):**
```json
{
  "original": "make a function to sort a list",
  "refined": "Create a Python function that sorts a list with the following requirements:\n\n1. Function signature: Accept a list of comparable elements as input\n2. Return a new sorted list (do not modify the original)\n3. Use Python's built-in sorting (efficient O(n log n) Timsort)\n4. Add type hints for better code clarity\n5. Include error handling for None or non-list inputs\n6. Add docstring with examples\n7. Consider edge cases: empty list, single element, already sorted, reverse sorted\n8. Make it generic to work with any comparable types (int, str, float, etc.)\n\nProvide clean, PEP 8 compliant code with appropriate documentation.",
  "model": "llama3.1"
}
```

*The refined output quality and style will vary depending on your chosen LLM provider and model.*

### Example Use Cases

**Basic prompt:**
```bash
curl -X POST http://localhost:8000/refine \
  -H "Content-Type: application/json" \
  -d '{"prompt": "create a REST API"}'
```

**More specific prompt:**
```bash
curl -X POST http://localhost:8000/refine \
  -H "Content-Type: application/json" \
  -d '{"prompt": "build user authentication"}'
```

**Algorithm request:**
```bash
curl -X POST http://localhost:8000/refine \
  -H "Content-Type: application/json" \
  -d '{"prompt": "optimize database queries"}'
```

## Configuration

### LLM Provider Selection

RefAIne supports multiple LLM providers. Choose your provider using the `LLM_PROVIDER` environment variable.

#### **Ollama** (Local, Free) - Recommended for Testing
```bash
LLM_PROVIDER=openai
OPENAI_BASE_URL=http://localhost:11434/v1
OPENAI_API_KEY=ollama
OPENAI_MODEL=llama3.1
```

**Prerequisites:**
- Install Ollama: https://ollama.ai
- Pull a model: `ollama pull llama3.1`
- Start server: `ollama serve`

**Supported Ollama Models:**
- `llama3.1`, `llama3.2`, `llama3.3`
- `qwen2.5`, `mistral`, `codellama`
- Any model available in Ollama library

#### **Groq** (Cloud, Free Tier)
```bash
LLM_PROVIDER=openai
OPENAI_BASE_URL=https://api.groq.com/openai/v1
OPENAI_API_KEY=your-groq-api-key
OPENAI_MODEL=llama-3.3-70b-versatile
```

**Get API Key:** https://console.groq.com

**Supported Groq Models:**
- `llama-3.3-70b-versatile`
- `llama-3.1-70b-versatile`
- `mixtral-8x7b-32768`

#### **Anthropic Claude** (Cloud, Paid)
```bash
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-your-key-here
CLAUDE_MODEL=claude-sonnet-4-20250514
```

**Supported Claude Models:**
- `claude-sonnet-4-20250514` (default)
- `claude-opus-4-20250514`
- `claude-3-5-sonnet-20241022`

#### **OpenAI** (Cloud, Paid)
```bash
LLM_PROVIDER=openai
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_API_KEY=sk-your-openai-key
OPENAI_MODEL=gpt-4-turbo-preview
```

**Supported OpenAI Models:**
- `gpt-4-turbo-preview`
- `gpt-4o`
- `gpt-3.5-turbo`

#### **LM Studio** (Local, Free)
```bash
LLM_PROVIDER=openai
OPENAI_BASE_URL=http://localhost:1234/v1
OPENAI_API_KEY=lm-studio
OPENAI_MODEL=your-model-name
```

**Prerequisites:**
- Download LM Studio: https://lmstudio.ai
- Load a model in LM Studio
- Start the server from the LM Studio UI

#### **Any OpenAI-Compatible API**

RefAIne works with any LLM service that implements the OpenAI API format:
```bash
LLM_PROVIDER=openai
OPENAI_BASE_URL=https://your-api-endpoint/v1
OPENAI_API_KEY=your-api-key
OPENAI_MODEL=your-model-name
```

Compatible services include: vLLM, Text Generation Inference, FastChat, LocalAI, and more.

### Environment Variables Reference

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `LLM_PROVIDER` | Provider type: `anthropic` or `openai` | `anthropic` | No |
| **Anthropic Settings** ||||
| `ANTHROPIC_API_KEY` | Anthropic API key | - | Required if using Anthropic |
| `CLAUDE_MODEL` | Claude model name | `claude-sonnet-4-20250514` | No |
| **OpenAI-Compatible Settings** ||||
| `OPENAI_API_KEY` | API key (for OpenAI, Groq, etc.) | - | Required if `LLM_PROVIDER=openai` |
| `OPENAI_BASE_URL` | API endpoint URL | `https://api.openai.com/v1` | No |
| `OPENAI_MODEL` | Model name | `gpt-4-turbo-preview` | No |

**Note:** For Ollama, use `LLM_PROVIDER=openai` with `OPENAI_BASE_URL=http://localhost:11434/v1`

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Development

### Project Structure
```
RefAIne/
├── main.py              # FastAPI application
├── pyproject.toml       # Dependencies
├── Dockerfile           # Container image
├── docker-compose.yml   # Orchestration
├── .env.example         # Environment template
└── README.md           # Documentation
```

### Testing

```bash
# Install with dev dependencies
uv pip install -r pyproject.toml

# Run the service
uvicorn main:app --reload

# Test in another terminal
curl -X POST http://localhost:8000/refine \
  -H "Content-Type: application/json" \
  -d '{"prompt": "test prompt"}'
```

## Production Considerations

- **Provider selection**: Choose based on your needs (cost, speed, quality, privacy)
- **Rate limiting**: Set appropriate limits for your chosen provider
- **Authentication**: Add API keys or authentication if exposing publicly
- **Monitoring**: Track API usage and costs (for paid providers)
- **Caching**: Implement caching for common prompts to reduce latency and costs
- **Timeouts**: Configure request timeouts based on provider speed
- **Scaling**: For local providers (Ollama), ensure adequate hardware resources
- **Security**: Keep API keys secure, use environment variables, never commit to git

## License

MIT
