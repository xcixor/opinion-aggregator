from django import template
from django.db.models import Count, Q
from opinion_aggregator.models import survey

register = template.Library()


@register.filter
def get_count(response):
    responses = survey.SurveyResponsesModel.objects.filter(response=response).count()
    return responses

@register.filter
def get_leadership_yes_responses(question):
    responses = survey.SurveyResponsesModel.objects.filter(question=question, response="Yes").\
            values_list('response', flat=True).\
                distinct()
    return len(responses)

@register.filter
def get_leadership_no_responses(question):
    responses = survey.SurveyResponsesModel.objects.filter(question=question, response="No").\
            values_list('response', flat=True).\
                distinct()
    return len(responses)


@register.filter
def get_salary_count(question):
    responses = survey.SurveyResponsesModel.objects.filter(question=question, response="have a job with salary").\
            values_list('response', flat=True).\
                distinct()
    return len(responses)

@register.filter
def get_business_responses(question):
    responses = survey.SurveyResponsesModel.objects.\
        filter(question=question, response="being a entrepreneur and have a you own businesses").\
            values_list('response', flat=True).\
                distinct()
    return len(responses)

@register.filter
def make_list(value):
    loop_list = []
    for i in range(0, value):
        loop_list.append(value)
    return loop_list


@register.filter
def get_popularity(response):
    responses = survey.SurveyResponsesModel.objects.filter(response=response)
    return len(responses)

@register.filter
def get_unique_responses(responses, value):
    if responses:
        response_list = survey.SurveyResponsesModel.objects.filter(question=responses[0].question).\
            values_list('response', flat=True).\
                distinct().order_by('response')[:int(value)]
        return response_list
    return None