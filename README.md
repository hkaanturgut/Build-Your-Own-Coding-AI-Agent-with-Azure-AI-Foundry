# Build Your Own Coding AI Agent with Azure AI Foundry

This repository demonstrates how to build and deploy custom AI coding agents using Azure AI Foundry. These agents are designed to enforce company-specific coding standards, assist development teams, and ensure code quality across different programming languages.

## 🌟 Features

- Custom AI agents for multiple programming languages (Python, Java)
- Automated code standard enforcement
- Integration with Azure AI services
- Vector store-based knowledge base for coding standards
- DevOps task automation capabilities

## 📁 Repository Structure

```
.
├── agents/                     # AI Agent implementation files
│   ├── chat_with_agent.py     # Main agent interaction script
│   ├── chat_with_agent_refactor.py # Refactored version with 
│   ├── java/                  # Java-specific agent setup
│   └── python/                # Python-specific agent setup
├── broken-scripts/            # Example scripts for testing
├── devops_tasks/             # DevOps automation scripts
├── generated_scripts/         # Output directory for generated code
└── instructions/             # Coding standards and instructions
```

## 🚀 Getting Started

### Prerequisites

- Azure subscription
- Azure AI Foundry access
- Python 3.x
- Azure CLI

### Setup

1. Configure Azure credentials:
   - Set up DefaultAzureCredential
   - Configure your Project Connection String

2. Set up language-specific agents:
   ```
   # For Python agent
   python agents/python/python-coding-agent-setup.py

   # For Java agent
   python agents/java/java-coding-agent-setup.py
   ```

## 🔧 Usage

The repository provides two main ways to interact with the AI agents:

1. Code Standard Enforcement:
   - Use `chat_with_agent.py` for real-time code review
   - Submit code for automated standard compliance checks

2. DevOps Task Automation:
   - Utilize `automate_devops_tasks.py` for CI/CD integration
   - Automate code quality checks in your pipeline

## 🤖 How It Works

1. The agents are initialized with language-specific coding standards
2. Standards are stored in vector stores for efficient retrieval
3. When code is submitted, the agent:
   - Analyzes the code against stored standards
   - Suggests improvements
   - Provides educational feedback
   - Can automatically refactor code to meet standards

## 📝 Configuration

Each agent requires:
- Project Connection String
- Model Deployment Name
- Vector Store configuration
- Language-specific standard instructions

## 🔗 Dependencies

- azure.ai.projects
- azure.identity
- Azure AI Foundry services

## 🛠️ Contributing

Contributions are welcome! Please feel free to submit pull requests for:
- Additional language support
- New coding standards
- Improved agent instructions
- Bug fixes and feature enhancements

## 📄 License
MIT License

```
MIT License

Copyright (c) [2025] [Kaan Turgut]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
[]
