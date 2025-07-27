
<div align="center">
<picture>
  <source media="(prefers-color-scheme: light)" srcset="./docs/dark.svg">
  <img alt="spounge-polykey-logo" src="./docs/light.svg" width="50%" height="50%">
</picture>

A node processor for [@Spounge](https://github.com/spounge-ai) that manages execution context via an MCP server and proto contracts, supporting LLM calls, API integrations, database operations, and LangGraph workflow execution. Requires Polykey for secure credential fetching and granting.

[![Status](https://img.shields.io/badge/status-waiting--for--polykey-lightgrey?style=flat)](#)


</div>

## Structural Insight & Execution Flow

Nodus employs a layered architecture for workflow processing:

1.  **Executor Layer (`executors/`):** Executes specific node tasks (Direct, Reasoning, Autonomous, Webhook). Executors are isolated from external service interactions and high-level decision-making.
2.  **Controller Layer (`controllers/`):** Manages orchestration and decision logic. For example, `LLMManager` determines required LLM models or capabilities. This layer delegates external interactions.
3.  **MCP Layer (`mcp/`):** Exposes external tools and services. The `MCPClient` provides an interface for dynamic tool discovery and invocation, centralizing access.
4.  **Integration Layer (`integrations/`):** Contains thin adapters for direct communication with third-party services (APIs, SDKs, LLMs, external infrastructure like `GeminiLLMProvider`, `PolykeyClient`). This layer encapsulates service mechanics without business logic.

**Execution Flow:**
An incoming request is routed to a designated executor. If the executor requires external capabilities (e.g., LLM inference or tool execution), it forwards the request to a controller (e.g., `LLMManager`) or directly to the `MCPClient`. The controller/MCP then utilizes the integration layer to interact with the external service.

## Current Status

Polykey integration: Awaiting full implementation for secure credential fetching and granting.
