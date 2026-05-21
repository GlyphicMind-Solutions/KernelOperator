# ./prompt/plan_launcher.py
# Plan Launcher Prompt Layer for Kernel Operator
# Created By: David Kistner (Unconditional Love) at GlyphicMind Solutions



#local imports
from prompt.prompt_builder import PromptBuilder
from prompt.plan_generator import STRICT_JSON_HEADER



# ======================================
# PLAN LAUNCHER PROMPT CLASS
# ======================================
class PlanLauncherPrompt:
    """
    Builds an execution-focused instruction block.
    The LLM should return ONLY the final execution JSON (same schema).
    """
    # ---------------
    # Initialize
    # ---------------
    def __init__(self, engine, model_key: str):
        """
            Initialize Plan Launcher Prompt Class
        """
        self.engine = engine
        self.builder = PromptBuilder(model_key)

    # ---------------
    # Initialize
    # ---------------
    def refine_for_execution(self, plan_text: str) -> str:
        """
            Optional: let the model refine/normalize a plan before runtime execution.
            Still returns strict JSON with the same schema.
        """
        instruction = (
            STRICT_JSON_HEADER
            + "\nNormalize and finalize the following plan for execution.\n"
            + "Ensure all commands and args are valid and consistent.\n"
        )
        prompt = self.builder.wrap(instruction, plan_text)
        return self.engine.generate(prompt)

