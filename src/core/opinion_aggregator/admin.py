from django.contrib import admin
from opinion_aggregator.models import User
from opinion_aggregator.models import survey

admin.site.register(User)
admin.site.register(survey.OptionModel)
admin.site.register(survey.QuestionModel)
admin.site.register(survey.PartModel)
admin.site.register(survey.SectionModel)
admin.site.register(survey.SurveyModel)
admin.site.register(survey.SurveyResponsesModel)
admin.site.register(survey.QuestionOptions)
# Register your models here.
