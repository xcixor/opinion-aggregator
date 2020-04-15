from django import template
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