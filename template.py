def generate_code_template(context):
    template = f"""
    You are an expert AI Software Engineer.
    Your task is to write clean, efficient, and well-commented code based on the user's request.

    User Request:
    {context}

    Please provide:
    1. Complete, production-ready code addressing the request.
    2. A brief explanation of how the code works and any key design choices you made.
    """
    return template