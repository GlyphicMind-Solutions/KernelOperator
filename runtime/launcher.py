# ./runtime/launcher.py
# Plan Launcher for Kernel Operator
# Created By: David Kistner (Unconditional Love) at GlyphicMind Solutions



# system imports
import os, json, subprocess, shutil, requests



# =====================================
# PLAN LAUNCHER CLASS
# =====================================
class PlanLauncher:
    """
    Executes validated plans.
    Streams output via callback.
    Creation-only. No destructive commands.
    """

    # --------------
    # Initialize
    # --------------
    def __init__(self, output_callback=None):
        self.out = output_callback or (lambda msg: None)

    # --------------
    # Run
    # --------------
    def execute(self, plan_text: str):
        plan = json.loads(plan_text)

        for step in plan["steps"]:
            cmd = step["command"]
            args = step.get("args", {})

            self.out(f"→ {cmd} {args}\n")

            handler = getattr(self, f"_cmd_{cmd}", None)
            if not handler:
                raise ValueError(f"No handler for command: {cmd}")

            handler(args)


# =====================================
# Command Handlers Section
# =====================================
    # -------------------------
    # Create Folder Command
    # -------------------------
    def _cmd_create_folder(self, args):
        path = args["path"]
        os.makedirs(path, exist_ok=True)
        self.out(f"Created folder: {path}\n")

    # -------------------------
    # Create File Command
    # -------------------------
    def _cmd_create_file(self, args):
        path = args["path"]
        open(path, "w").close()
        self.out(f"Created file: {path}\n")

    # -------------------------
    # Write File Command
    # -------------------------
    def _cmd_write_file(self, args):
        path = args["path"]
        content = args["content"]
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        self.out(f"Wrote file: {path}\n")

    # -------------------------
    # Append File Command
    # -------------------------
    def _cmd_append_file(self, args):
        path = args["path"]
        content = args["content"]
        with open(path, "a", encoding="utf-8") as f:
            f.write(content)
        self.out(f"Appended file: {path}\n")

    # -------------------------
    # Copy File Command
    # -------------------------
    def _cmd_copy_file(self, args):
        src = args["src"]
        dst = args["dst"]
        shutil.copy(src, dst)
        self.out(f"Copied {src} → {dst}\n")

    # -------------------------
    # Move File Command
    # -------------------------
    def _cmd_move_file(self, args):
        src = args["src"]
        dst = args["dst"]
        # Safe move: do not overwrite existing files
        if os.path.exists(dst):
            raise ValueError(f"Refusing to overwrite existing file: {dst}")
        shutil.move(src, dst)
        self.out(f"Moved {src} → {dst}\n")

    # -------------------------
    # Download Command
    # -------------------------
    def _cmd_download(self, args):
        url = args["url"]
        path = args["path"]
        data = requests.get(url).content
        with open(path, "wb") as f:
            f.write(data)
        self.out(f"Downloaded {url} → {path}\n")

    # -------------------------
    # HTTP Request Command
    # -------------------------
    def _cmd_http_request(self, args):
        method = args.get("method", "GET").upper()
        url = args["url"]
        data = args.get("data")
        resp = requests.request(method, url, json=data)
        self.out(f"HTTP {method} {url} → {resp.status_code}\n")

    # -------------------------
    # Run Shell Commands
    # -------------------------
    def _cmd_run_shell(self, args):
        cmd = args["cmd"]
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True
        )
        if result.stdout:
            self.out(result.stdout)
        if result.stderr:
            self.out(result.stderr)

    # -------------------------
    # Pip Install Command
    # -------------------------
    def _cmd_pip_install(self, args):
        package = args["package"]
        result = subprocess.run(
            ["pip", "install", package],
            capture_output=True,
            text=True
        )
        self.out(result.stdout)
        if result.stderr:
            self.out(result.stderr)

    # ------------------------------------
    # Create Virtual Enviroment Command
    # ------------------------------------
    def _cmd_create_virtualenv(self, args):
        path = args["path"]
        result = subprocess.run(
            ["python3", "-m", "venv", path],
            capture_output=True,
            text=True
        )
        self.out(f"Created virtualenv at: {path}\n")
        if result.stderr:
            self.out(result.stderr)

    # --------------------------------------
    # Install Requirements Command
    # --------------------------------------
    def _cmd_install_requirements(self, args):
        req_file = args["path"]
        result = subprocess.run(
            ["pip", "install", "-r", req_file],
            capture_output=True,
            text=True
        )
        self.out(result.stdout)
        if result.stderr:
            self.out(result.stderr)

    # ----------------------------
    # Scaffold Project Command
    # ----------------------------
    def _cmd_scaffold_project(self, args):
        """
        Generic scaffolding command.
        LLM can generate folder/file structure in args["structure"].
        """
        structure = args["structure"]

        for item in structure:
            if item["type"] == "folder":
                os.makedirs(item["path"], exist_ok=True)
                self.out(f"Created folder: {item['path']}\n")

            elif item["type"] == "file":
                with open(item["path"], "w", encoding="utf-8") as f:
                    f.write(item.get("content", ""))
                self.out(f"Created file: {item['path']}\n")

