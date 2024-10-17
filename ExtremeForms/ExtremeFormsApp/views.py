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
from django.urls import reverse


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
            'forms': QuestionList.objects.filter(user=request.user),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        if request.POST.get('action') == 'create':
            form_name = request.POST.get('form_name')
            new_form = QuestionList.objects.create(name=form_name, user=request.user)
            new_form.form_link = request.build_absolute_uri(reverse('ExtremeFormsApp:answer_form', args=[new_form.id]))
            new_form.save()

            return redirect('ExtremeFormsApp:new_form_initiated', question_list_id=new_form.id)

        context = {
            'forms': QuestionList.objects.filter(user=request.user),
        }
        return render(request, self.template_name, context)

class NewFormInitiatedView(LoginRequiredMixin, View):
    template_name = 'ExtremeFormsApp/new_form_initiated.html'

    def get(self, request, question_list_id):
        # Fetch the QuestionList or return a 404 if not found
        question_list = get_object_or_404(QuestionList, id=question_list_id)

        # Retrieve related questions and include question type and labeled options
        questions_with_options = []
        for question in question_list.questions.all():
            if question.question_type == 'multiple_choice':
                # Access options from the dict pattern
                options_dict = question.multiple_choice_options or {"options": []}
                labeled_options = [(chr(97 + i), option) for i, option in enumerate(options_dict.get("options", []))]
            else:
                labeled_options = []  # No options for non-multiple choice questions

            questions_with_options.append((question, question.question_type, labeled_options))

        # Prepare context with questions, types, and labeled options
        context = {
            'question_list': question_list,
            'questions_with_options': questions_with_options,
        }
        return render(request, self.template_name, context)

    def post(self, request, question_list_id):
        question_list = get_object_or_404(QuestionList, id=question_list_id)

        if request.POST.get('action') == 'add-multiple-choice':
            new_question = Question.objects.create(
                question_list=question_list,
                question_type='multiple_choice',
                text='',
                multiple_choice_options={"options": []}  # Initialize as empty dict
            )

        elif request.POST.get('action') == 'add-long-answer':
            new_question = Question.objects.create(
                question_list=question_list,
                question_type='long_answer',
                text='',
            )

        elif request.POST.get('action') == 'finish':
            return redirect('ExtremeFormsApp:form_created_success', question_list_id=question_list.id)
        
        elif request.POST.get('action') == 'save':
            question_id = request.POST.get('question_id')
            question = get_object_or_404(Question, id=question_id)

            # Save the question text
            question.text = request.POST.get('question_text')
            
            # Save the options in the dict format
            option_texts = []
            for i in range(len(question.multiple_choice_options.get("options", []))):
                option_text = request.POST.get(f'option_text_{i}')
                if option_text:
                    option_texts.append(option_text)

            question.multiple_choice_options = {"options": option_texts}  # Store as dict
            question.save()

        elif request.POST.get('action') == 'add-option':
            question_id = request.POST.get('question_id')
            question = get_object_or_404(Question, id=question_id)
            
            # Retrieve existing options and append a new empty one
            options = question.multiple_choice_options.get("options", [])
            options.append('')  # Add an empty option for user to fill in
            question.multiple_choice_options = {"options": options}
            question.save()

        elif request.POST.get('action') == 'remove-last-option':
            question_id = request.POST.get('question_id')
            question = get_object_or_404(Question, id=question_id)
            
            # Remove the last option
            options = question.multiple_choice_options.get("options", [])
            if options:  # Check if there are options to remove
                options.pop()  # Remove the last option
                
                # Update multiple_choice_options after removing the option
                question.multiple_choice_options = {"options": options}
                question.save()

        elif request.POST.get('action') == 'remove-question':
            question_id = request.POST.get('question_id')
            question = get_object_or_404(Question, id=question_id)
            question.delete()  # Remove the question from the database

        return redirect('ExtremeFormsApp:new_form_initiated', question_list_id=question_list.id)


@login_required
def form_created_success(request, question_list_id):
    question_list = get_object_or_404(QuestionList, id=question_list_id)
    
    context = {
        'question_list': question_list,
    }
    return render(request, 'ExtremeFormsApp/form_created_success.html', context)


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
    question_list = get_object_or_404(QuestionList, id=id)
    questions = question_list.questions.all()

    # Prepare option counts as a list of dictionaries for easier template access
    option_counts = []

    # Iterate over questions to collect data
    for question in questions:
        if question.question_type == 'multiple_choice':
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
        'form': question_list,
        'questions': questions,
        'answers': Answer.objects.filter(question__question_list=question_list),  # Corrected line
        'option_counts': option_counts,  # Pass the simplified structure to the template
    }

    print(option_counts)  # Add this to check the output of option_counts

    return render(request, 'ExtremeFormsApp/form_result.html', context)


class AnswerFormView(LoginRequiredMixin, View):
    template_name = 'ExtremeFormsApp/answer_form.html'

    def get(self, request, question_list_id):
        question_list = get_object_or_404(QuestionList, id=question_list_id)
        questions = question_list.questions.all()
        
        # Prepare the context with the questions
        context = {
            'question_list': question_list,
            'questions': questions,
        }
        return render(request, self.template_name, context)

    def post(self, request, question_list_id):
        question_list = get_object_or_404(QuestionList, id=question_list_id)
        
        for question in question_list.questions.all():
            if question.question_type == 'multiple_choice':
                answer_text = request.POST.get(f'multiple_choice_answer_{question.id}')
                Answer.objects.create(
                    question=question,
                    multiple_choice_answer=answer_text
                )
            elif question.question_type == 'long_answer':
                answer_text = request.POST.get(f'long_answer_{question.id}')
                Answer.objects.create(
                    question=question,
                    long_answer_answer=answer_text
                )

        # Redirect to a success page or back to the form list
        return redirect('ExtremeFormsApp:form_answered_success', question_list_id=question_list.id)


@login_required
def form_answered_success(request, question_list_id):
    question_list = get_object_or_404(QuestionList, id=question_list_id)
    return render(request, 'ExtremeFormsApp/form_answered_success.html', {'question_list': question_list})

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
