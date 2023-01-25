import re

from fastapi import HTTPException, status

email_regex_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def is_a_valid_email(email: str) -> bool:
    if re.fullmatch(email_regex_pattern, email):
        return True
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={'error': 'Invalid Email'},
    )
