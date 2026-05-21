# ./runtime/validator.py
# Validator for the Kernel Operator
# Created By: David Kistner (Unconditional Love) at GlyphicMind Solutions



# system imports
import json



# =====================================
# PLAN VALIDATOR CLASS
# =====================================
class PlanValidator:
    """
    Validates JSON plans before execution.
    Ensures:
    - valid JSON
    - required fields exist
    - commands are allowed
    - destructive commands are blocked
    """

    REQUIRED_FIELDS = ["plan", "steps"]

    # Allowed commands (creation-only)
    ALLOWED_COMMANDS = [
        "create_file",
        "create_folder",
        "write_file",
        "append_file",
        "copy_file",
        "move_file",
        "download",
        "http_request",
        "run_shell",
        "pip_install",
        "create_virtualenv",
        "install_requirements",
        "scaffold_project"
    ]

    # Explicitly banned destructive commands
    BANNED_COMMANDS = [
        "delete_file",
        "delete_folder",
        "rm",
        "rmdir",
        "unlink",
        "truncate",
        "wipe",
        "format",
        "mkfs",
        "chmod_000"
    ]

    # -------------
    # Validate
    # -------------
    def validate(self, plan_text: str):
        try:
            plan = json.loads(plan_text)
        except Exception as e:
            raise ValueError(f"Invalid JSON: {e}")

        # Required fields
        for field in self.REQUIRED_FIELDS:
            if field not in plan:
                raise ValueError(f"Missing required field: {field}")

        # Steps must be a list
        if not isinstance(plan["steps"], list):
            raise ValueError("Plan 'steps' must be a list.")

        # Validate each step
        for step in plan["steps"]:
            cmd = step.get("command")

            # Missing command
            if not cmd:
                raise ValueError("Step missing 'command' field.")

            # Block destructive commands
            if cmd in self.BANNED_COMMANDS:
                raise ValueError(f"Destructive command not allowed: {cmd}")

            # Ensure command is allowed
            if cmd not in self.ALLOWED_COMMANDS:
                raise ValueError(f"Disallowed command: {cmd}")

        return True
