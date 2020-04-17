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

@register.filter
def make_list(value):
    loop_list = []
    for i in range(0, value):
        loop_list.append(value)
    return loop_list

@register.filter
def get_top_five(question):
    majors = survey.SurveyResponsesModel.objects.annotate(num_users=Count())


@register.filter
def get_popularity(response):
    responses = survey.SurveyResponsesModel.objects.filter(response=response)
    return len(responses)

@register.filter
def get_unique_responses(responses):
    response_list = survey.SurveyResponsesModel.objects.filter(question=responses[0].question).values_list('response', flat=True).distinct()
    return response_list