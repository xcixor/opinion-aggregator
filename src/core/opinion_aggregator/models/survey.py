"""survey models
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from . import User

class SurveyModel(models.Model):
    """An investigation of a phenomenon

    Arguments:
        models {class} -- django model
    """
    short_description = models.CharField(
        _('Short description of the survey, required'),
        max_length=40,
        blank=False,
        null=False,
        unique=True)

    long_description = models.CharField(
        _('Long description of the survey, optional'),
        max_length=255,
        blank=True,
        null=True)

    class Meta:
        verbose_name_plural = "Surveys"

    def __str__(self):
        if self.long_description:
            description = ""
            description += self.short_description
            description += "\n\n"
            description += self.long_description
        return self.short_description


class PartModel(models.Model):
    """A part of a survey

    Arguments:
        models {class} -- django model
    """
    title = models.CharField(
        _('Name of the part, eg Part A'),
        max_length=40,
        blank=False,
        null=False)
    long_description = models.CharField(
        _('A more detailed description, e.g personal information'),
        max_length=255,
        blank=True,
        null=True)
    survey = models.ForeignKey(
        SurveyModel, related_name='parts',
        on_delete=models.CASCADE,
        null=False, blank=False)

    class Meta:
        verbose_name_plural = "Parts of a survey"
        unique_together = ('title', 'survey')

    def __str__(self):
        if self.long_description:
            description = ""
            description += self.title
            description += "\n\n"
            description += self.long_description
        return self.title


class SectionModel(models.Model):
    """An area of commonality

    Arguments:
        models {class} -- django model
    """
    title = models.CharField(
        _('Title of the section: eg personal info'),
        max_length=40,
        blank=False,
        null=False)
    long_description = models.CharField(
        _('Long description of this area'),
        max_length=255,
        blank=True,
        null=True)
    part = models.ForeignKey(
        PartModel, related_name='sections',
        on_delete=models.CASCADE,
        null=False, blank=False)

    class Meta:
        verbose_name_plural = "Sections of the survey"
        unique_together = ('title', 'part')

    def __str__(self):
        if self.long_description:
            description = ""
            description += self.title
            description += "\n\n"
            description += self.long_description
            return description
        return self.title


class QuestionModel(models.Model):
    """Defines a question in the survey

    Arguments:
        models {class} -- django model
    """
    description = models.CharField(
        _('Description of the question'),
        max_length=400,
        blank=False,
        null=False)
    section = models.ForeignKey(
        SectionModel, related_name='questions',
        on_delete=models.CASCADE,
        null=False, blank=False)

    class Meta:
        verbose_name_plural = "Questions"
        unique_together = ('description', 'section')

    def __str__(self):
        return self.description


class OptionModel(models.Model):
    """A potential answer to a question
    Arguments:
        models {class} -- django model
    """
    description = models.CharField(
        _('An answer to a question'),
        max_length=200,
        blank=False,
        null=False)

    class Meta:
        verbose_name_plural = "Options"

    def __str__(self):
        return self.description


class QuestionOptions(models.Model):
    """Options for a question

    Arguments:
        models {class} -- django model
    """
    question = models.ForeignKey(
        QuestionModel, related_name='options',
        on_delete=models.CASCADE,
        null=False, blank=False)

    option = models.ForeignKey(
        OptionModel, on_delete=models.CASCADE,
        null=False, blank=False)

    class Meta:
        verbose_name_plural = "Question Options"

    def __str__(self):
        return str(self.option)


class SurveyResponsesModel(models.Model):
    """User responses to a survey questions

    Arguments:
        models {class} -- django model
    """
    response = models.CharField(
        _('User response to the question'),
        max_length=255,
        blank=False,
        null=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        null=False, blank=False)

    question = models.ForeignKey(
        QuestionModel, related_name='responses',
        on_delete=models.CASCADE,
        null=False, blank=False)

    class Meta:
        verbose_name_plural = "Responses"

    def __str__(self):
        return self.response
