# ./KernelOperator/engine/llm_engine.py
# LLM Engine for KernelOperator (Local GGUF Loader)
# Created By: David Kistner (Unconditional Love) at GlyphicMind Solutions LLC.



# system imports
import os, sys, yaml
from pathlib import Path
from typing import Dict, Optional
from contextlib import contextmanager, redirect_stdout, redirect_stderr
from llama_cpp import Llama



# ------------------------------
# SUPPRESS LLAMA OUTPUT
# ------------------------------
@contextmanager
def suppress_llama_io():
    """
    Prevent llama.cpp from spamming stdout/stderr.
    """
    with open(os.devnull, "w") as devnull:
        old_stdout, old_stderr = sys.stdout, sys.stderr
        try:
            with redirect_stdout(devnull), redirect_stderr(devnull):
                yield
        finally:
            sys.stdout, sys.stderr = old_stdout, old_stderr



# ======================================
# LLM ENGINE CLASS
# ======================================
class LLMEngine:
    """
    LLMEngine
    - Loads local .gguf models via llama_cpp
    - Uses manifest.yaml → system-level models.yaml
    - Supports multiple models, selected by key
    - Model-agnostic: prompt templates handled by PromptBuilder
    """

    # ----------------
    # Initialize
    # ----------------
    def __init__(self, manifest_path: Path, log=None):
        """
            Initializes the LLM Engine
        """
        #pathing
        self.manifest_path = Path(manifest_path)

        #log
        self.log = log or (lambda msg: print(msg))

        #model configuration
        self.models_config: Dict[str, dict] = {}
        self.models: Dict[str, Llama] = {}
        self.default_key: Optional[str] = None
        self._load_manifest()

    # --------------------------------------
    # Load Manifest
    # --------------------------------------
    def _load_manifest(self):
        """
        Loads manifest.yaml → loads external system-level models.yaml
        """

        if not self.manifest_path.exists():
            raise FileNotFoundError(f"manifest.yaml not found at {self.manifest_path}")

        # Load local manifest
        with open(self.manifest_path, "r", encoding="utf-8") as f:
            local_manifest = yaml.safe_load(f) or {}

        external_path = (
            local_manifest.get("model_definitions")
            or local_manifest.get("models")
        )

        if not external_path:
            raise ValueError("manifest.yaml missing both 'model_definitions' and 'models' keys.")

        external_path = Path(external_path).expanduser().resolve()

        if not external_path.exists():
            raise FileNotFoundError(f"System model registry not found: {external_path}")

        self.log(f"🧠 LLMEngine: loading system model registry: {external_path}")

        # Load system-level models.yaml
        with open(external_path, "r", encoding="utf-8") as f:
            external_manifest = yaml.safe_load(f) or {}

        root = external_path.parent
        models = (
            external_manifest.get("models")
            or external_manifest.get("model_definitions")
            or {}
        )

        resolved = {}
        for key, cfg in models.items():
            cfg = dict(cfg)

            # Resolve model path
            if "path" in cfg:
                cfg["path"] = str((root / cfg["path"]).resolve())

            # Resolve mmproj path (if multimodal)
            if "mmproj" in cfg:
                cfg["mmproj"] = str((root / cfg["mmproj"]).resolve())

            resolved[key] = cfg

        self.models_config = resolved

        if not self.models_config:
            raise ValueError("No models defined in system model registry.")

        # First model becomes default
        self.default_key = next(iter(self.models_config.keys()))

    # --------------------------------------
    # Get Available Models
    # --------------------------------------
    def get_available_models(self):
        """
        Returns a list of available models with metadata.
        """
        out = []
        for key, cfg in self.models_config.items():
            out.append(
                {
                    "key": key,
                    "path": cfg.get("path"),
                    "n_ctx": cfg.get("n_ctx", 32768),
                    "template": cfg.get("template", "llama"),
                }
            )
        return out

    # --------------------------
    # Get Context Window
    # --------------------------
    def get_context_window(self, model_key: str) -> int:
        """
            retreives token context window
        """
        cfg = self.models_config.get(model_key, {})
        return int(cfg.get("n_ctx", 32768))

    # ---------------------------------------
    # Load Model
    # ---------------------------------------
    def load_model(self, key: Optional[str] = None) -> Llama:
        """
        Lazy-load a model by key.
        """
        if key is None:
            key = self.default_key

        if key in self.models:
            return self.models[key]

        cfg = self.models_config.get(key)
        if not cfg:
            raise KeyError(f"Model key '{key}' not found in registry.")

        model_path = Path(cfg.get("path"))
        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found: {model_path}")

        n_ctx = int(cfg.get("n_ctx", 32768))

        self.log(f"🧠 LLMEngine: loading model '{key}'")

        with suppress_llama_io():
            llm = Llama(
                model_path=str(model_path),
                n_ctx=n_ctx,
                n_threads=os.cpu_count() or 4,
            )

        self.models[key] = llm
        self.log(f"🧠 LLMEngine: model loaded: {key}")

        return llm

    # ---------------------------------------
    # Generate
    # ---------------------------------------
    def generate(self, prompt: str, model_key: Optional[str] = None, max_tokens: int = 16344) -> str:
        """
        Generate text using the selected model.
        """
        llm = self.load_model(model_key)

        active_key = model_key or self.default_key
        self.log(f"🧠 LLMEngine: generating with model={active_key}")

        out = llm(
            prompt,
            max_tokens=max_tokens,
            stop=["FIN~"],
            echo=False,
        )

        return out["choices"][0]["text"]

