from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Question, Answer, QuestionVotedUser, AnswerVotedUser

User = get_user_model()


def get_profile_questions(request, username):
    profile = User.objects.get(username=username)
    profile_questions_list = Question.objects.filter(question_asker=profile)
    context = {
        'questions_list': profile_questions_list
    }
    return render(request, 'questions/profile_questions_list.html', context)


def get_profile_answers(request, username):
    profile = User.objects.get(username=username)
    profile_answers_list = Answer.objects.filter(answerer=profile)
    context = {
        'profile_answers_list': profile_answers_list
    }
    return render(request, 'questions/profile_answers_list.html', context)


def get_question(request, question_title):
    user = request.user
    question = Question.objects.get(question_title=question_title)
    answer = question.answer_set.all()
    queupvote = request.GET.get('queupvote' or None)
    quedownvote = request.GET.get('quedownvote' or None)
    ansupvote = request.GET.get('ansupvote' or None)
    ansdownvote = request.GET.get('ansdownvote' or None)
    fetched_answer = None
    if request.GET.get('ans_number'):
        fetched_answer = answer[int(request.GET.get('ans_number')) - 1]

    if queupvote or quedownvote or ansupvote or ansdownvote:
        if user.is_authenticated:
            try:
                try:
                    ansVotedUser = AnswerVotedUser.objects.get(
                        Q(answer=fetched_answer),
                        Q(voting_user=user),
                        Q(voting_value=1) | Q(voting_value=-1))

                except:
                    if request.GET['ansupvote']:
                        AnswerVotedUser.objects.create(answer=fetched_answer, voting_user=user, voting_value=1)
                        messages.add_message(request, messages.SUCCESS, 'You upvoted this answer.')
                    elif request.GET['ansdownvote']:
                        AnswerVotedUser.objects.create(question=question, voting_user=user, voting_value=-1)
                        messages.add_message(request, messages.SUCCESS, 'You downvoted this answer.')
                else:
                    if ansupvote:
                        if ansVotedUser.voting_value == 1:
                            messages.add_message(request, messages.ERROR, 'You have already upvoted this answer.')
                        elif ansVotedUser.voting_value == -1:
                            ansVotedUser.voting_value = 1
                            ansVotedUser.save()
                            messages.add_message(request, messages.SUCCESS, 'You upvoted this answer.')
                    elif ansdownvote:
                        if ansVotedUser.voting_value == 1:
                            ansVotedUser.voting_value = -1
                            ansVotedUser.save()
                            messages.add_message(request, messages.SUCCESS, 'You downvoted this answer.')
                        elif ansVotedUser.voting_value == -1:
                            messages.add_message(request, messages.ERROR, 'You have already downvoted this answer.')
            except:
                try:
                    queVotedUser = QuestionVotedUser.objects.get(
                                Q(question=question),
                                Q(voting_user=user),
                                Q(voting_value=1) | Q(voting_value=-1))

                except:
                    if request.GET['queupvote']:
                        QuestionVotedUser.objects.create(question=question, voting_user=user, voting_value=1)
                        messages.add_message(request, messages.SUCCESS, 'You upvoted this question.')
                    elif request.GET['quedownvote']:
                        QuestionVotedUser.objects.create(question=question, voting_user=user, voting_value=-1)
                        messages.add_message(request, messages.SUCCESS, 'You downvoted this question.')
                else:
                    if queupvote:
                        if queVotedUser.voting_value == 1:
                            messages.add_message(request, messages.ERROR, 'You have already upvoted this question.')
                        elif queVotedUser.voting_value == -1:
                            queVotedUser.voting_value = 1
                            queVotedUser.save()
                            messages.add_message(request, messages.SUCCESS, 'You upvoted this question.')
                    elif quedownvote:
                        if queVotedUser.voting_value == 1:
                            queVotedUser.voting_value = -1
                            queVotedUser.save()
                            messages.add_message(request, messages.SUCCESS, 'You downvoted this question.')
                        elif queVotedUser.voting_value == -1:
                            messages.add_message(request, messages.ERROR, 'You have already downvoted this question.')
        else:
            messages.add_message(request, messages.ERROR, 'You should be logged in to upvote or downvote.')


    if question:
        context = {
            'question': question,
            'answer': answer,
            'errors': None,
            'user': user
        }
        return render(request, 'questions/question_card.html', context=context)
    return render(request, 'questions/question_card.html', {'errors': 'No such question exists.'})


def get_all_users(request):
    user_list = User.objects.all()
    context = {
        'users': user_list
    }
    return render(request, 'questions/all_users.html', context=context)


@login_required
def userFeed(request):
    user = request.user
#     Find all the people this user follow and fetch the answers of these people and populate the feed
    following_qs = user.following.all()
    # This question card will contain question and its answer object
    question_card = []
    for obj in following_qs:
        person = obj.following_user_id
        for answer in person.answer_set.all():
            question_card.append({
                'question': answer.question,
                'answer': answer
            })
    context = {
        'question_card': question_card,
        'user_name': request.user.get_full_name
    }
    return render(request, 'questions/userfeed.html', context=context)


