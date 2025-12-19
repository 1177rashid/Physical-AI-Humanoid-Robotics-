# Implementation Plan: AI-Native Textbook on Physical AI & Humanoid Robotics

**Branch**: `001-ai-native-textbook` | **Date**: 2025-12-18 | **Spec**: [specs/001-ai-native-textbook/spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-ai-native-textbook/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Create a Docusaurus MDX textbook deployed on GitHub Pages with embedded RAG chatbot (FastAPI + OpenAI Agents/ChatKit + Qdrant + Neon Postgres) covering Physical AI & Humanoid Robotics. The textbook will have a modular structure: Foundations → ROS 2 Nervous System → Digital Twins → NVIDIA Isaac → Vision-Language-Action → Humanoid Control → Capstone, with hands-on labs and a voice-driven humanoid capstone project.

## Technical Context

**Language/Version**: Python 3.11, JavaScript/TypeScript for frontend, Docusaurus MDX
**Primary Dependencies**: Docusaurus, FastAPI, OpenAI Agents/ChatKit, Qdrant, Neon Postgres, ROS 2 (Humble/Iron), rclpy, Gazebo, NVIDIA Isaac
**Storage**: Neon Serverless Postgres for user data, Qdrant for vector storage, GitHub Pages for static content
**Testing**: pytest for backend, Jest for frontend, >=80% coverage requirement
**Target Platform**: Ubuntu 22.04, Web browser (GitHub Pages), ROS 2 ecosystem
**Project Type**: Web application with static site generator and backend API services
**Performance Goals**: <5s chatbot response time, <3s content load time, support 1000 concurrent users
**Constraints**: Free-tier services where mandated, secure API handling, responsive design, embedded chatbot UI with selected-text support
**Scale/Scope**: Educational platform supporting up to 1000 concurrent users during peak usage

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Pre-Design Check (Passed)
1. **Clarity for Intermediate AI Developers**: All concepts and implementations must be accessible and well-documented for advanced students and AI engineers
2. **Accuracy and Reproducibility**: All implementations must be reproducible and reliable for real-world applications
3. **Security-First Approach**: Secure handling of APIs, databases, and user data as a foundational requirement
4. **Seamless RAG Integration**: RAG chatbot capabilities must support both full-book and selected-text queries with optimal performance
5. **Spec-Driven Development Adherence**: Strictly adhere to spec-driven development methodology and project requirements
6. **Locked Tech Stack Compliance**: Adhere to the locked technology stack: Docusaurus MDX, FastAPI, OpenAI Agents/ChatKit, Neon Postgres, Qdrant, GitHub Pages

### Post-Design Check (Current Status)
1. ✅ **Clarity for Intermediate AI Developers**: Docusaurus MDX with detailed documentation and examples addresses this requirement
2. ✅ **Accuracy and Reproducibility**: ROS 2 (Humble/Iron) with rclpy, Gazebo simulation, and NVIDIA Isaac provide reproducible environment
3. ✅ **Security-First Approach**: Authentication service and secure API handling implemented in backend design
4. ✅ **Seamless RAG Integration**: FastAPI backend with Qdrant vector store and OpenAI Agents/ChatKit SDK addresses this requirement
5. ✅ **Spec-Driven Development Adherence**: All design decisions align with feature specification requirements
6. ✅ **Locked Tech Stack Compliance**: All technologies match the constitution-specified stack (Docusaurus, FastAPI, OpenAI Agents/ChatKit, Neon Postgres, Qdrant, GitHub Pages)

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-native-textbook/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Web application with Docusaurus frontend and FastAPI backend
docs/
├── src/
│   ├── components/
│   ├── pages/
│   └── theme/
├── docs/
│   ├── foundations/
│   ├── ros2-nervous-system/
│   ├── digital-twins/
│   ├── nvidia-isaac/
│   ├── vision-language-action/
│   ├── humanoid-control/
│   └── capstone/
├── static/
│   ├── img/
│   └── examples/
├── docusaurus.config.js
├── sidebars.js
└── package.json

backend/
├── src/
│   ├── models/
│   │   ├── textbook_module.py
│   │   ├── lab_exercise.py
│   │   ├── capstone_project.py
│   │   └── learning_resource.py
│   ├── services/
│   │   ├── rag_service.py
│   │   ├── chatbot_service.py
│   │   ├── content_service.py
│   │   └── auth_service.py
│   ├── api/
│   │   ├── v1/
│   │   │   ├── textbook.py
│   │   │   ├── chat.py
│   │   │   ├── labs.py
│   │   │   └── capstone.py
│   │   └── main.py
│   └── utils/
│       ├── vectorizer.py
│       └── security.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/
├── requirements.txt
└── main.py

history/
├── prompts/
│   └── ai-native-textbook/
└── adr/

.specify/
├── memory/
├── scripts/
└── templates/
```

**Structure Decision**: Selected web application structure with Docusaurus frontend for textbook content and FastAPI backend for RAG chatbot and dynamic services. The docs/ directory contains the Docusaurus site with textbook content organized by topic, while the backend/ directory contains the API services for chatbot, authentication, and dynamic content delivery.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
