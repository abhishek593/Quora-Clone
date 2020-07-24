from django.db import models
from django.conf import settings


class QuestionVotedUser(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    voting_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    voting_value = models.IntegerField()

    class Meta:
        unique_together = ('question', 'voting_user')


class Question(models.Model):
    question_asker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question_title = models.CharField(max_length=120)
    question_description = models.TextField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.question_title[:30]

    @property
    def get_question_upvoters(self):
        qs = self.questionvoteduser_set.filter(voting_value=1)
        upvoters = []
        for upvoter in qs:
            upvoters.append(upvoter.voting_user)
        return upvoters

    @property
    def get_question_downvoters(self):
        qs = self.questionvoteduser_set.filter(voting_value=-1)
        downvoters = []
        for downvoter in qs:
            downvoters.append(downvoter.voting_user)
        return downvoters


class AnswerVotedUser(models.Model):
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
    voting_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    voting_value = models.IntegerField()

    class Meta:
        unique_together = ('answer', 'voting_user')


class Answer(models.Model):
    answerer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    answer_text = models.TextField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.answer_text[:30]

    @property
    def get_answer_upvoters(self):
        qs = self.answervoteduser_set.filter(voting_value=1)
        upvoters = []
        for upvoter in qs:
            upvoters.append(upvoter.voting_user)
        return upvoters

    @property
    def get_answer_downvoters(self):
        qs = self.answervoteduser_set.filter(voting_value=-1)
        downvoters = []
        for downvoter in qs:
            downvoters.append(downvoter.voting_user)
        return downvoters
