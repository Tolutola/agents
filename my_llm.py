"""
my_llm.py - one place to choose which AI provider and model the labs use.

Every *_mine notebook starts with a setup cell like this:

    import sys; sys.path.append("..")      # lets the notebook import this file
    from my_llm import setup, models, client
    setup()
    PROVIDER = "openrouter"                # openrouter | gemini | deepseek | anthropic | ollama
    SMALL, MEDIUM, LARGE = models(PROVIDER)

Change PROVIDER to switch everything at once, or set SMALL / MEDIUM / LARGE to any
model name that provider offers. MY_MODELS.md explains the options, and
my_models.ipynb lists every model your keys can use right now.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from openai import AsyncOpenAI, OpenAI

ENV_FILE = Path(__file__).parent / ".env"

# Each provider's OpenAI-compatible endpoint, and the .env variable that holds its key
PROVIDERS = {
    "openrouter": {"base_url": "https://openrouter.ai/api/v1", "key": "OPENROUTER_API_KEY"},
    "gemini": {"base_url": "https://generativelanguage.googleapis.com/v1beta/openai/", "key": "GEMINI_API_KEY"},
    "deepseek": {"base_url": "https://api.deepseek.com", "key": "DEEPSEEK_API_KEY"},
    "anthropic": {"base_url": "https://api.anthropic.com/v1/", "key": "ANTHROPIC_API_KEY"},
    "ollama": {"base_url": "http://localhost:11434/v1", "key": None},
}

# (small, medium, large) for each provider: cheap and quick, everyday default, most capable.
# The OpenRouter row matches the OpenAI models Ed uses in the course.
MODELS = {
    "openrouter": ("openai/gpt-5.4-nano", "openai/gpt-5.4-mini", "openai/gpt-5.5"),
    "gemini": ("gemini-3.1-flash-lite", "gemini-3.8-flash", "gemini-4-argon"),
    "deepseek": ("deepseek-flash", "deepseek-flash", "deepseek-v4-pro"),
    "anthropic": ("claude-haiku-5-5", "claude-sonnet-5-5", "claude-opus-5-5"),
    "ollama": ("llama3.2", "gpt-oss:20b", "qwen3.8:27b"),
}


def setup():
    """Load my keys from .env, send any code that still expects OpenAI to OpenRouter,
    and stop the Agents SDK uploading traces to OpenAI (that needs a real OpenAI key)."""
    load_dotenv(ENV_FILE, override=True)
    if not os.getenv("OPENAI_API_KEY"):
        # OpenRouter accepts OpenAI model names like "gpt-5.4-mini", so untouched course
        # code (and helper .py files such as sidekick.py) keeps working, billed to OpenRouter
        os.environ["OPENAI_API_KEY"] = os.environ["OPENROUTER_API_KEY"]
        os.environ["OPENAI_BASE_URL"] = PROVIDERS["openrouter"]["base_url"]
    try:
        from agents import set_trace_processors

        # Removes only the OpenAI uploader: trace() still works, and labs can add
        # their own processor (like week 6's LogTracer) with add_trace_processor
        set_trace_processors([])
    except ImportError:
        pass


def models(provider):
    """The (small, medium, large) model names for a provider."""
    return MODELS[provider]


def base_url(provider):
    return PROVIDERS[provider]["base_url"]


def api_key(provider):
    key_name = PROVIDERS[provider]["key"]
    return os.environ[key_name] if key_name else "ollama"  # Ollama ignores the key


# ---- Plain OpenAI client (weeks 1 and onwards) ----

def client(provider="openrouter"):
    """An OpenAI client pointed at the provider: client("gemini").chat.completions.create(...)"""
    return OpenAI(base_url=base_url(provider), api_key=api_key(provider))


def async_client(provider="openrouter"):
    return AsyncOpenAI(base_url=base_url(provider), api_key=api_key(provider))


# ---- One helper per agent framework ----

def agents_model(provider, model):
    """OpenAI Agents SDK (weeks 2 and 6): Agent(..., model=agents_model("gemini", "gemini-3.8-flash"))"""
    from agents import OpenAIChatCompletionsModel

    return OpenAIChatCompletionsModel(model=model, openai_client=async_client(provider))


def langchain_model(provider, model, **kwargs):
    """LangChain / LangGraph (week 4): use in place of ChatOpenAI(...) or a "openai:..." string."""
    if provider == "anthropic":
        from langchain_anthropic import ChatAnthropic

        return ChatAnthropic(model=model, api_key=api_key(provider), **kwargs)
    if provider == "gemini":  # native client: Gemini 3 tool calls need "thought signatures" passed back
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(model=model, google_api_key=api_key(provider), **kwargs)
    from langchain_openai import ChatOpenAI

    return ChatOpenAI(model=model, base_url=base_url(provider), api_key=api_key(provider), **kwargs)


def pydantic_ai_model(provider, model):
    """Pydantic AI (week 5): Agent(pydantic_ai_model(PROVIDER, MEDIUM), ...)"""
    if provider == "anthropic":
        from pydantic_ai.models.anthropic import AnthropicModel
        from pydantic_ai.providers.anthropic import AnthropicProvider

        return AnthropicModel(model, provider=AnthropicProvider(api_key=api_key(provider)))
    if provider == "gemini":
        from pydantic_ai.models.google import GoogleModel
        from pydantic_ai.providers.google import GoogleProvider

        return GoogleModel(model, provider=GoogleProvider(api_key=api_key(provider)))
    from pydantic_ai.models.openai import OpenAIChatModel
    from pydantic_ai.providers.openai import OpenAIProvider

    return OpenAIChatModel(model, provider=OpenAIProvider(base_url=base_url(provider), api_key=api_key(provider)))


def strands_model(provider, model):
    """AWS Strands (week 5): Agent(model=strands_model(PROVIDER, MEDIUM), ...)"""
    if provider == "anthropic":
        from strands.models.anthropic import AnthropicModel

        return AnthropicModel(client_args={"api_key": api_key(provider)}, model_id=model, max_tokens=16000)
    if provider == "gemini":
        from strands.models.gemini import GeminiModel

        return GeminiModel(client_args={"api_key": api_key(provider)}, model_id=model)
    from strands.models.openai import OpenAIModel

    return OpenAIModel(client_args={"api_key": api_key(provider), "base_url": base_url(provider)}, model_id=model)


def agno_model(provider, model):
    """Agno (week 5): Agent(model=agno_model(PROVIDER, MEDIUM), ...)"""
    if provider == "anthropic":
        from agno.models.anthropic import Claude

        return Claude(id=model, api_key=api_key(provider))
    from agno.models.openai.like import OpenAILike

    return OpenAILike(id=model, api_key=api_key(provider), base_url=base_url(provider))


def maf_client(provider, model):
    """Microsoft Agent Framework (week 5): Agent(client=maf_client(PROVIDER, MEDIUM), ...)"""
    from agent_framework.openai import OpenAIChatCompletionClient

    if provider == "gemini":
        # MAF has no native Gemini client here, and Gemini 3 tool calls fail through Google's
        # OpenAI-compatible endpoint, so reach the same model through OpenRouter instead
        print(f"Note: MAF can't call Gemini tools directly; using google/{model} via OpenRouter (billed to OpenRouter)")
        provider, model = "openrouter", f"google/{model}"
    return OpenAIChatCompletionClient(model=model, api_key=api_key(provider), base_url=base_url(provider))
