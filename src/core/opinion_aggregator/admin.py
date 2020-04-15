from django.contrib import admin
from opinion_aggregator.models import User
from opinion_aggregator.models import survey

class ResponsesAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'response')

admin.site.register(User)
admin.site.register(survey.OptionModel)
admin.site.register(survey.QuestionModel)
admin.site.register(survey.PartModel)
admin.site.register(survey.SectionModel)
admin.site.register(survey.SurveyModel)
admin.site.register(survey.SurveyResponsesModel, ResponsesAdmin)
admin.site.register(survey.QuestionOptions)
# Register your models here.
