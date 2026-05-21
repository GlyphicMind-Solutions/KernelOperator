# ./prompt/plan_generator.py
# Plan Generator for Kernel Operator
# Created By: David Kistner (Unconditional Love) at GlyphicMind Solutions



#local imports
from prompt.prompt_builder import PromptBuilder


#--- Prompt Header ---#
STRICT_JSON_HEADER = """# INSTRUCTION
You must output ONLY a valid JSON object that the Kernel Operator system can execute.
Do NOT output any natural language, explanations, commentary, markdown, or code fences.
Do NOT wrap the JSON in backticks.
Do NOT include any text before or after the JSON.
Return ONLY the JSON object.

The JSON MUST have this structure:

{
  "plan": "High-level natural language summary of what you will do.",
  "steps": [
    {
      "command": "one of: create_file, create_folder, write_file, append_file, copy_file, move_file, download, http_request, run_shell, pip_install, create_virtualenv, install_requirements, scaffold_project",
      "args": {
        "...": "command-specific arguments"
      }
    }
  ]
}
"""



# ======================================
# PLAN GENERATOR CLASS
# ======================================
class PlanGenerator:
    """
    Generates a creation-only execution plan as strict JSON.
    """
    # -------------
    # Initialize
    # -------------
    def __init__(self, engine, model_key: str):
        """
            Initalizes the Plan Generator Prompt
        """
        self.engine = engine
        self.builder = PromptBuilder(model_key)

    # ---------------
    # Generate Plan
    # ---------------
    def generate_plan(self, description: str) -> str:
        """
            prompts header, plus user description to the LLM
        """
        instruction = (
            STRICT_JSON_HEADER
            + "\nGenerate a plan for the following description:\n"
        )
        prompt = self.builder.wrap(instruction, description)
        return self.engine.generate(prompt)

