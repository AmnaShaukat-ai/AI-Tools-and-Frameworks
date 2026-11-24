# What is LangChain?

LangChain is an open-source framework used to build applications powered by Large Language Models (LLMs). It helps developers connect and orchestrate multiple components to create complex workflows, such as RAG applications and AI agents.

## Main Components of LangChain

Some of its main components are:

- **Prompt:** Defines the instructions and input format given to the LLM.
- **Model:** The LLM that processes the input and generates a response.
- **Retriever:** Finds relevant documents or information from a data source.
- **Chain:** Connects multiple components into a sequence of steps.
- **Tools:** Functions that allow an LLM or agent to perform specific actions, such as searching products or checking order status.
- **Agent:** Uses an LLM to decide which tools to call and what steps to take to complete a task.

## How Does LangChain Help in RAG?

A typical RAG workflow involves several steps:

1. Loading documents from different sources.
2. Splitting documents into smaller chunks.
3. Generating embeddings for those chunks.
4. Storing embeddings in a vector database.
5. Retrieving relevant information when a user asks a question.
6. Sending the retrieved context to an LLM to generate an answer.

LangChain provides components that connect and manage these steps. It simplifies the development of RAG applications by providing integrations for document loaders, text splitters, embedding models, vector stores, retrievers, and prompts.

However, LangChain is not mandatory for building RAG. Developers can also implement the same workflow using a direct SDK and their own Python code.

## When Should We Use LangChain, and When Should We Avoid It?

**Use LangChain when:**
- An application involves multiple connected components.
- We need to build RAG workflows with document loaders, retrievers, and vector databases.
- We need integrations with different LLM providers and data sources.
- We want to organize complex workflows using reusable components.

**Avoid or reconsider LangChain when:**
- The application only requires a simple LLM API call.
- We need maximum control over API requests and want fewer dependencies.
- The framework adds unnecessary complexity to a simple application.

For structured outputs, the choice depends on the requirements. A direct OpenAI SDK can handle structured outputs, while Pydantic AI is useful when we need typed agent outputs, validation, dependencies, and tool calling.

## How Is LangChain Different from a Direct SDK?

**LangChain:**
- Provides higher-level abstractions to connect and orchestrate multiple components.
- Offers integrations for RAG, tools, retrievers, and different model providers.
- Can reduce the amount of custom orchestration code developers need to write.
- Adds an abstraction layer and may introduce additional dependencies.

**Direct SDK:**
- Provides direct access to a provider's API.
- Gives developers more control over API calls, tool calling, and application logic.
- Is often simpler for applications with straightforward requirements.
- Requires developers to manage more of the workflow themselves.

**Key Difference:** LangChain helps organize and orchestrate complex AI workflows, while a Direct SDK provides a more direct way to interact with an AI provider's APIs, giving developers greater control over implementation.

## Practical Implementation: LangChain Agent with Multiple Tools

In this practical, I used LangChain to create an AI agent that could use multiple Python tools to handle different customer requests.

**Main components used:**

- **`@tool`:** Used to convert Python functions into tools that the agent can call.
- **`create_agent`:** Used to create an agent that can decide which tools to use based on the user's request.
- **Python tool functions:** Implemented specific actions that the agent could perform.

**How it works:**

1. Python functions are defined for specific tasks.
2. The `@tool` decorator registers these functions as tools.
3. The tools are passed to `create_agent`.
4. The user sends a query to the agent.
5. The LLM decides which tool or tools are relevant.
6. LangChain executes the selected tools and provides their results to the agent.
7. The agent generates a final response using the tool results.

**Key Learning:**

I learned how LangChain connects Python functions with an AI agent and allows the agent to select and use multiple tools according to the user's request.

This practical demonstrated tool integration and agent orchestration using LangChain.