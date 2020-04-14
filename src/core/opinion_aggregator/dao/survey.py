"""fetch data from survey models
"""
from opinion_aggregator.models import survey as survey_models
from django.core.paginator import Paginator

def get_surveys():
    """fetches surveys
    """
    return survey_models.SurveyModel.objects.all()


def get_survey_parts():
    """fetches all survey parts
    """
    pages = survey_models.PartModel.objects.all()
    return pages