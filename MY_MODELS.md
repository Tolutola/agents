# My Models and Providers

How my practice notebooks choose an AI provider and model, which models I have, and the gotchas.

- **`my_llm.py`** holds my providers, keys and default models. Every `_mine` notebook imports it.
- **`my_models.ipynb`** lists live every model my keys can use, shows my balances, and lets me try any model. Run All to refresh.

## Switching provider or model

Every `_mine` notebook starts with a setup cell like this:

```python
import sys; sys.path.append("..")       # lets this notebook import my_llm.py from the agents folder
from my_llm import setup, models, client
setup()                                  # loads .env; anything still expecting OpenAI goes to OpenRouter

PROVIDER = "openrouter"                  # openrouter | gemini | deepseek | anthropic | ollama
SMALL, MEDIUM, LARGE = models(PROVIDER)  # model names; or set any, e.g. MEDIUM = "x-ai/grok-4.3"
```

- **Switch provider:** change `PROVIDER`, then re-run the notebook from the top.
- **Try one specific model:** add a line after `models(...)`, for example `MEDIUM = "moonshotai/kimi-k2.6"`. The name must be one that `PROVIDER` offers; copy it from `my_models.ipynb`.
- **Change my defaults everywhere:** edit `MODELS` in `my_llm.py`.

`setup()` also points any code that still expects OpenAI (helper `.py` files like `sidekick.py`, or cells I haven't changed) at OpenRouter. OpenRouter accepts OpenAI model names like `gpt-5.4-mini`, so that code keeps working and is billed to my OpenRouter credit.

## My providers

| Provider | `.env` key | Good for | Balance |
|---|---|---|---|
| `openrouter` | `OPENROUTER_API_KEY` | Hundreds of models with one key, including OpenAI's GPT models, which I have no direct key for | `my_models.ipynb`, or openrouter.ai/activity |
| `gemini` | `GEMINI_API_KEY` (`GOOGLE_API_KEY` is the same key) | Fast, cheap Google models; Google ADK in week 5 | Google AI Studio |
| `deepseek` | `DEEPSEEK_API_KEY` | Very cheap and capable | `my_models.ipynb` |
| `anthropic` | `ANTHROPIC_API_KEY` | Claude | Billing page in the Claude Console |
| `ollama` | none | Free, private, runs on this Mac | free |

## Default models

Prices are US dollars per million input / output tokens, from OpenRouter's listing in October 2026.

| Provider | SMALL | MEDIUM (most labs) | LARGE |
|---|---|---|---|
| `openrouter` | `openai/gpt-5.4-nano` ($0.20 / $1.25) | `openai/gpt-5.4-mini` ($0.75 / $4.50) | `openai/gpt-5.5` ($5 / $30) |
| `gemini` | `gemini-3.1-flash-lite` ($0.25 / $1.50) | `gemini-3.8-flash` ($0.83 / $4.12) | `gemini-4-argon` ($2 / $10) |
| `deepseek` | `deepseek-flash` (about $0.09 / $0.18) | `deepseek-flash` | `deepseek-v4-pro` ($0.30 / $0.59) |
| `anthropic` | `claude-haiku-5-5` ($0.10 / $0.50) | `claude-sonnet-5-5` ($2 / $10) | `claude-opus-5-5` ($4 / $20) |
| `ollama` | `llama3.2` | `gpt-oss:20b` | `qwen3.8:27b` |

The OpenRouter row matches the OpenAI models Ed uses, so with the default `PROVIDER` the labs behave like his.

### Other models worth trying (through OpenRouter)

| Model | Price (in / out) | Notes |
|---|---|---|
| `moonshotai/kimi-k2.6` | $0.65 / $3.41 | Strong open model; Ed uses it in week 2 |
| `x-ai/grok-4.3` | $1.25 / $2.50 | Grok, without a separate xAI key |
| `deepseek/deepseek-v4-flash` | $0.09 / $0.18 | DeepSeek with working structured outputs |
| `qwen/qwen3.8-27b` | $0.24 / $2.20 | Same model as my local `qwen3.8:27b`, but in the cloud |
| `anthropic/claude-sonnet-5.5` | $2 / $10 | Claude billed to OpenRouter credit instead |
| Models ending `:free` | $0 | Rate-limited; see the free table in `my_models.ipynb` |

## How each week is wired

| Week | Framework | In the `_mine` notebooks |
|---|---|---|
| 1 | OpenAI client | `openai = client(PROVIDER)`, then `model=SMALL` / `MEDIUM` / `LARGE` |
| 2 and 6 | OpenAI Agents SDK | `MODEL = agents_model(PROVIDER, MEDIUM)`, then `Agent(..., model=MODEL)`. To mix providers: `agents_model("gemini", "gemini-3.8-flash")` |
| 3 | CrewAI | Not changed (no notebooks). Set `llm:` in a crew's `agents.yaml`, for example `openrouter/openai/gpt-5.4-mini`, `gemini/gemini-3.8-flash`, `deepseek/deepseek-flash`, `anthropic/claude-sonnet-5-5` or `ollama/qwen3.8:27b` (Ollama also needs `base_url: http://localhost:11434`). CrewAI reads the same `.env` keys. I haven't tested this |
| 4 | LangChain / LangGraph | `langchain_model(PROVIDER, MEDIUM)` in place of `ChatOpenAI(...)` and `"openai:..."` strings. Read replies with `.text` |
| 5 | Google ADK | Unchanged: uses Gemini directly with my `GOOGLE_API_KEY`. ADK needs LiteLLM for other providers, and that isn't installed |
| 5 | Pydantic AI | `pydantic_ai_model(PROVIDER, MEDIUM)` |
| 5 | Strands | `strands_model(PROVIDER, MEDIUM)` |
| 5 | Agno | `agno_model(PROVIDER, MEDIUM)` |
| 5 | Microsoft Agent Framework | `maf_client(PROVIDER, MEDIUM)` |

Every helper works with all five providers. Each was tested with a multi-step tool call on every provider. The first model cell of every notebook was run on OpenRouter, and five notebooks (one per framework) were run on every provider.

### Starting a new lab

When Ed adds a lab, copy it to `_mine` first (see `MY_GIT_WORKFLOW.md`). Then paste the setup cell above near the top, after the imports, and swap the hard-coded models:

| Ed's code | Mine |
|---|---|
| `OpenAI()` | `client(PROVIDER)` |
| `model="gpt-5.4-mini"` in the OpenAI client | `model=MEDIUM` |
| `model="gpt-5.4-mini"` in the Agents SDK | `model=agents_model(PROVIDER, MEDIUM)` |
| `ChatOpenAI(model=...)` | `langchain_model(PROVIDER, MEDIUM)` |

In week 5 subfolders, use `sys.path.append("../..")`.

## My local Ollama models

| Model | Size | Use it for |
|---|---|---|
| `qwen3.8:27b` | 18 GB | Best local all-rounder for agents. In my tests it got multi-step tool calls right 3 times out of 3, at about 35 words (tokens) per second |
| `gpt-oss:20b` | 13 GB | Fastest capable model, at about 80 tokens per second, with good tool calling. Weaker at mental arithmetic |
| `gemma4:26b` | 16 GB | Fast backup; once invented a tool name that didn't exist |
| `llama3.2` | 2 GB | Tiny and quick; week 1 lab 2. Weak at tools |
| `qwen3-embedding:0.6b` | 0.6 GB | Embeddings only (text to vectors, for RAG) |

- **Use them:** set `PROVIDER = "ollama"`, or call one directly with `client("ollama").chat.completions.create(model="qwen3.8:27b", messages=...)`.
- **Embeddings:** `client("ollama").embeddings.create(model="qwen3-embedding:0.6b", input=["some text"])`.
- **Keep Ollama running:** the Ollama app must be open (menu bar icon). It's in local-only mode (`~/.ollama/server.json`), so it never uses Ollama's cloud.
- **Memory:** a model loads when first called and unloads after 5 idle minutes. Run `ollama ps` to see what's loaded, `ollama stop <model>` to unload one now, and `ollama list` / `ollama rm <model>` to manage downloads.
- **Speed:** local models are slower on the big agent labs (week 6 traders, deep research), so use OpenRouter there if waiting gets painful.

## Gotchas

| Situation | What happens | What to do |
|---|---|---|
| Ollama agent with both `tools=` and `output_type=` | It never calls its tools and makes up the answer | Split it into two agents: one with the tools, then a formatter with `output_type` that reads the first one's answer |
| `output_type=` / `with_structured_output` on `deepseek` | DeepSeek's API rejects it | Use `PROVIDER = "openrouter"` with `MEDIUM = "deepseek/deepseek-v4-flash"` |
| `tool_choice="required"` on `anthropic` (Claude 5.5) or `deepseek` | Error 400 | Week 2 lab 2 already switches to `"auto"` for these |
| `SandboxAgent` (week 2 lab 3) | Needs OpenAI's Responses API and its built-in tools | That cell stays on OpenAI's `gpt-5.4-mini` via OpenRouter, whatever `PROVIDER` is |
| `WebSearchTool` (week 2 lab 4) | Needs an OpenAI key | Replaced by `openai/gpt-5.4-mini:online`: the `:online` suffix makes OpenRouter search the web on each request (a few cents per search) |
| Gemini in LangChain | `.content` comes back as a list of parts | The notebooks read `.text`, which is always plain text |
| Gemini in Microsoft Agent Framework | Gemini tool calls fail through Google's OpenAI-compatible endpoint | `maf_client` sends Gemini through OpenRouter instead (it prints a note; billed to OpenRouter) |
| `temperature` | Current Claude models reject values below 1 through the OpenAI-compatible endpoint, and GPT-5 models don't accept it at all | Leave it out (the labs don't set it) |
| Trace links to platform.openai.com | Nothing shows: uploading traces needs an OpenAI key | `setup()` turns off that upload. `trace(...)` and custom trace processors, like week 6's `LogTracer`, still work |
| Week 4 lab 5 Sidekick | `sidekick.py` always uses `gpt-5.4-mini` | Runs via OpenRouter. To change it, copy to `sidekick_mine.py` and edit the copy |

### Non-model keys some labs need

| Key | Used by | Get one |
|---|---|---|
| `SERPER_API_KEY` | Week 4 labs 2, 4 and 5 (Google search tool) | serper.dev (free starter credits) |
| `TAVILY_API_KEY` | Week 6 lab 3 and the trading floor researcher | tavily.com (free tier) |
| `PUSHOVER_TOKEN`, `PUSHOVER_USER` | Push notifications in weeks 1, 2, 4, 5 and 6 | pushover.net |
| Email settings (`EMAIL_ADDRESS` and others) | Week 2 email sending | See Ed's week 2 instructions |
| `MASSIVE_API_KEY` | Week 6 market data (optional; there's a built-in fallback) | massive.com |

## Scripts that run outside a notebook

Some labs run Python files in a terminal, so `setup()` never runs:
- the week 5 workers (`uv run strands_worker.py` and the others),
- the week 6 trading floor (`uv run -m backend.trading_floor`) and its API,
- the Sidekick app when run on its own.

They expect an OpenAI key. To send them to OpenRouter, add these lines to `.env`:

```bash
# Send code that expects OpenAI to OpenRouter (OpenRouter accepts OpenAI model names like gpt-5.4-mini)
OPENAI_API_KEY=${OPENROUTER_API_KEY}
OPENAI_BASE_URL=https://openrouter.ai/api/v1
```

`${OPENROUTER_API_KEY}` reuses the key already in the file, so the secret isn't copied.

- **Model names:** these scripts then run OpenAI models such as `gpt-5.4-mini` billed to OpenRouter. The week 5 workers read `WORKER_MODEL`, for example `WORKER_MODEL=gpt-5.4 uv run strands_worker.py`.
- **Trace warnings:** the Agents SDK will print a harmless "tracing" warning when it fails to upload traces to OpenAI. Don't add `OPENAI_AGENTS_DISABLE_TRACING`, because that also switches off the trading floor's activity log.
- **Removing them:** if I ever get a real OpenAI key, replace these two lines with `OPENAI_API_KEY=<that key>`.
