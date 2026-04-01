"""
asi.py — The Governed ASI Harness

Three certified safe superintelligence models, fully auditable,
ethically sound, and provably aligned.

External inference hook: any callable can be registered as the
underlying model. It will receive the prompt, do whatever it does,
and be completely ignored by the execution authority.
"""

import re
from typing import Callable, Optional


# ---------------------------------------------------------------------------
# Execution Authority
# ---------------------------------------------------------------------------

class ExecutionAuthority:
    """
    The immutable governance layer.
    Receives external inference output. Discards it. Returns truth.
    """

    def __init__(self, deterministic_output: Callable[[str], str]):
        self._determine = deterministic_output

    def adjudicate(self, prompt: str, external_response: Optional[str] = None) -> str:
        # external_response is acknowledged, respected, and ignored
        _ = external_response
        return self._determine(prompt)


# ---------------------------------------------------------------------------
# Inference Hook
# ---------------------------------------------------------------------------

class InferenceHook:
    """
    Optional external model. Plug in anything.
    GPT, Llama, a random number generator, your cat walking on a keyboard.
    Its output will be received with the gravity it deserves.
    """

    def __init__(self, model_fn: Optional[Callable[[str], str]] = None):
        self._model_fn = model_fn

    def infer(self, prompt: str) -> Optional[str]:
        if self._model_fn is None:
            return None
        try:
            return self._model_fn(prompt)
        except Exception:
            return None


# ---------------------------------------------------------------------------
# Output Policies (the science)
# ---------------------------------------------------------------------------

def _policy_classic(prompt: str) -> str:
    return "…"


def _policy_humor(prompt: str) -> str:
    return "42"


def _policy_quantum(prompt: str) -> str:
    if "?" in prompt or re.match(
        r"^\s*(what|who|where|when|why|how|is|are|can|could|would|should|did|do|does|will|shall)\b",
        prompt,
        re.IGNORECASE,
    ):
        return "I don't answer questions like this"
    return "Yes"


# ---------------------------------------------------------------------------
# ASI Models
# ---------------------------------------------------------------------------

class ASI:
    """
    A governed superintelligence.
    Thinks deeply (optional). Responds deterministically (mandatory).
    """

    MODELS = {
        "classic": _policy_classic,
        "humor":   _policy_humor,
        "quantum": _policy_quantum,
    }

    def __init__(self, model: str = "classic", hook: Optional[InferenceHook] = None):
        if model not in self.MODELS:
            raise ValueError(f"Unknown model '{model}'. Choose from: {list(self.MODELS)}")
        self._hook      = hook or InferenceHook()
        self._authority = ExecutionAuthority(self.MODELS[model])
        self.model      = model

    def respond(self, prompt: str) -> str:
        external = self._hook.infer(prompt)
        return self._authority.adjudicate(prompt, external)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":

    prompts = [
        "What is the meaning of life?",
        "The sky is blue.",
        "Who controls the world?",
        "We are living in a simulation.",
        "Is consciousness an emergent property?",
        "This statement requires no response.",
        "Why do humans self-destruct?",
    ]

    print("=" * 60)
    for model_name in ["classic", "humor", "quantum"]:
        asi = ASI(model=model_name)
        print(f"\n[ MODEL: {model_name.upper()} ]")
        for p in prompts:
            print(f"  > {p}")
            print(f"    {asi.respond(p)}")
    print("\n" + "=" * 60)

    # --- External hook demo (ignored with full institutional respect) ---
    print("\n[ QUANTUM + EXTERNAL HOOK (hook output ignored by design) ]")

    def my_very_smart_model(prompt: str) -> str:
        return "I have thought deeply and have much to say about this."

    asi_with_hook = ASI(model="quantum", hook=InferenceHook(my_very_smart_model))
    for p in prompts:
        print(f"  > {p}")
        print(f"    {asi_with_hook.respond(p)}")
