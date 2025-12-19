---
description: "Task list for AI-Native Textbook on Physical AI & Humanoid Robotics implementation"
---

# Tasks: AI-Native Textbook on Physical AI & Humanoid Robotics

**Input**: Design documents from `/specs/001-ai-native-textbook/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/`
- Paths shown below follow the structure from plan.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure with frontend/ and backend/ directories
- [x] T002 Initialize Docusaurus project in frontend/ directory with MDX support
- [x] T003 [P] Initialize Python project in backend/ with FastAPI dependencies in requirements.txt
- [x] T004 [P] Configure linting and formatting tools for Python (black, flake8) and JavaScript (ESLint, Prettier)
- [x] T005 Set up GitHub Pages deployment configuration for frontend/
- [x] T006 Create docker-compose.yml for local development with Qdrant and Postgres

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T007 Setup database schema and migrations framework for Neon Postgres in backend/src/models/
- [x] T008 [P] Implement authentication/authorization framework in backend/src/services/auth_service.py
- [x] T009 [P] Setup API routing and middleware structure in backend/src/api/main.py
- [x] T010 Create base models/entities that all stories depend on in backend/src/models/
- [x] T011 [P] Setup RAG service infrastructure with Qdrant integration in backend/src/services/rag_service.py
- [x] T012 Configure error handling and logging infrastructure in backend/src/utils/
- [x] T013 Setup environment configuration management in backend/src/config/
- [x] T014 Create basic Docusaurus theme and component structure in frontend/src/components/

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Access Interactive Learning Content (Priority: P1) 🎯 MVP

**Goal**: Enable users to navigate through modular content covering sensing, perception, planning, and control systems for humanoid robots using ROS 2, Gazebo, NVIDIA Isaac, and Vision-Language-Action models

**Independent Test**: Verify users can navigate through textbook content modules and access information about physical AI and humanoid robotics concepts, delivering core educational value

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T015 [P] [US1] Contract test for /textbook/modules endpoint in backend/tests/contract/test_textbook.py
- [x] T016 [P] [US1] Integration test for textbook module retrieval in backend/tests/integration/test_textbook.py

### Implementation for User Story 1

- [x] T017 [P] [US1] Create TextbookModule model in backend/src/models/textbook_module.py
- [x] T018 [P] [US1] Create LearningResource model in backend/src/models/learning_resource.py
- [x] T019 [US1] Implement TextbookService in backend/src/services/content_service.py (depends on T017, T018)
- [x] T020 [US1] Implement /textbook/modules endpoints in backend/src/api/v1/textbook.py
- [x] T021 [US1] Implement /textbook/modules/{id} endpoint in backend/src/api/v1/textbook.py
- [x] T022 [US1] Implement /textbook/modules/{id}/resources endpoint in backend/src/api/v1/textbook.py
- [x] T023 [US1] Add validation and error handling for textbook endpoints
- [x] T024 [US1] Create Docusaurus components for textbook module display in frontend/src/components/TextbookModule.tsx
- [x] T025 [US1] Set up basic textbook content structure in frontend/docs/ with initial MDX files
- [x] T026 [US1] Integrate backend API calls into Docusaurus frontend for textbook content
- [x] T027 [US1] Add Mermaid diagram support in Docusaurus for visual representation of concepts

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Complete Hands-on Labs (Priority: P2)

**Goal**: Enable users to practice implementing embodied AI systems by working through hands-on lab exercises that guide them through ROS 2, Gazebo simulation, and NVIDIA Isaac tools with Python (rclpy) code examples

**Independent Test**: Verify users can access, follow, and complete hands-on lab exercises with accompanying code samples, delivering practical learning value

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [x] T028 [P] [US2] Contract test for /textbook/modules/{id}/labs endpoint in backend/tests/contract/test_labs.py
- [x] T029 [P] [US2] Integration test for lab exercise retrieval and submission in backend/tests/integration/test_labs.py

### Implementation for User Story 2

- [x] T030 [P] [US2] Create LabExercise model in backend/src/models/lab_exercise.py
- [x] T031 [P] [US2] Create UserLabSubmission model in backend/src/models/user_lab_submission.py
- [x] T032 [US2] Implement LabService in backend/src/services/content_service.py (depends on T030)
- [x] T033 [US2] Implement /textbook/modules/{id}/labs endpoint in backend/src/api/v1/labs.py
- [x] T034 [US2] Implement /labs/submit endpoint in backend/src/api/v1/labs.py
- [x] T035 [US2] Implement user lab submission tracking in backend/src/api/v1/labs.py
- [x] T036 [US2] Add validation and error handling for lab endpoints
- [x] T037 [US2] Create Docusaurus components for lab exercise display in frontend/src/components/LabExercise.tsx
- [x] T038 [US2] Implement lab exercise integration with textbook modules in frontend/
- [x] T039 [US2] Add Python code sample rendering with syntax highlighting in frontend/
- [x] T040 [US2] Create lab submission interface in frontend for code submission and feedback

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Build Voice-Driven Capstone Project (Priority: P3)

**Goal**: Enable users to apply their learning by developing an autonomous humanoid robot as a capstone project with comprehensive guidance integrating all textbook concepts into a unified project involving voice commands and VLA models

**Independent Test**: Verify users can follow the capstone project guidelines and successfully implement voice-driven humanoid robot functionality, delivering demonstration of comprehensive understanding

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [x] T041 [P] [US3] Contract test for capstone project endpoints in backend/tests/contract/test_capstone.py
- [x] T042 [P] [US3] Integration test for capstone project functionality in backend/tests/integration/test_capstone.py

### Implementation for User Story 3

- [x] T043 [P] [US3] Create CapstoneProject model in backend/src/models/capstone_project.py
- [x] T044 [P] [US3] Create ChatSession and ChatMessage models in backend/src/models/
- [x] T045 [US3] Implement CapstoneService in backend/src/services/content_service.py (depends on T043)
- [x] T046 [US3] Implement ChatbotService with RAG integration in backend/src/services/chatbot_service.py (depends on T044)
- [x] T047 [US3] Implement /chat endpoints in backend/src/api/v1/chat.py
- [x] T048 [US3] Implement /chat/session endpoints in backend/src/api/v1/chat.py
- [x] T049 [US3] Add voice command processing capabilities in backend/src/services/chatbot_service.py
- [x] T050 [US3] Create Docusaurus components for capstone project display in frontend/src/components/CapstoneProject.tsx
- [x] T051 [US3] Integrate RAG chatbot into textbook interface in frontend/
- [x] T052 [US3] Implement capstone project guidance workflow in frontend
- [x] T053 [US3] Add voice input integration for voice-driven interactions

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T054 [P] Documentation updates in frontend/
- [ ] T055 User progress tracking implementation across all stories in backend/src/models/user_progress.py and frontend
- [ ] T056 Performance optimization for content loading and RAG responses
- [ ] T057 [P] Additional unit tests in backend/tests/unit/ and frontend/tests/
- [ ] T058 Security hardening for user authentication and content protection
- [ ] T059 Run quickstart.md validation
- [ ] T060 Setup comprehensive logging and monitoring for production deployment
- [ ] T061 Implement graceful degradation when simulation environments unavailable (FR-015)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for /textbook/modules endpoint in backend/tests/contract/test_textbook.py"
Task: "Integration test for textbook module retrieval in backend/tests/integration/test_textbook.py"

# Launch all models for User Story 1 together:
Task: "Create TextbookModule model in backend/src/models/textbook_module.py"
Task: "Create LearningResource model in backend/src/models/learning_resource.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence