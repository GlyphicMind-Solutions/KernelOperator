# ./runtime/security.py
# Security Context for Kernel Operator
# Created By: David Kistner (Unconditional Love) at GlyphicMind Solutions



# system imports
import os, json



# =====================================
# SECURITY CONTEXT CLASS
# =====================================
class SecurityContext:
    """
    Performs safety checks on plans.
    Prevents:
    - path traversal
    - destructive operations
    - shell injection
    - malformed arguments
    """

    # Commands that require path validation
    PATH_COMMANDS = {
        "create_file": ["path"],
        "create_folder": ["path"],
        "write_file": ["path"],
        "append_file": ["path"],
        "copy_file": ["src", "dst"],
        "move_file": ["src", "dst"],
        "download": ["path"],
    }

    # Commands that require shell safety
    SHELL_COMMANDS = ["run_shell"]

    # Commands that are NEVER allowed (destructive)
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
        "chmod_000",
        "del",
    ]

    # -----------------
    # Check Plan
    # -----------------
    def check_plan(self, plan_text: str):
        """
        Validates the plan for security issues.
        Raises ValueError on any violation.
        """
        try:
            plan = json.loads(plan_text)
        except Exception as e:
            raise ValueError(f"Invalid JSON: {e}")

        steps = plan.get("steps", [])
        if not isinstance(steps, list):
            raise ValueError("Plan 'steps' must be a list.")

        for step in steps:
            cmd = step.get("command")
            args = step.get("args", {})

            # Block destructive commands
            if cmd in self.BANNED_COMMANDS:
                raise ValueError(f"Destructive command not allowed: {cmd}")

            # Path Safety
            if cmd in self.PATH_COMMANDS:
                for key in self.PATH_COMMANDS[cmd]:
                    if key in args:
                        self._validate_path(args[key])

            # Shell Safety
            if cmd in self.SHELL_COMMANDS:
                self._validate_shell(args.get("cmd", ""))

        return True

    # -------------------------------------
    # Validate Path
    # -------------------------------------
    def _validate_path(self, path: str):
        """
        Allows ANY path except traversal attempts.
        No SAFE_ROOT. No workspace restriction.
        """
        normalized = os.path.normpath(path)

        # Prevent "../" traversal
        if ".." in normalized.split(os.sep):
            raise ValueError(f"Path traversal detected: {path}")

    # -------------------------------------
    # Shell Validation
    # -------------------------------------
    def _validate_shell(self, cmd: str):
        """
        Prevents shell injection.
        Allows safe commands like ping, curl, python, pip, etc.
        """
        forbidden = [";", "&&", "||", "|", "`", "$(", "<", ">"]

        for token in forbidden:
            if token in cmd:
                raise ValueError(f"Shell injection detected in command: {cmd}")

