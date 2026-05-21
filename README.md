# KernelOperator
### AI‑Driven Planning, Validation & Execution Runtime  

---

## 📘 Overview

KernelOperator is a **local, safe, creation‑only AI planning and execution environment** designed for deterministic, user‑supervised automation.

It provides:

- **LLM‑powered plan generation**  
- **Strict JSON planning format**  
- **Plan analysis & correction**  
- **Plan validation & security enforcement**  
- **Creation‑only execution runtime**  
- **Safe shell, networking, pip, and scaffolding**  
- **A full PyQt5 GUI with 7 coordinated tabs**  
- **Local GGUF model loading via llama.cpp**  

KernelOperator is built for **developers, automation engineers, and AI system architects** who need a safe, predictable, and extensible planning engine.

---

## 🚀 Features

- **Model‑agnostic prompt layer** (Gemma, Llama, Mistral, GPT‑OSS, Qwen)
- **Strict JSON plan generation**
- **Plan analysis & correction using LLM**
- **Creation‑only validator** (no deletion, no overwriting, no destructive ops)
- **SecurityContext** for path safety, shell safety, and network safety
- **PlanLauncher** for safe execution:
  - create_file  
  - create_folder  
  - write_file  
  - append_file  
  - copy_file  
  - move_file  
  - download  
  - http_request  
  - run_shell (safe subset)  
  - pip_install  
  - create_virtualenv  
  - install_requirements  
  - scaffold_project  
- **Full GUI**:
  - Description Tab  
  - RAW Output Tab  
  - Analyze Plan Tab  
  - Planning Tab  
  - Launcher Output Tab  
  - Logs Tab  
  - Settings Tab  
- **Local GGUF model loading** via llama-cpp-python
- **Manifest‑based model registry**

---

## 🧠 Architecture Diagram
```
┌──────────────────────────┐
│      DescriptionTab      │
│    (User writes task)    │
└──────────────┬───────────┘
               │
               ▼
     ┌──────────────────┐
     │  PlanGenerator   │
     │ (LLM produces    │
     │  strict JSON)    │
     └───────┬──────────┘
             │
             ▼
┌────────────────────────┐
│      RawOutputTab      │
│ (Shows raw LLM output) │
└──────────┬─────────────┘
           │
           ▼
┌────────────────────┐
│  AnalyzePlanTab    │
│  PlanAnalyzer LLM  │
└──────────┬─────────┘
           │
           ▼
┌────────────────────┐
│    PlanningTab     │
│ Validator + SecCtx │
└──────────┬─────────┘
           │
           ▼
┌────────────────────┐
│    PlanLauncher    │
│ (Safe execution)   │
└──────────┬─────────┘
           │
           ▼
┌────────────────────┐
│ LauncherOutputTab  │
│ (Streaming logs)   │
└──────────┬─────────┘
           │
           ▼
┌────────────────────┐
│      LogsTab       │
│ (Historical logs)  │
└────────────────────┘
```

---

## 📁 Directory Structure
```
KernelOperator/
│
├── engine/
│   ├── llm_engine.py
│   └── __init__.py
│
├── gui/
│   ├── main_window.py
│   ├── __init__.py
│   ├── tabs/
│   │   ├── description_tab.py
│   │   ├── raw_output_tab.py
│   │   ├── analyze_plan_tab.py
│   │   ├── planning_tab.py
│   │   ├── launcher_output_tab.py
│   │   ├── logs_tab.py
│   │   └── settings_tab.py
│   │   └── __init__.py
│   └── widgets/
│       ├── model_selector_widget.py
│       ├── text_window.py
│       └── __init__.py
│
├── prompt/
│   ├── prompt_builder.py
│   ├── plan_generator.py
│   ├── plan_analyzer.py
│   ├── plan_launcher.py
│   └── __init__.py
│
├── runtime/
│   ├── validator.py
│   ├── security.py
│   ├── launcher.py
│   └── __init__.py
│
├── models/
│   ├── manifest.yaml
│   └── __init__.py
│
├── main.py
├── requirements.txt
└── README.md
```

---

## 🛠 Installation

### 1. Clone the repository


### 2. Create a virtual environment

```
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Place your GGUF models  
Edit:
```
models/manifest.yaml
```
To point to your system‑level `models.yaml`.

### 5. Run the application
```
python main.py
```

---

## 🧩 Usage Flow

### 1. **Select a model**  
Use the Model Selector at the top of the GUI.

### 2. **Describe your task**  
In the Description Tab, write what you want the LLM to plan.

### 3. **Generate a plan**  
The LLM produces strict JSON.

### 4. **Analyze the plan**  
Use AnalyzePlanTab to refine or correct the plan.

### 5. **Validate the plan**  
Paste the final JSON into PlanningTab.

### 6. **Execute safely**  
PlanLauncher runs the plan with:
- no deletion  
- no overwriting  
- no privilege escalation  
- no unsafe shell commands  

### 7. **View logs**  
LauncherOutputTab streams execution logs.  
LogsTab stores historical logs.

---

## 🔒 Safety Architecture

KernelOperator is designed to be **safe by architecture**, not by trust.

### ✔ Creation‑only  
No destructive commands allowed.

### ✔ Strict JSON  
No natural language execution.

### ✔ Validator  
Ensures:
- allowed commands only  
- correct structure  
- no missing fields  

### ✔ SecurityContext  
Prevents:
- path traversal  
- shell injection  
- unsafe networking  
- overwriting files  

### ✔ User‑supervised execution  
Nothing runs without explicit user approval.

---

## 🧭 Roadmap

- Autonomous System Intelligence  
- Multi‑agent orchestration  
- Plugin system  
- Remote sandbox execution  
- Model‑agnostic adapters  
- Full project scaffolding templates  

---

## 📄 License

MIT License

---

## ❤️ Author

**David Kistner (Unconditional Love)**  
GlyphicMind Solutions LLC
