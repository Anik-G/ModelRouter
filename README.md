# Model Router for Azure OpenAI
![ModelRouter](https://github.com/user-attachments/assets/149f9204-68b6-4795-8992-09d3f0488a39)

![ModelRouter](https://github.com/Anik-G/ModelRouter/blob/main/ss/IMG-20260411-WA0001.jpg)
![ModelRouter](https://github.com/Anik-G/ModelRouter/blob/main/ss/IMG-20260411-WA0000.jpg)

## Overview

The Model Router feature within Azure OpenAI is a deployable model trained to select the best large language model (LLM) to respond to a given prompt in real time. By assessing factors such as prompt complexity, cost, and performance, Model Router dynamically routes requests to the most suitable underlying model. This approach helps you optimize both cost and quality: smaller, more efficient models are used when possible, while larger, more capable models are chosen when needed.

Key features of the Model Router include:
- Intelligent model selection for optimal cost and quality
- Transparent versioning with fixed underlying model sets per release
- Support for vision-enabled chats (image input)
- No additional charges for routing—you're billed only for the usage of underlying models

For more details, see the [official documentation](https://aka.ms/ModelRouter).

---

## Python Samples

This repository provides ready-to-use Python samples demonstrating how to interact with the Model Router feature in Azure OpenAI. The sample `model-router-foundrysample.py` is based on the getting started code from Azure AI Foundry. The sample `model-router-gradio.py` provides a Gradio front end to the sample, and exposes the chosen model at the top.

### Getting Started

1. **Clone this repository:**
   ```bash
   git clone https://github.com/Anik-G/ModelRouter.git
   cd ModelRouter
   ```

1.1. **Optional Pre requisits:**
   ```bash
   python3 --version
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies:**
   Most samples require `azure-ai-openai` and related libraries. Install with:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your Azure credentials:**
   - Set the `AZURE_OPENAI_API_KEY` and `AZURE_OPENAI_API_ENDPOINT` environment variables as described in the [Azure OpenAI documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/quickstart?tabs=python).

   - update below environ variables to .env file to the root directory./ModelRouter . Code will use load_dotenv() to load .env file.

```bash
import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

endpoint = os.environ["AZURE_OPENAI_API_ENDPOINT"]
deployment = os.environ["AZURE_OPENAI_API_MODEL"]
subscription_key = os.environ["AZURE_OPENAI_API_KEY"]
api_version = os.environ["AZURE_OPENAI_API_VERSION"]
```


4. **Run a sample:**
   - Review the individual Python scripts in this repo, and use whichever is the best fit for your need:
  
   - Sample code test

   For example:
   ```bash
   python3 model-router-foundry-sample.py
   ```

   - Gradio App for Model Router from Any host 
   
   With Gradio Python WebApp : For example:
   ```bash
   python3 model-router-gradio-app.py
   ```
5. **Review and adapt:**
   - Modify the samples (user_messages) to fit your use case and deployment.

---

## Useful Links

- [Model Router Documentation (Microsoft Learn)](https://aka.ms/ModelRouter)
- [Supported Models](https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/model-router#supported-underlying-models)
- [Microsoft - Optimize your GenAI applications at scale in Azure AI Foundry](https://azure.microsoft.com/en-us/blog/the-latest-azure-ai-foundry-innovations-help-you-optimize-ai-investments-and-differentiate-your-business/)
