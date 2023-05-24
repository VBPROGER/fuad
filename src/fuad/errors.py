#!/usr/bin/env python3
class BaseFUADError(BaseException):
    'Main class to capture all errors'
class MagicError(BaseFUADError):
    'Invalid magic received'
class DataReadingError(BaseFUADError):
    'Couldn\'t read the data'
class SecurityViolation(BaseFUADError):
    'Violation of security'

class HashMismatch(SecurityViolation):
    'Hashes didn\'t match'
class InterceptedPath(SecurityViolation):
    'Path is invalid and may be intercepted'
class NameMetaMismatch(SecurityViolation):
    'Name in dictionary and in metadata didn\'t match'

class UnexpectedHandleError(BaseFUADError):
    'The condition was not implemented or will not be, or condition is not handled'