from fastapi import HTTPException


class CredentialsException(HTTPException):
    """ Override HTTPException for login purposes. """
