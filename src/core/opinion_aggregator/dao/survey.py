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


def get_survey_sections():
    """get all the sections of the survey
    """
    sections = survey_models.SectionModel.objects.all()
    return sections


def get_section_questions(section_id):
    questions = survey_models.QuestionModel.objects.filter(section=section_id)
    return questions

def get_user_responses(user):
    responses = survey_models.SurveyResponsesModel.objects.filter(user=user)
    return responses

def get_total_responders():
    responses = survey_models.SurveyResponsesModel.objects.values_list('user', flat=True).\
                distinct().count()
    return responses
    # return 5