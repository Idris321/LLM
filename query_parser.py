# query_parser.py
def parse_query(query):
    """
    Parses a natural language query into a structured dictionary.

    Args:
        query (str): A comma-separated string containing user details.
                     Expected format: "age gender, procedure, location, policy_duration"
                     Example: "65 male, Deep Brain stimulation, Pune, 1 year"

    Returns:
        dict: A dictionary with keys 'age', 'gender', 'procedure', 'location', 'policy_duration'.

    Raises:
        ValueError: If the query format is incorrect or incomplete.
    """
    details = {}
    parts = query.split(',')
    
    if len(parts) < 4:
        raise ValueError("Query must contain at least four parts separated by commas.")
    
    # Correctly parse each part of the query and handle potential errors
    try:
        age_gender_part = parts[0].strip().split()
        if len(age_gender_part) < 2:
            raise ValueError("Age and gender are not correctly formatted.")
        details['age'] = int(age_gender_part[0])  # Convert age to int for potential numerical checks
        details['gender'] = age_gender_part[1]
        details['procedure'] = parts[1].strip()
        details['location'] = parts[2].strip()
        details['policy_duration'] = parts[3].strip()
    except (IndexError, ValueError) as e:
        raise ValueError(f"Invalid query format. Please check your input. Details: {e}") from e

    return details
