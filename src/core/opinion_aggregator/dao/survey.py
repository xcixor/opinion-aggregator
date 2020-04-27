"""fetch data from survey models
"""
from django.core.paginator import Paginator
from django.db.models import Count
from opinion_aggregator.models import survey as survey_models


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

def get_question_options(question):
    """fetch a question responses

    Arguments:
        question {string} -- question to fetch responses for
    """
    question_object = survey_models.QuestionModel.objects.filter(description=question).first()
    responses = survey_models.QuestionOptions.objects.filter(question=question_object)
    return responses


def get_question_responses(question):
    question_object = survey_models.QuestionModel.objects.filter(description=question).first()
    return question_object.responses.all()



def get_popularity(response):
    responses = survey_models.SurveyResponsesModel.objects.filter(response=response)
    return len(responses)


def get_unique_responses(responses, value):
    """get unique responses

    Arguments:
        responses {[queryset]} -- [queryset to filter from responses model]
        value {[type]} -- [restrict to this number of responses]

    Returns:
        [type] -- [description]
    """
    if responses:
        response_list = survey_models.SurveyResponsesModel.objects.filter(question=responses[0].question).\
            values_list('response', flat=True).\
                distinct().annotate(response_count=Count('response')).order_by('-response_count')[:int(value)]
        return response_list
    return None


def get_sub_categories_count(options, count):
    """return count of an options subcategories
    """
    count = 0
    for option in options:
        sub_category_response_count = survey_models.SurveyResponsesModel.objects.filter(response=option).count()
        count += sub_category_response_count
    return count