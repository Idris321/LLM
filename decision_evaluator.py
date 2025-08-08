# decision_evaluator.py
def evaluate_decision(retrieved_info, parsed_query):
    """
    Evaluates the retrieved information to make a decision based on keywords
    and the original query context.

    This function now checks for both positive (approval) and negative (rejection)
    keywords in the API's response to provide a more accurate decision.
    """
    print("Evaluating decision based on retrieved information...")

    # Set a default response in case the API provides no useful information
    decision = "rejected"
    amount = "0"
    justification = ["Insufficient information or low confidence score to approve the claim."]

    # Check for a high confidence score from the information retriever
    # We will assume a high score for any successful API call
    if not retrieved_info or retrieved_info[0]['score'] < 0.5:
        return decision, amount, justification

    # Extract the text from the most confident answer
    justification_text = retrieved_info[0]['answer']
    query_procedure = parsed_query.get('procedure', '').lower()

    # Define keywords for approval and rejection
    approval_keywords = [
        "covered",
        "listed under",
        "reimburse",
        "treatment methods"
    ]
    rejection_keywords = [
        "pre-existing",
        "excluded",
        "waiting period",
        "not covered",
        "not listed",
        "unless",
        "limited to"
    ]

    # New, improved logic: Check for approval keywords in the context of the query.
    # The presence of an approval keyword overrides any generic rejection keywords.
    if any(keyword in justification_text.lower() for keyword in approval_keywords):
        if query_procedure in justification_text.lower():
            decision = "approved"
            amount = "500,000 INR (Mock Amount)"
            justification = [f"Based on the documents, the procedure '{query_procedure}' is covered."]
            return decision, amount, justification
    
    # If no specific approval is found, then we check for rejection keywords
    if any(keyword in justification_text.lower() for keyword in rejection_keywords):
        decision = "rejected"
        amount = "0"
        justification = [justification_text]
        return decision, amount, justification
    
    # Fallback to the original decision if no clear keywords are found
    return decision, amount, justification

