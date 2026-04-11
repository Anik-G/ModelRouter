# 🚀 Model Router for Azure OpenAI with Python

![ModelRouter Header](https://github.com/Anik-G/ModelRouter/blob/main/ss/query.gif)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![Gradio](https://img.shields.io/badge/Gradio-UI%20App-purple?logo=gradio)](https://gradio.app/)
[![Azure OpenAI](https://img.shields.io/badge/Azure%20OpenAI-Model%20Router-blueviolet?logo=microsoftazure)](https://aka.ms/ModelRouter)

![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Roboto+Mono&size=26&pause=1000&color=2A9DFF&width=780&lines=Azure+Model+Router+Demo;Live+Gradio+Frontend;Intelligent+Model+Selection)

## Overview

Azure OpenAI Model Router is a smart routing layer that chooses the best underlying LLM for each request in real time. This repository shows how to use Model Router from Python, including:

- a Foundry-style sample script
- a live Gradio app with streaming conversation
- model diagnostics and usage reporting

Model Router evaluates prompt complexity, cost, and latency to route requests to the most appropriate backend model. That means you can:

- use smaller, cheaper models when they are enough
- reserve larger, more capable models for harder tasks
- avoid extra routing fees (you only pay for the underlying model usage)

> Model Router helps you optimize both cost and quality with transparent model selection.

## Why this repo?

This repo makes it easy to experiment with Azure OpenAI Model Router using Python.

- ✅ Clean `model-router-foundry-sample.py` demo
- ✅ Interactive `model-router-gradio-app.py` with model details
- ✅ Built to run from a `.env` file using `python-dotenv`
- ✅ Ready for quick customization and production exploration

## Key Features

- Intelligent model selection for optimal cost and quality
- Transparent routing with model metadata shown in the app
- Supports conversational streaming output
- Easy setup using environment variables
- Includes sample Gradio UI for immediate testing

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/Anik-G/ModelRouter.git
cd ModelRouter
```

### 2. (Optional) Create a Python virtual environment

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Azure credentials

Create a `.env` file in the repository root and add your Azure OpenAI settings.

```env
AZURE_OPENAI_API_ENDPOINT=https://<your-resource-name>.openai.azure.com/
AZURE_OPENAI_API_KEY=<your-api-key>
AZURE_OPENAI_API_VERSION=2024-06-01-preview
AZURE_OPENAI_API_MODEL=<your-model-router-deployment-name>
```

This repo uses `load_dotenv()` to load configuration automatically.

### 5. Verify the connection

```python
import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()
endpoint = os.environ["AZURE_OPENAI_API_ENDPOINT"]
deployment = os.environ["AZURE_OPENAI_API_MODEL"]
subscription_key = os.environ["AZURE_OPENAI_API_KEY"]
api_version = os.environ["AZURE_OPENAI_API_VERSION"]

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)
```

### 6. Run a sample script

```bash
python3 model-router-foundry-sample.py
```

<img width="1047" height="775" alt="Screenshot 2026-04-11 111202" src="https://github.com/user-attachments/assets/fa6f74f3-1b72-43f4-8f0e-715d5706ee10" />


### 7. Launch the Gradio app

```bash
python3 model-router-gradio-app.py
```

![Model Router UI](https://github.com/Anik-G/ModelRouter/blob/main/ss/query.gif)

## Recommended Usage

- Start with `model-router-foundry-sample.py` to understand the API flow.
- Use `model-router-gradio-app.py` for interactive chat and live model tracking.
- Update the sample prompts to match your business domain.
- Check the model name and type in the app to confirm routing behavior.

## Notes

- The Gradio app shows the selected model and its classification.
- Model Router does not charge extra routing fees; only the underlying model usage is billed.
- For production, validate your deployment name and API version carefully.

## Useful Links

- [Model Router Documentation (Microsoft Learn)](https://aka.ms/ModelRouter)
- [Supported Models](https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/model-router#supported-underlying-models)
- [Azure AI Foundry Blog](https://azure.microsoft.com/en-us/blog/the-latest-azure-ai-foundry-innovations-help-you-optimize-ai-investments-and-differentiate-your-business/)

---

## License

MIT License
