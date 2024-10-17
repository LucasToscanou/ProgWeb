import csv

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View

from .forms import count_multiple_choice_answers  # Uncomment if needed
from ExtremeFormsApp.models import Answer, Question, QuestionList


# Create your views here.
@login_required
def index(request):
    return render(request, 'ExtremeFormsApp/index.html')

@login_required
def form_result(request):
    return render(request, 'ExtremeFormsApp/form_result.html')


class NewFormView(LoginRequiredMixin, View):
    template_name = 'ExtremeFormsApp/new_form.html'

    def get(self, request):
        context = {
            'form_created': False,
            'forms': QuestionList.objects.filter(user=request.user),  # Fetch existing forms for the logged-in user
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form_created = False

        if request.POST.get('action') == 'create':
            form_name = request.POST.get('form_name')
            new_form = QuestionList.objects.create(name=form_name, user=request.user)
            form_created = True
            # Ensure to use the app name when redirecting
            return redirect('ExtremeFormsApp:new_form_initiated', question_list_id=new_form.id)

        elif request.POST.get('action') == 'save':
            # Logic to save questions will be implemented here
            pass

        context = {
            'form_created': form_created,
            'forms': QuestionList.objects.filter(user=request.user),
        }
        return render(request, self.template_name, context)

class NewFormInitiatedView(LoginRequiredMixin, View):
    template_name = 'ExtremeFormsApp/new_form.html'

    def get(self, request, question_list_id):
        # Fetch the QuestionList or return a 404 if not found
        question_list = get_object_or_404(QuestionList, id=question_list_id)

        # Get related questions, assuming a reverse relationship exists
        questions = question_list.questions.all()  # Adjust according to your model relationships

        # Render the new form initiation page with the relevant context
        context = {
            'question_list': question_list,
            'questions': questions,
            # Include any other context needed for rendering
        }
        return render(request, self.template_name, context)


class QuestionListView(LoginRequiredMixin, View):
    def get(self, request, question_list_id):
        question_lists = QuestionList.objects.all()

        # Print each instance
        # for question_list in question_lists:
        #     print(f'ID: {question_list.id}, Name: {question_list.name}, User: {question_list.user}, Created At: {question_list.created_at}')
        
        
        # questions = Question.objects.filter(questionList_id=question_list_id)
        # forms = []
        # for question in questions:
        #     if question.question_type == 'multiple_choice':
        #         form = MultipleChoiceQuestionForm()
        #         forms.append((form, question))
        #     elif question.question_type == 'long_answer':
        #         form = LongAnswerQuestionForm()
        #         forms.append((form, question))
        # context = {'forms': forms, 'question_list_id': question_list_id}
        context = {}
        return render(request, 'ExtremeFormsApp/answer_form.html', context)

    def post(self, request, question_list_id):
        # questions = Question.objects.filter(questionList_id=question_list_id)
        # for question in questions:
        #     if question.question_type == 'multiple_choice':
        #         form = MultipleChoiceQuestionForm(request.POST, options=question.multiple_choice_options)
        #         if form.is_valid():
        #             multiple_choice_answer = request.POST.get(f'option_{form.cleaned_data["option"]}')  # Get the selected option
        #             # Save the response for the multiple-choice question
        #             Answer.objects.create(
        #                 question=question,
        #                 questionList_id=question_list_id,
        #                 multiple_choice_answer=multiple_choice_answer
        #             )

        #     elif question.question_type == 'long_answer':
        #         form = LongAnswerQuestionForm(request.POST)
        #         if form.is_valid():
        #             long_answer_answer = form.cleaned_data['question_text']  # Get the answer text
        #             # Save the response for the long answer question
        #             Answer.objects.create(
        #                 question=question,
        #                 questionList_id=question_list_id,
        #                 long_answer_answer=long_answer_answer
        #             )

        return redirect('success_url')  # Redirect to a success page after saving answers
    
    
@login_required
def form_detail_view(request, id):
    questionList = get_object_or_404(QuestionList, id=id)  # Fetch the form or return 404 if not found
    context = {
        'form': questionList,
        'questions': questionList.questions.all()
    }
    print(context)
    return render(request, 'ExtremeFormsApp/form_details.html', context)

@login_required
def edit_form_view(request, id):
    questionList = get_object_or_404(QuestionList, id=id)
    return render(request, 'ExtremeFormsApp/edit_form.html', {'form': questionList})

@login_required
def delete_form_view(request, id):
    questionList = get_object_or_404(QuestionList, id=id)
    context = {'form': questionList}
    return render(request, 'ExtremeFormsApp/delete_form.html', context)

@login_required
def form_result_view(request, id):
    questionList = get_object_or_404(QuestionList, id=id)
    questions = questionList.questions.all()

    # Prepare option counts as a list of dictionaries for easier template access
    option_counts = []

    # Iterate over questions to collect data
    for question in questions:
        if question.type == 'multiple_choice':
            options = question.multiple_choice_options.get("options", [])
            question.options = [chr(65 + i) for i in range(len(options))]

            # Initialize option count dictionary for this question
            counts = {
                'question_id': question.id,
                'counts': {option: 0 for option in options}
            }

            # Count answers for this question
            answers = Answer.objects.filter(question=question)
            for answer in answers:
                if answer.multiple_choice_answer in counts['counts']:
                    counts['counts'][answer.multiple_choice_answer] += 1

            option_counts.append(counts)

    context = {
        'form': questionList,
        'questions': questions,
        'answers': Answer.objects.filter(question__questionList=questionList),
        'option_counts': option_counts,  # Pass the simplified structure to the template
    }
    return render(request, 'ExtremeFormsApp/form_result.html', context)




class UserFormsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        question_lists = QuestionList.objects.filter(user=request.user)
        return render(request, 'ExtremeFormsApp/user_forms.html', {'question_lists': question_lists})
    


@login_required
def download_csv(request, form_id):
    # Get questions related to the specific QuestionList (form_id)
    questions = Question.objects.filter(questionList_id=form_id)
    
    # Prepare the response for CSV download
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="form_results_{form_id}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Question', 'Answer'])  # Write headers

    # Iterate through questions to gather answers
    for question in questions:
        if question.type == 'multiple_choice':
            # Count answers for multiple-choice questions
            option_counts = count_multiple_choice_answers(question)  # Define this logic as needed
            for option, qty in option_counts.items():
                writer.writerow([question.text, f'{option}: {qty} resposta(s)'])
        elif question.type == 'long_answer':
            # Fetch answers specific to the current question
            answers = Answer.objects.filter(question=question)
            for answer in answers:
                writer.writerow([question.text, answer.long_answer_answer])

    return response
