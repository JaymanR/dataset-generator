---
title: Dataset Generator
emoji: 🧪
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: "6.10.0"
app_file: app.py
pinned: false
---

# Synthetic Dataset Generator

A Gradio web app that uses LLMs to generate synthetic JSON datasets from a plain-text description. Describe the schema and content you want, choose a model, set the record count, and download the result.

## Features

- Supports multiple LLM providers: OpenAI, Anthropic, Google, and HuggingFace
- Simple prompt-driven interface — no code required
- Outputs a valid JSON array you can download directly

## Supported Models

| Model | Provider |
|---|---|
| GPT-5 Nano | OpenAI |
| GPT-5.4 Mini | OpenAI |
| Claude Haiku 4.5 | Anthropic |
| Gemini 2.5 Flash Lite | Google |
| Qwen3 8B | HuggingFace |
| Qwen3 4B | HuggingFace |

## Setup

**1. Install dependencies**

```bash
uv sync
```

**2. Set API keys**

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key
```

**3. Run the app**

```bash
python app.py
```

Then open the local URL printed in the terminal (e.g. `http://127.0.0.1:7860`).

## Usage

1. Select a model from the dropdown.
2. Set the number of records using the slider (1–500).
3. Describe your dataset in the prompt box. For example:

   ```
   Generate customer support tickets with fields:
   - ticket_id (string)
   - issue (string)
   - priority (low | medium | high)
   - resolved (boolean)
   ```

4. Click **Generate**.
5. Review the JSON output, then click **Download JSON** to save it.

## Project Structure

```
app.py          # Gradio UI and entry point
generator.py    # Core generation logic
config.py       # Model definitions and API client setup
pyproject.toml  # Dependencies
```
