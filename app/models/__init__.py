# File: app/models/__init__.py
"""
MongoDB document models using Beanie ODM.
"""
from app.models.course import Course
from app.models.material import Material
from app.models.lecture import Lecture
from app.models.content import GeneratedContent

__all__ = ["Course", "Material", "Lecture", "GeneratedContent"]
