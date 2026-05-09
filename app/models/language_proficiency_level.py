from enum import Enum


class ProficiencyLevel(str, Enum):
    elementary = "Elementary proficiency"
    limited_working = "Limited working proficiency"
    professional_working = "Professional working proficiency"
    full_professional = "Full professional proficiency"
    native_bilingual = "Native or bilingual proficiency"
