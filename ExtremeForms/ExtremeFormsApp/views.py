from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import MultipleChoiceQuestionForm, LongAnswerQuestionForm
from ExtremeFormsApp.models import Question, QuestionList, Answer
from django.views import View
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def index(request):
    return render(request, 'ExtremeFormsApp/index.html')

def form_result(request):
    return render(request, 'ExtremeFormsApp/form_result.html')


class NewFormView(LoginRequiredMixin, View):
    template_name = 'ExtremeFormsApp/new_form.html'
    
    def get(self, request, *args, **kwargs):
        # Create a new QuestionList with a placeholder name
        questionList = QuestionList(name="placeholder", user=request.user)
        questionList.save()

        # Create the title question
        title = Question(question_text="Título do Form", question_type='title', questionList=questionList)
        title.save()

        questions = [title]  # Add more questions as needed
        forms = []

        # Prepare forms based on the question type
        for q in questions:
            if q.question_type == 'multiple_choice':
                form = MultipleChoiceQuestionForm(options=q.multiple_choice_options)
                forms.append((form, 'multiple_choice'))
            elif q.question_type == 'long_answer':
                form = LongAnswerQuestionForm()
                forms.append((form, 'long_answer'))

        context = {
            'questions': questions,
            'forms': forms,
            'questionList': questionList,  # Pass the questionList to the template
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # Create a new QuestionList with a placeholder name
        questionList = QuestionList(user=request.user)
        questionList.save()

        # Get the title from the POST request
        title_text = request.POST.get('title_text', "Título do Form")
        
        # Create the title question using the submitted title
        title = Question(question_text=title_text, question_type='title', questionList=questionList)
        title.save()

        # Update the questionList name with the title text and save it again
        questionList.questionList_name = title.question_text
        questionList.save()

        questions = [title]  # Add more questions if needed
        output = {}
        
        action = request.POST.get('action')  # Check which button was clicked

        if action == 'save':
            for index, q in enumerate(questions):
                if q.question_type == 'multiple_choice':
                    form = MultipleChoiceQuestionForm(request.POST, options=q.multiple_choice_options)
                    if form.is_valid():
                        question_text = form.cleaned_data['question_text']
                        options = [form.cleaned_data[f'option_{i}'] for i in range(1, len(q.multiple_choice_options) + 1)]
                        
                        # Save the multiple-choice question and options to the database
                        Question.objects.create(
                            questionList=questionList,
                            question_text=question_text,
                            question_type='multiple_choice',
                            multiple_choice_options={chr(65 + i): opt for i, opt in enumerate(options)}
                        )
                        
                        output[f'multiple_choice_question_{index}'] = {
                            'question_text': question_text,
                            'options': options
                        }
                    else:
                        print(f'Multiple choice question {index} errors:', form.errors)

                elif q.question_type == 'long_answer':
                    form = LongAnswerQuestionForm(request.POST)
                    if form.is_valid():
                        question_text = form.cleaned_data['question_text']
                        
                        # Save the long answer question to the database
                        Question.objects.create(
                            questionList=questionList,
                            question_text=question_text,
                            question_type='long_answer',
                            long_answer_text=question_text
                        )
                        
                        output[f'long_answer_question_{index}'] = {
                            'question_text': question_text
                        }
                    else:
                        print(f'Long answer question {index} errors:', form.errors)

            return redirect('success_url')  # Replace with your success URL

        # Re-render the form if there was an issue
        forms = []
        for q in questions:
            if q.question_type == 'multiple_choice':
                form = MultipleChoiceQuestionForm(options=q.multiple_choice_options)
                forms.append((form, 'multiple_choice'))
            elif q.question_type == 'long_answer':
                form = LongAnswerQuestionForm()
                forms.append((form, 'long_answer'))
        
        context = {
            'output': output,
            'questions': questions,
            'forms': forms,
            'questionList': questionList,  # Pass the questionList to the template
        }
        return render(request, self.template_name, context)



class QuestionListView(LoginRequiredMixin, View):
    def get(self, request, question_list_id):
        question_lists = QuestionList.objects.all()

        # Print each instance
        for question_list in question_lists:
            print(f'ID: {question_list.id}, Name: {question_list.name}, User: {question_list.user}, Created At: {question_list.created_at}')
        
        
        questions = Question.objects.filter(questionList_id=question_list_id)
        forms = []
        for question in questions:
            if question.question_type == 'multiple_choice':
                form = MultipleChoiceQuestionForm()
                forms.append((form, question))
            elif question.question_type == 'long_answer':
                form = LongAnswerQuestionForm()
                forms.append((form, question))
        context = {'forms': forms, 'question_list_id': question_list_id}
        return render(request, 'ExtremeFormsApp/answer_form.html', context)

    def post(self, request, question_list_id):
        questions = Question.objects.filter(questionList_id=question_list_id)
        for question in questions:
            if question.question_type == 'multiple_choice':
                form = MultipleChoiceQuestionForm(request.POST, options=question.multiple_choice_options)
                if form.is_valid():
                    multiple_choice_answer = request.POST.get(f'option_{form.cleaned_data["option"]}')  # Get the selected option
                    # Save the response for the multiple-choice question
                    Answer.objects.create(
                        question=question,
                        questionList_id=question_list_id,
                        multiple_choice_answer=multiple_choice_answer
                    )

            elif question.question_type == 'long_answer':
                form = LongAnswerQuestionForm(request.POST)
                if form.is_valid():
                    long_answer_answer = form.cleaned_data['question_text']  # Get the answer text
                    # Save the response for the long answer question
                    Answer.objects.create(
                        question=question,
                        questionList_id=question_list_id,
                        long_answer_answer=long_answer_answer
                    )

        return redirect('success_url')  # Redirect to a success page after saving answers