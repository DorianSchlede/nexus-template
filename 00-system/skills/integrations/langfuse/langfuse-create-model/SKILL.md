---
name: langfuse-create-model
description: "Create a model definition for cost tracking. Load when user says 'create model', 'add model', 'new model'."
---

# Create Model

Create a new model definition for cost tracking.

## Usage

```bash
python scripts/create_model.py --name "gpt-4o-mini" --match-pattern "gpt-4o-mini.*" --input-price 0.00015 --output-price 0.0006
python scripts/create_model.py --name "claude-3-opus" --match-pattern "claude-3-opus.*" --unit "TOKENS" --input-price 0.015 --output-price 0.075
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--name` | Yes | Model name |
| `--match-pattern` | Yes | Regex pattern to match model names |
| `--unit` | No | TOKENS or CHARACTERS (default: TOKENS) |
| `--input-price` | No | Input price per unit |
| `--output-price` | No | Output price per unit |
| `--total-price` | No | Total price (if not split) |
| `--tokenizer` | No | Tokenizer: openai, claude, none |

## API Reference

```
POST /api/public/models
```
