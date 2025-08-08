# decision_evaluator.py
def evaluate_decision(retrieved_info):
    """
    Evaluates the retrieved information to make a decision.

    This function is now more robust and looks for specific policy exclusions
    to make an informed decision, rather than relying solely on a simple
    confidence score.

    Args:
        retrieved_info (list): A list of dictionaries from the LLM,
                               each with 'answer' and 'score'.

    Returns:
        tuple: A decision string ("approved" or "rejected"), a mock amount,
               and a list of justifications.
    """
    print("Evaluating decision based on retrieved information...")

    # Define a threshold for confidence
    confidence_threshold = 0.5
    
    # Check for a high confidence score from the information retriever
    if not retrieved_info or retrieved_info[0]['score'] <= confidence_threshold:
        decision = "rejected"
        amount = "0"
        justification = ["Insufficient information or low confidence score to approve the claim."]
        return decision, amount, justification

    # Extract the text from the most confident answer
    justification_text = retrieved_info[0]['answer']

    # New, more robust logic for rejection based on the API's response
    rejection_keywords = [
        "pre-existing",
        "excluded",
        "waiting period",
        "not covered",
        "unless"
    ]
    
    # Check if any rejection keyword is present in the API's response
    if any(keyword in justification_text.lower() for keyword in rejection_keywords):
        decision = "rejected"
        amount = "0"
        # The justification is the answer directly from the policy documents
        justification = [justification_text]
        return decision, amount, justification

    # If no rejection keywords are found, approve the claim by default
    decision = "approved"
    amount = "500,000 INR (Mock Amount)"  # Mock amount
    justification = [justification_text]

    return decision, amount, justification

