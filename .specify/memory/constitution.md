<!--
Sync Impact Report:
- Version change: N/A → 1.0.0 (initial constitution creation)
- Added principles:
  1. Clarity for Intermediate AI Developers
  2. Accuracy and Reproducibility
  3. Security-First Approach
  4. Seamless RAG Integration
  5. Spec-Driven Development Adherence
  6. Locked Tech Stack Compliance
- Added sections: Technical Standards and Constraints, Development Workflow and Quality Assurance
- Templates requiring updates: ✅ No template updates required - templates use generic placeholders
- Follow-up TODOs: None
-->
# Docusaurus Book with Integrated RAG Chatbot Constitution

## Core Principles

### Clarity for Intermediate AI Developers
Provide step-by-step guidance and clear explanations for intermediate AI developers, ensuring all concepts and implementations are accessible and well-documented.

### Accuracy and Reproducibility
Maintain production-ready code with strict accuracy, ensuring all implementations are reproducible and reliable for real-world applications.

### Security-First Approach
Implement secure handling of APIs, databases, and user data as a foundational requirement in all system designs and implementations.

### Seamless RAG Integration
Ensure seamless integration of RAG chatbot capabilities supporting both full-book and selected-text queries with optimal performance.

### Spec-Driven Development Adherence
Strictly adhere to spec-driven development methodology and project requirements throughout the implementation lifecycle.

### Locked Tech Stack Compliance
Adhere to the locked technology stack without deviations, utilizing specified tools and services exclusively as defined in project requirements.

## Technical Standards and Constraints
Content: Docusaurus MDX with Mermaid diagrams, testable code blocks, and chapter summaries. Code: TypeScript/Python, error handling, logging, input validation, inline comments. RAG stack: OpenAI Agents/ChatKit SDKs, FastAPI backend, Neon Serverless Postgres, Qdrant Cloud Free Tier. Testing: ≥80% backend coverage (pytest), frontend component tests, E2E RAG accuracy. Deployment: GitHub Pages for site, serverless-compatible backend. Constraints: Free-tier only where mandated, Chatbot response time < 5s, Responsive, embedded UI with selected-text support.

## Development Workflow and Quality Assurance
Implementation workflow: Content-first approach with Docusaurus MDX, followed by RAG backend integration. Review process: Code reviews must verify security practices, performance requirements, and spec compliance. Quality gates: All code must pass security scanning, performance benchmarks (response time < 5s), and achieve ≥80% test coverage before merging.

## Governance
All implementations must comply with the specified tech stack requirements. Changes to the technology stack require formal amendment to this constitution. All PRs/reviews must verify compliance with security standards, performance requirements, and architectural constraints. All features must be tested for both general and selected-text chatbot modes.

**Version**: 1.0.0 | **Ratified**: 2025-12-16 | **Last Amended**: 2025-12-16