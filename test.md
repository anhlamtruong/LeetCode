flowchart TD
User([Staff User]) --> |Inputs NL Query & Pre-prompt Questionnaire| UI[Frontend Interface]
UI --> |Displays Mandatory Disclaimer| User

    subgraph Dual_AI_Architecture [Dual-AI Backend]
        UI --> |Raw Request + User Context| ValService[Validation Service \n AI + Rule-based Logic]

        %% Auditing branch
        ValService --> |Pipes Report Action| PubSub[Pub/Sub Queue]
        PubSub --> Audit[(Permanent Audit Log)]

        %% Validation logic
        ValService --> |Evaluates Prompt| RBAC{RBAC & Permissions Check}
        RBAC -- Unauthorized --> Block[Block Request / Filter Columns]
        RBAC -- Authorized --> EdgeCheck[Process Edge Cases \n e.g., Unfinalized Data]

        %% AI Engine
        EdgeCheck --> |Structured JSON Payload| AIEngine[On-Premise AI Engine \n DeepSeek + Ollama]
    end

    subgraph Data_Layer [Database Layer]
        AIEngine --> |Executes Read-Only SQL| RDS[(Amazon RDS PostgreSQL \n SIS / LMS Data)]
        RDS --> |Raw Data Results| AIEngine
    end

    AIEngine --> |Returns Report + Automated Disclaimers| UI
