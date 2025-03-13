class BluetermError(Exception):
    """Base exception for all bluetermgen errors."""

    pass


class MessageError(BluetermError):
    """Base exception for Message-related errors."""

    pass


class ValidationError(MessageError):
    """Raised when input validation fails."""

    pass


class AlignmentError(MessageError):
    """Raised when alignment validation fails."""

    pass


class PaddingError(MessageError):
    """Raised when padding validation fails."""

    pass


class StyleError(MessageError):
    """Raised when style validation fails."""

    pass
