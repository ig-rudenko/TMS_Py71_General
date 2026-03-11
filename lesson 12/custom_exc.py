class ValidationError(Exception): ...


class EmailValidationError(ValidationError): ...


def raise_email_errors(email: str):
    if "@" not in email or "." not in email:
        raise EmailValidationError("Invalid email address")



raise_email_errors("user")