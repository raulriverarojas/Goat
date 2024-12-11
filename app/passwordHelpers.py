import re
class PasswordHelpers:
    # Define the regex patterns
    patterns = {
        'lowercase': r'[a-z]',
        'uppercase': r'[A-Z]',
        'number': r'\d',
        'special_char': r'[ -\/:-`{-\xFF]'  # ASCII ranges: 32-47, 58-96, 123-255
    }
    
    # Length requirement (8+ characters)
    valid_length = r'.{8,}'
    
    # Ensure only valid characters are used
    
    @classmethod
    def is_valid_password(cls, password: str) -> bool:
        """
        Validate if a password meets all requirements.
        """
        # Check length
        if not re.search(cls.valid_length, password):
            return False
            
        # Check all required patterns
        return all(re.search(pattern, password) for pattern in cls.patterns.values())
    
    @classmethod
    def check_requirements(cls, password: str) -> dict:
        """
        Return detailed breakdown of which requirements the password meets.
        """
        return {
            'length': bool(re.search(cls.valid_length, password)),
            'valid_chars': bool(re.match(cls.valid_chars, password)),
            **{name: bool(re.search(pattern, password)) 
               for name, pattern in cls.patterns.items()}
        }