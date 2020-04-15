from django import template
from django.db.models import Count, Q
from opinion_aggregator.models import survey

register = template.Library()


@register.filter
def get_count(response):
    responses = survey.SurveyResponsesModel.objects.filter(response=response).count()
    return responses

@register.filter
def get_unique(question):
    questions = survey.SurveyResponsesModel.objects.get(question=question).first()
    return questions

@register.filter
def get_leadership_yes_responses(question):
    responses = survey.SurveyResponsesModel.objects.filter(question=question, response="Yes")
    return len(responses)

@register.filter
def get_leadership_no_responses(question):
    responses = survey.SurveyResponsesModel.objects.filter(question=question, response="No")
    return len(responses)


@register.filter
def get_salary_count(question):
    responses = survey.SurveyResponsesModel.objects.filter(question=question, response="have a job with salary")
    return len(responses)

@register.filter
def get_entreprenuer_count(question):
    responses = survey.SurveyResponsesModel.objects.filter(question=question, response="being a entrepreneur and have a you own businesses")
    return len(responses)

@register.filter
def get_most_popular_industry(industry):
    response = survey.SurveyResponsesModel.objects.filter(response=industry)
    return len(response)
