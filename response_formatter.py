# response_formatter.py
import json

def format_response(decision, amount, justification):
    """
    Formats the final decision into a human-readable JSON string.

    Args:
        decision (str): The final decision ("approved" or "rejected").
        amount (str): The amount to be paid (or "0" if rejected).
        justification (list): A list of strings explaining the decision.

    Returns:
        str: A JSON formatted string of the decision.
    """
    response = {
        "Decision": decision,
        "Amount": amount,
        "Justification": justification
    }
    return json.dumps(response, indent=4)

