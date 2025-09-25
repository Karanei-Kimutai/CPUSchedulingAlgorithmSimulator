"""
Utility helpers used by the CPU scheduling simulator.

Provides:
 - safeInput: robust user input with validation and type conversion
 - ensureDirectoryExists: create output directories if missing
"""

import os
from typing import Iterable, Optional, Type, Any


def safeInput(promptMessage: str, castType: Type = str, validOptions: Optional[Iterable[Any]] = None) -> Any:
    """
    Prompt the user repeatedly until a valid value is provided.

    Args:
        promptMessage: Text to present to the user.
        castType: Type to cast the raw input into (e.g. int, float, str).
        validOptions: Optional iterable of allowed values AFTER casting. For string options,
                      comparison is case-insensitive and the canonical option (from validOptions)
                      is returned.

    Returns:
        The user input converted to castType, and validated against validOptions if provided.
    """
    while True:
        rawInput = input(promptMessage).strip()
        try:
            castedValue = castType(rawInput)
        except ValueError:
            print(f"Invalid input: please enter a valid {castType.__name__}.")
            continue

        if validOptions is not None:
            # If options are strings, compare in lowercase for convenience
            if isinstance(castedValue, str):
                loweredValue = castedValue.lower()
                normalizedOptions = [opt.lower() if isinstance(opt, str) else opt for opt in validOptions]
                if loweredValue not in normalizedOptions:
                    print(f"Invalid option. Allowed options: {validOptions}")
                    continue
                # return canonical option from validOptions (preserve provided casing)
                for opt in validOptions:
                    if isinstance(opt, str) and opt.lower() == loweredValue:
                        return opt
                return castedValue
            else:
                if castedValue not in validOptions:
                    print(f"Invalid option. Allowed options: {validOptions}")
                    continue

        return castedValue


def ensureDirectoryExists(directoryPath: str) -> str:
    """
    Create the directory inside the project root if it does not exist. 
    Always resolves relative to the project root, not the current working directory.

    Args:
        directoryPath: path to directory (relative or absolute).

    Returns:
        The absolute path of the ensured directory.
    """
    #Resolve base directory(two levels up from this file)
    baseDirectory=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    absolutePath=os.path.join(baseDirectory,directoryPath)
    # Create directory if it doesn't exist
    os.makedirs(absolutePath, exist_ok=True)
    return absolutePath

