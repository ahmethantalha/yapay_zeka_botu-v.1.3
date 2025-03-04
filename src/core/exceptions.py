class AppException(Exception):
    """Base exception for application"""
    pass

class FileProcessingError(AppException):
    """Error during file processing"""
    pass

class AIServiceError(AppException):
    """Error from AI service"""
    pass

class DatabaseError(AppException):
    """Error from database operations"""
    pass

class ConfigurationError(AppException):
    """Error in application configuration"""
    pass

class SecurityError(AppException):
    """Error in security operations"""
    pass