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

        Please analyze the content and provide a detailed JSON response with the following structure:

        {
            "pii": [
                {
                    "type": "ssn",
                    "value": "XXX-XX-1234",
                    "confidence": "high",
                    "context": "Found in employee records section"
                }
            ],
            "phi": [
                {
                    "type": "medical_record",
                    "value": "MRN#12345",
                    "confidence": "high",
                    "context": "Located in patient documentation"
                },
                {
                    "type": "diagnosis",
                    "value": "Type 2 Diabetes",
                    "confidence": "medium",
                    "context": "Mentioned in medical history"
                }
            ],
            "pci": [
                {
                    "type": "credit_card",
                    "value": "XXXX-XXXX-XXXX-5678",
                    "confidence": "high",
                    "context": "Found in payment section"
                }
            ]
        }

        For each identified item, include:
        - The specific type of sensitive information
        - The detected value
        - Confidence level (high, medium, low)
        - Contextual information about where/how the information was found

        If no sensitive information is found in a category, return an empty array for that category.
        Ensure all responses maintain proper formatting and include appropriate redaction of sensitive values.
    """

    SYSTEM_ROLE = "You are a data security expert specializing in identifying sensitive information."