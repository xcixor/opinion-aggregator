"""fetch data from survey models
"""
from opinion_aggregator.models import survey as survey_models

def get_surveys():
    """fetches surveys
    """
    return survey_models.SurveyModel.objects.all()