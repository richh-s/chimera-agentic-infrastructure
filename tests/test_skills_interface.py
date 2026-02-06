import pytest


def test_skill_interface_contract():
    """
    Defines the REQUIRED interface for all Chimera skills.

    This test MUST FAIL until skills are implemented
    with a standardized invoke(inputs: dict) -> dict interface.
    """

    # Example skill paths (expected to exist later)
    skill_imports = [
        "skills.analyze.skill_content_analyzer.skill",
        "skills.govern.skill_safety_validator.skill",
        "skills.compose.skill_persona_publisher.skill",
    ]

    for module_path in skill_imports:
        module = __import__(module_path, fromlist=["invoke"])

        # Skill MUST expose invoke()
        assert hasattr(module, "invoke"), f"{module_path} must define invoke()"

        invoke_fn = getattr(module, "invoke")

        # invoke must be callable
        assert callable(invoke_fn), f"{module_path}.invoke must be callable"

        # invoke must accept exactly one argument (inputs dict)
        result = invoke_fn({})  # SHOULD fail until implemented

        # invoke must return a dict
        assert isinstance(result, dict), "Skill invoke() must return a dict"

        # Required output envelope
        required_keys = {
            "success",
            "confidence",
            "output",
        }

        assert required_keys.issubset(result.keys()), (
            f"Skill output missing required keys: {required_keys}"
        )

        assert isinstance(result["success"], bool)
        assert isinstance(result["confidence"], (int, float))
        assert 0.0 <= result["confidence"] <= 1.0
        assert isinstance(result["output"], dict)
