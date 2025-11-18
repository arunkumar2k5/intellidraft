# OpenRouter API Integration

## What is OpenRouter?

OpenRouter is a unified API gateway that provides access to multiple AI models from different providers (OpenAI, Anthropic, Google, Meta, etc.) through a single API interface.

## Why OpenRouter Instead of Direct OpenAI?

### 1. **Multiple Model Access**
- Access GPT-3.5, GPT-4, Claude, Llama, and many more models
- Switch between models without changing code
- Compare performance across different models

### 2. **Cost Optimization**
- Choose cheaper models for simple tasks
- Use premium models only when needed
- Pay-as-you-go pricing with competitive rates

### 3. **Reliability**
- Automatic fallback to alternative models if one fails
- Better uptime and availability
- Load balancing across providers

### 4. **Flexibility**
- Single API key for all models
- Easy to experiment with different models
- No vendor lock-in

## Getting Your OpenRouter API Key

1. Visit https://openrouter.ai/
2. Sign up for a free account
3. Go to https://openrouter.ai/keys
4. Create a new API key
5. Copy the key (starts with `sk-or-v1-...`)

## Supported Models

IntelliDraft currently uses `openai/gpt-3.5-turbo` through OpenRouter, but you can easily switch to:

- `openai/gpt-4` - More accurate, higher cost
- `anthropic/claude-3-haiku` - Fast and cost-effective
- `anthropic/claude-3-sonnet` - Balanced performance
- `google/gemini-pro` - Google's model
- `meta-llama/llama-3-8b` - Open source option

## Changing the Model

Edit `backend/services/openai_service.py` and change the model in the payload:

```python
payload = {
    "model": "anthropic/claude-3-haiku",  # Change this line
    "messages": [...],
    ...
}
```

## Pricing

OpenRouter pricing is competitive and transparent:
- GPT-3.5-turbo: ~$0.0005 per 1K tokens
- GPT-4: ~$0.03 per 1K tokens
- Claude-3-haiku: ~$0.00025 per 1K tokens

For component classification (typically 50-100 tokens), costs are minimal:
- ~$0.00005 per classification with GPT-3.5
- ~$0.00001 per classification with Claude-3-haiku

## Free Credits

New OpenRouter accounts often receive free credits to get started. Check your dashboard at https://openrouter.ai/credits

## API Limits

- Rate limits vary by model
- Most models: 60 requests/minute for free tier
- Upgrade to paid tier for higher limits

## Documentation

- OpenRouter Docs: https://openrouter.ai/docs
- Model Comparison: https://openrouter.ai/models
- API Reference: https://openrouter.ai/docs/api-reference

## Benefits for IntelliDraft

1. **Cost-effective**: Use cheaper models for classification
2. **Scalable**: Easy to upgrade to better models as needed
3. **Reliable**: Fallback options if primary model is unavailable
4. **Future-proof**: Access to latest models as they're released

## Example: Switching to Claude

If you want to use Claude-3-haiku instead of GPT-3.5:

1. Edit `backend/services/openai_service.py`
2. Change line 51 from:
   ```python
   "model": "openai/gpt-3.5-turbo",
   ```
   to:
   ```python
   "model": "anthropic/claude-3-haiku",
   ```
3. Restart the backend server

That's it! No other changes needed.

## Monitoring Usage

Track your API usage at: https://openrouter.ai/activity

## Support

- OpenRouter Discord: https://discord.gg/openrouter
- Email: help@openrouter.ai
