from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from opinion_aggregator.models import User
from opinion_aggregator.models import survey

class ResponsesAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'response')


class OptionSubCategoryModelInline(NestedStackedInline):
    fk_name = 'option'
    model = survey.OptionSubCategory
    extra = 1


class QuestionOptionsModelAdmin(admin.ModelAdmin):
    inlines = [OptionSubCategoryModelInline]


class OptionModelInline(NestedStackedInline):
    model = survey.QuestionOptions
    # show_change_link = True
    fk_name = 'question'
    inlines = [OptionSubCategoryModelInline]
    extra = 1


class QuestionModelAdmin(NestedModelAdmin):
    model = survey.QuestionModel
    inlines = [OptionModelInline]


admin.site.register(User)
admin.site.register(survey.OptionModel)
admin.site.register(survey.QuestionModel, QuestionModelAdmin)
# admin.site.register(QuestionModelAdmin)
admin.site.register(survey.PartModel)
admin.site.register(survey.SectionModel)
admin.site.register(survey.SurveyModel)
admin.site.register(survey.SurveyResponsesModel, ResponsesAdmin)
# admin.site.register(survey.QuestionOptions, QuestionOptionsModelAdmin)
admin.site.register(survey.OptionSubCategory)
