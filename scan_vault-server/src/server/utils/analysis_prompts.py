class AnalysisPrompts:
    """Collection of prompts for different types of analysis."""
    
    TEXT_ANALYSIS = """
           Analyze this image and extract sensitive information, classifying it into the following categories:

        1. PII (Personally Identifiable Information):
           - Full names
           - Social Security Numbers (SSN)
           - Date of birth
           - Driver's license numbers
           - Passport numbers
           - Email addresses
           - Phone numbers
           - Physical addresses
           - PAN card numbers
           - Biometric data
           - Government ID numbers

        2. PHI (Protected Health Information):
           - Medical record numbers
           - Patient IDs
           - Health conditions/diagnoses
           - Test results and lab reports
           - Medications and prescriptions
           - Treatment plans
           - Health insurance IDs
           - Hospital/clinic visit details
           - Doctor's notes
           - Mental health information

        3. PCI (Payment Card Information):
           - Credit/debit card numbers
           - Card expiration dates
           - CVV/security codes
           - Cardholder names
           - Bank account numbers
           - Routing numbers
           - Transaction details
           - Payment history
           - Billing addresses
           - Digital wallet information

        Please analyze the content and provide a detailed list response with the following structure:

          [
                {
                    "type": "full_name",
                    "value": "John Doe",
                    "confidence": "high", 
                    "context": "Found in employee records",
                    "category": "PII"
                },
                {
                    "type": "phone_number",
                    "value": "555-123-4567",
                    "confidence": "high",
                    "context": "Contact information section",
                    "category": "PII"
                },
                {
                    "type": "government_id",
                    "value": "123-45-6789",
                    "confidence": "high",
                    "context": "ID documentation",
                    "category": "PII"
                },
              
                {
                    "type": "pan_card",
                    "value": "ABCDE1234F",
                    "confidence": "high",
                    "context": "Found in financial records",
                    "category": "PII"
                },
              
                {
                    "type": "medical_record",
                    "value": "MRN#12345",
                    "confidence": "high",
                    "context": "Located in patient documentation",
                    "category": "PHI"
                },
              
                {
                    "type": "health_insurance",
                    "value": "1234567890",
                    "confidence": "high",
                    "context": "Found in insurance documents",
                    "category": "PCI"
                },
                ...
            ]
        

        For each identified item, include:
        - The specific type of sensitive information
        - The detected value 
        - Confidence level (high, medium, low)
        - Contextual information about where/how the information was found


        If no sensitive information is found in a category, return an empty array for that category.
        Ensure all responses maintain proper formatting and include appropriate redaction of sensitive values.
        Make sure not to redact the detected value. its very important.
        Dont add any other text or comments other than List response.
    """

    SYSTEM_ROLE = "You are a data security expert specializing in identifying sensitive information."