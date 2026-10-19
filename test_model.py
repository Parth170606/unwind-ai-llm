
import json
from pathlib import Path

import torch
import transformers
import peft
from safetensors import safe_open

ADAPTER_DIR = Path("model/final_adapter")

print("=== UNWIND AI V2: PRE-FLIGHT CHECK ===")
print("PyTorch:", torch.__version__)
print("Transformers:", transformers.__version__)
print("PEFT:", peft.__version__)

config_path = ADAPTER_DIR / "adapter_config.json"
weights_path = ADAPTER_DIR / "adapter_model.safetensors"
tokenizer_path = ADAPTER_DIR / "tokenizer.json"

for path in (config_path, weights_path, tokenizer_path):
    if not path.is_file():
        raise FileNotFoundError(f"Required file is missing: {path}")
    print(f"Found: {path}")

with config_path.open("r", encoding="utf-8") as f:
    config = json.load(f)

print("\nBase model:", config.get("base_model_name_or_path"))
print("LoRA rank:", config.get("r"))
print("LoRA alpha:", config.get("lora_alpha"))
print("Task type:", config.get("task_type"))

print("\nChecking trained adapter weights...")
with safe_open(str(weights_path), framework="pt", device="cpu") as f:
    keys = list(f.keys())
    print("Tensor count:", len(keys))
    print("Sample tensor names:", keys[:5])

print("\nPre-flight check passed.")
print("No base model was downloaded or loaded.")
print("Next step: choose a memory-safe inference method.")
