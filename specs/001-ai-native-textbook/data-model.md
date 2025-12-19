# Data Model: AI-Native Textbook on Physical AI & Humanoid Robotics

## Entity: TextbookModule
**Description**: Represents a section of the textbook covering specific topics (sensing, perception, planning, control)

**Fields**:
- id: string (unique identifier)
- title: string (module title)
- slug: string (URL-friendly identifier)
- content: string (MDX content)
- category: enum ['foundations', 'ros2-nervous-system', 'digital-twins', 'nvidia-isaac', 'vision-language-action', 'humanoid-control', 'capstone']
- prerequisites: array of string (module IDs that must be completed first)
- learning_objectives: array of string (what students should learn)
- estimated_duration: integer (minutes)
- created_at: datetime
- updated_at: datetime
- is_published: boolean

**Relationships**:
- Has many LabExercise (via lab_exercises.module_id)
- Has many LearningResource (via learning_resources.module_id)

**Validation rules**:
- title must be 3-100 characters
- slug must be unique and URL-friendly
- content must be valid MDX
- category must be one of the defined values

## Entity: LabExercise
**Description**: Represents a hands-on activity with step-by-step instructions, code samples, and expected outcomes for practical learning

**Fields**:
- id: string (unique identifier)
- module_id: string (foreign key to TextbookModule)
- title: string (exercise title)
- description: string (brief description)
- difficulty: enum ['beginner', 'intermediate', 'advanced']
- instructions: string (step-by-step instructions in MDX)
- code_samples: array of object (code examples with language and content)
- expected_outcomes: array of string (what should happen when completed)
- prerequisites: array of string (what knowledge/skills are needed)
- simulation_required: boolean (does this require Gazebo/Isaac?)
- estimated_duration: integer (minutes)
- created_at: datetime
- updated_at: datetime
- is_published: boolean

**Relationships**:
- Belongs to TextbookModule (via module_id)
- Has many LearningResource (via learning_resources.lab_exercise_id)

**Validation rules**:
- title must be 3-100 characters
- module_id must reference existing module
- difficulty must be one of the defined values
- instructions must be valid MDX

## Entity: CapstoneProject
**Description**: Represents the comprehensive final project integrating all textbook concepts into a voice-driven humanoid robot implementation

**Fields**:
- id: string (unique identifier)
- title: string (project title)
- description: string (brief description)
- overview: string (detailed project overview in MDX)
- requirements: array of string (what the project must do)
- voice_integration_required: boolean (does it require voice processing?)
- simulation_components: array of string (simulation elements needed)
- evaluation_criteria: array of string (how the project will be evaluated)
- estimated_duration: integer (hours)
- created_at: datetime
- updated_at: datetime
- is_published: boolean

**Relationships**:
- Has many LearningResource (via learning_resources.capstone_project_id)

**Validation rules**:
- title must be 3-100 characters
- overview must be valid MDX
- requirements must not be empty

## Entity: LearningResource
**Description**: Represents supporting materials including code samples, diagrams, simulation configurations, and documentation

**Fields**:
- id: string (unique identifier)
- title: string (resource title)
- resource_type: enum ['code_sample', 'diagram', 'simulation_config', 'documentation', 'video', 'dataset']
- content: string (the actual resource content or path)
- file_path: string (path to file if external)
- module_id: string (optional, foreign key to TextbookModule)
- lab_exercise_id: string (optional, foreign key to LabExercise)
- capstone_project_id: string (optional, foreign key to CapstoneProject)
- tags: array of string (keywords for search)
- created_at: datetime
- updated_at: datetime
- is_published: boolean

**Relationships**:
- Belongs to TextbookModule (via module_id, optional)
- Belongs to LabExercise (via lab_exercise_id, optional)
- Belongs to CapstoneProject (via capstone_project_id, optional)

**Validation rules**:
- title must be 3-100 characters
- resource_type must be one of the defined values
- Must belong to exactly one of module_id, lab_exercise_id, or capstone_project_id
- If resource_type is 'file', file_path must be provided

## Entity: User
**Description**: Represents a student or AI engineer using the textbook

**Fields**:
- id: string (unique identifier)
- email: string (user's email address)
- name: string (display name)
- role: enum ['student', 'engineer', 'instructor', 'admin']
- created_at: datetime
- updated_at: datetime
- last_login_at: datetime
- is_active: boolean

**Relationships**:
- Has many UserProgress (via user_progress.user_id)
- Has many UserLabSubmission (via user_lab_submissions.user_id)

**Validation rules**:
- email must be valid email format and unique
- name must be 2-50 characters
- role must be one of the defined values

## Entity: UserProgress
**Description**: Tracks a user's progress through the textbook modules

**Fields**:
- id: string (unique identifier)
- user_id: string (foreign key to User)
- module_id: string (foreign key to TextbookModule)
- status: enum ['not_started', 'in_progress', 'completed']
- completion_percentage: integer (0-100)
- started_at: datetime
- completed_at: datetime (nullable)
- last_accessed_at: datetime
- time_spent: integer (seconds)

**Relationships**:
- Belongs to User (via user_id)
- Belongs to TextbookModule (via module_id)

**Validation rules**:
- user_id and module_id combination must be unique
- status must be one of the defined values
- completion_percentage must be between 0 and 100

## Entity: UserLabSubmission
**Description**: Tracks a user's lab exercise submissions and results

**Fields**:
- id: string (unique identifier)
- user_id: string (foreign key to User)
- lab_exercise_id: string (foreign key to LabExercise)
- submission_content: string (user's solution/implementation)
- submission_files: array of object (submitted files with name and path)
- status: enum ['submitted', 'grading', 'graded', 'revised']
- grade: integer (0-100, nullable)
- feedback: string (instructor feedback)
- submitted_at: datetime
- graded_at: datetime (nullable)

**Relationships**:
- Belongs to User (via user_id)
- Belongs to LabExercise (via lab_exercise_id)

**Validation rules**:
- user_id and lab_exercise_id combination must be unique for active submissions
- status must be one of the defined values
- grade must be between 0 and 100 if provided

## Entity: ChatSession
**Description**: Represents a conversation session with the RAG chatbot

**Fields**:
- id: string (unique identifier)
- user_id: string (foreign key to User, nullable for anonymous)
- session_title: string (auto-generated from first query)
- created_at: datetime
- updated_at: datetime
- is_active: boolean

**Relationships**:
- Belongs to User (via user_id, optional)
- Has many ChatMessage (via chat_messages.session_id)

**Validation rules**:
- user_id is optional (for anonymous sessions)
- session_title must be 5-100 characters

## Entity: ChatMessage
**Description**: Represents a single message in a chat session

**Fields**:
- id: string (unique identifier)
- session_id: string (foreign key to ChatSession)
- role: enum ['user', 'assistant']
- content: string (message content)
- context_sources: array of string (which textbook sections were referenced)
- timestamp: datetime
- message_type: enum ['text', 'code', 'diagram', 'error']

**Relationships**:
- Belongs to ChatSession (via session_id)

**Validation rules**:
- role must be one of the defined values
- content must not be empty
- message_type must be one of the defined values

## State Transitions

### UserProgress State Transitions:
- not_started → in_progress (when user starts module)
- in_progress → completed (when user completes module)
- completed → in_progress (if user revisits to review)

### UserLabSubmission State Transitions:
- (new submission) → submitted (when user submits lab)
- submitted → grading (when grading begins)
- grading → graded (when grading completed)
- graded → submitted (if returned for revision)
- submitted → revised (when user resubmits after feedback)