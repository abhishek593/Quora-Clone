from django.contrib import admin
from . import models

admin.site.register(models.Question)
admin.site.register(models.Answer)
admin.site.register(models.QuestionVotedUser)
admin.site.register(models.AnswerVotedUser)
