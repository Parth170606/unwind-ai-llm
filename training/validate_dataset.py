import json
from pathlib import Path
from collections import Counter

DATASET_PATH = Path("data/raw/train.jsonl")

REQUIRED_ROLES = {"system", "user", "assistant"}
ALLOWED_ROLES = {"system", "user", "assistant"}


def validate_dataset():
    if not DATASET_PATH.exists():
        print(f"ERROR: Dataset not found: {DATASET_PATH}")
        return

    examples = []
    errors = []

    with DATASET_PATH.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            try:
                example = json.loads(line)
            except json.JSONDecodeError as error:
                errors.append(
                    f"Line {line_number}: Invalid JSON - {error.msg}"
                )
                continue

            if not isinstance(example, dict):
                errors.append(
                    f"Line {line_number}: Example must be a JSON object."
                )
                continue

            messages = example.get("messages")

            if not isinstance(messages, list):
                errors.append(
                    f"Line {line_number}: 'messages' must be a list."
                )
                continue

            roles = []
            valid_messages = True

            for message in messages:
                if not isinstance(message, dict):
                    errors.append(
                        f"Line {line_number}: Each message must be an object."
                    )
                    valid_messages = False
                    continue

                role = message.get("role")
                content = message.get("content")

                if role not in ALLOWED_ROLES:
                    errors.append(
                        f"Line {line_number}: Invalid role: {role!r}"
                    )
                    valid_messages = False
                else:
                    roles.append(role)

                if not isinstance(content, str) or not content.strip():
                    errors.append(
                        f"Line {line_number}: Message content is empty "
                        "or not text."
                    )
                    valid_messages = False

            if not REQUIRED_ROLES.issubset(set(roles)):
                errors.append(
                    f"Line {line_number}: Must include system, user, "
                    "and assistant messages."
                )
                valid_messages = False

            if valid_messages:
                examples.append(example)

    print("\nUNWIND DATASET VALIDATION")
    print("-" * 30)
    print(f"Valid examples: {len(examples)}")
    print(f"Errors found: {len(errors)}")

    role_counts = Counter(
        message["role"]
        for example in examples
        for message in example["messages"]
    )

    print("\nMessage counts:")
    for role, count in sorted(role_counts.items()):
        print(f"  {role}: {count}")

    if errors:
        print("\nProblems to fix:")
        for error in errors:
            print(f"  - {error}")
        print("\nRESULT: FAILED")
    else:
        print("\nRESULT: PASSED")
        print("The dataset structure looks good.")


if __name__ == "__main__":
    validate_dataset()
