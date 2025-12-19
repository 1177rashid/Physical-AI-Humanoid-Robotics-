# Research: AI-Native Textbook on Physical AI & Humanoid Robotics

## Architecture Decisions

### 1. Docusaurus vs Other Static Site Generators
**Decision**: Use Docusaurus
**Rationale**:
- Native MDX support for rich content integration
- Built-in versioning capabilities for textbook updates
- Strong plugin ecosystem for search, analytics, and custom components
- GitHub Pages deployment compatibility
- Mermaid diagram integration out of the box

**Alternatives considered**:
- Next.js with MDX: More complex setup, less educational-focused
- GitBook: Less customizable, limited versioning
- Hugo: Less MDX support, more complex templating

### 2. GitHub Pages vs Vercel
**Decision**: Use GitHub Pages
**Rationale**:
- Cost-free hosting aligned with educational mission
- Tight integration with GitHub workflow
- Sufficient performance for static content delivery
- No vendor lock-in concerns

**Alternatives considered**:
- Vercel: Better performance metrics but has cost implications
- Netlify: Similar to Vercel, but less GitHub integration

### 3. Simulation-first vs Sim-to-Real
**Decision**: Simulation-first approach with sim-to-real pathways
**Rationale**:
- Provides accessible learning environment for all students
- Reduces hardware requirements for initial learning
- Enables safe experimentation with humanoid robotics
- Clear pathway to real hardware when available

**Alternatives considered**:
- Sim-to-real: Requires expensive hardware upfront
- Real-hardware only: Not accessible to all learners

### 4. Cloud GPU vs On-prem RTX
**Decision**: Cloud GPU resources for compute-intensive tasks
**Rationale**:
- Cost-effective OpEx model vs CapEx for on-prem hardware
- Scalable resources for varying demand
- Accessibility for all learners regardless of local hardware
- Maintenance handled by cloud provider

**Alternatives considered**:
- On-prem RTX: Higher upfront costs, maintenance burden
- Hybrid: Complex to manage, limited benefit for educational use

### 5. On-device vs Remote LLM Planning
**Decision**: Remote LLM planning via API
**Rationale**:
- Consistent performance regardless of user hardware
- Access to latest models and capabilities
- Centralized management and updates
- Better for RAG implementation

**Alternatives considered**:
- On-device: Limited by user hardware, model constraints

## Technology Stack Research

### Docusaurus Implementation
- MDX support for interactive content and code examples
- Plugin architecture for custom textbook features
- Built-in search and navigation capabilities
- Responsive design for multiple device types

### RAG Implementation
- FastAPI backend for RAG services
- OpenAI Agents/ChatKit for conversational interface
- Qdrant for vector storage of textbook content
- Neon Postgres for metadata and user data

### ROS 2 Integration
- rclpy for Python ROS 2 client library
- Ubuntu 22.04 LTS for stability
- ROS 2 Humble/H Iron for long-term support
- Integration with Gazebo simulation environment

### NVIDIA Isaac Integration
- Isaac ROS for perception and navigation
- GPU acceleration for real-time processing
- Integration with Vision-Language-Action models
- Simulation-to-real transfer capabilities

## Content Structure Research

### Section Organization
Based on research of effective robotics education approaches:
1. Foundations: Core concepts and mathematical background
2. ROS 2 Nervous System: Communication and control architecture
3. Digital Twins: Simulation and modeling concepts
4. NVIDIA Isaac: Advanced perception and control
5. Vision-Language-Action: Multimodal AI integration
6. Humanoid Control: Specialized locomotion and manipulation
7. Capstone: Voice-driven humanoid implementation

## Quality Validation Research

### Learning Outcomes Assessment
- Chapter objectives aligned with measurable outcomes
- Practical labs with verifiable results
- Diagram accuracy verification through peer review
- End-to-end pipeline validation with simulation

### Testing Strategy Research
- Chapter validation against stated objectives
- ROS 2 Python examples verified in simulation
- Mermaid diagrams validated against system architecture
- RAG chatbot responses constrained to indexed book content
- Capstone validates complete voice → plan → navigate → manipulate flow