# novelGPT - README.md

**novelGPT** is a Python package designed to assist with large-scale novel writing projects using OpenAI's GPT technology. It facilitates the breakdown of novel-writing tasks into manageable parts and uses AI to generate content based on user specifications. It surpasses openAI token response limit through recursive calling.

## Features
- **Clarification Process:** Interactively clarifies the user’s requests to ensure accurate content generation.
- **Task Breakdown:** Splits novel writing into specific sections, assigning manageable tasks to AI.
- **Automated Writing:** Uses GPT-4o mini to generate specific sections of a novel based on detailed prompts.
- **Content Saving:** Outputs generated content to a text file for easy access and editing.

## Installation
To install the package, use the follow instructions:

```bash
git clone https://github.com/AlexCerullo/novelGPT.git
cd novelGPT
pip install -r requirements.txt

**Note: Create file named api.env, and paste the following (with your openAI key)
OPENAI_API_KEY=sk-...