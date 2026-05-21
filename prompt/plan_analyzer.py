# ./prompt/plan_analyzer.py
# Plan Analyzer for Kernel Operator
# Created By: David Kistner (Unconditional Love) at GlyphicMind Solutions



#local imports
from prompt.prompt_builder import PromptBuilder
from prompt.plan_generator import STRICT_JSON_HEADER



# =========================
# PLAN ANALYZER CLASS
# =========================
class PlanAnalyzer:
    """
    Analyzes an existing plan for correctness and completeness.
    Returns STRICT JSON with analysis.
    """
    # ---------------
    # Initialize
    # ---------------
    def __init__(self, engine, model_key: str):
        """
            Initializes the Plan Analyzer Prompt
        """
        self.engine = engine
        self.builder = PromptBuilder(model_key)

    # ---------------
    # Analyze Plan
    # ---------------
    def analyze_plan(self, plan_text: str) -> str:
        """
            Prompts header, instruction, and plan_text
        """
        instruction = (
            STRICT_JSON_HEADER
            + "\nAnalyze the following plan for correctness, safety, and completeness.\n"
            + "If changes are needed, return a corrected plan in the SAME JSON format.\n"
        )
        prompt = self.builder.wrap(instruction, plan_text)
        return self.engine.generate(prompt)

