# ./prompt/prompt_builder.py
# Minimal Model-Aware Prompt Wrapper for Kernel Operator
# Created by: David Kistner (GlyphicMind Solutions LLC)



#system imports
import re



# =================================
# PROMPT BUILDER CLASS
# =================================
class PromptBuilder:
    """
    Minimal model-aware prompt wrapper.
    KernelOperator sends a neutral instruction block.
    This class wraps it in the correct chat template.
    """

    # ---------------
    # Initialize
    # ---------------
    def __init__(self, model_key: str):
        """
            Initializes Prompt Builder
        """
        self.model_key = (model_key or "").lower()

    # ----------------
    # Detect Family
    # ----------------
    def _detect_family(self) -> str:
        """
            Detects Model family name for prompting
        """
        key = self.model_key

        if "gemma" in key or "dream" in key:
            return "gemma"

        if "mistral" in key:
            return "mistral"

        if "gpt" in key or "20b" in key:
            return "gpt"

        if "llama" in key or "hermes" in key:
            return "llama"

        if "qwen" in key or "qwencoder" in key:
            return "qwen"

        return "fallback"

    # ----------------
    # Wrap
    # ----------------
    def wrap(self, instruction_block: str, user_text: str) -> str:
        family = self._detect_family()

        # GEMMA
        if family == "gemma":
            return (
                f"<start_of_turn>system\n"
                f"{instruction_block}\n"
                f"<end_of_turn>\n\n"
                f"<start_of_turn>user\n"
                f"{user_text}\n"
                f"<end_of_turn>\n\n"
                f"<start_of_turn>assistant\n"
            )

        # MISTRAL
        if family == "mistral":
            return (
                f"<|im_start|>system\n"
                f"[INST]\n"
                f"{instruction_block}\n"
                f"[/INST]\n"
                f"<|im_end|>\n\n"
                f"<|im_start|>user\n"
                f"{user_text}\n"
                f"<|im_end|>\n\n"
                f"<|im_start|>assistant\n"
            )

        # QWEN / QWEN CODER
        if family == "qwen":
            return (
                f"<|im_start|>system\n"
                f"{instruction_block}\n"
                f"<|im_end|>\n\n"
                f"<|im_start|>user\n"
                f"{user_text}\n"
                f"<|im_end|>\n\n"
                f"<|im_start|>assistant\n"
            )

        # GPT-OSS (requires split output)
        if family == "gpt":
            return (
                f"<|start|>system<|message|>\n"
                f"{instruction_block}\n"
                f"<|end|>\n\n"
                f"<|start|>user<|message|>\n"
                f"{user_text}\n"
                f"<|end|>\n\n"
                f"<|start|>(analysis)assistantanalysis<|message|>\n"
                f"Thinking...\n"
                f"<|end|>\n\n"
                f"<|start|>assistantfinal<|message|>\n"
            )

        # LLAMA / HERMES
        if family == "llama":
            return (
                f"<|im_start|>system\n"
                f"{instruction_block}\n"
                f"<|im_end|>\n\n"
                f"<|im_start|>user\n"
                f"{user_text}\n"
                f"<|im_end|>\n\n"
                f"<|im_start|>assistant\n"
            )

        # FALLBACK (phi-style markdown)
        return (
            f"# SYSTEM\n"
            f"{instruction_block}\n\n"
            f"# USER\n"
            f"{user_text}\n\n"
            f"# ASSISTANT\n"
        )

    # ----------------------------------
    # GPT output splitter
    # ----------------------------------
    @staticmethod
    def split_gpt_oss_output(text: str):
        t = text.replace("\r", "")
        match = re.search(r"\bAnswer:\b", t, re.IGNORECASE)

        if not match:
            return "", t.strip()

        idx = match.start()
        thoughts = t[:idx].replace("Thinking:", "").strip()
        content = t[idx:].replace("Answer:", "").strip()
        return thoughts, content

