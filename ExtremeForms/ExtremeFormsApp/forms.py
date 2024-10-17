from django import forms
from ExtremeFormsApp.models import Question
from collections import defaultdict


# class MultipleChoiceQuestionForm(forms.Form):
#     question_text = forms.CharField(label='Question', max_length=200)

#     def __init__(self, *args, options=None, **kwargs):
#         super().__init__(*args, **kwargs)
#         options = options or []

#         for i, option_text in enumerate(options, start=1):
#             self.fields[f'option_{i}'] = forms.CharField(
#                 label=f'Option {chr(96 + i).upper()}',
#                 max_length=100,
#                 initial=option_text,
#                 required=True
#             )

# class LongAnswerQuestionForm(forms.Form):
#     question_text = forms.CharField(label='Question', max_length=200)
#     long_answer_text = forms.CharField(
#         label='Answer',
#         widget=forms.Textarea,
#         required=False
#     )

# class AddQuestionForm(forms.ModelForm):
#     class Meta:
#         model = Question
#         fields = ['question_text', 'question_type', 'multiple_choice_options', 'long_answer_text']
#         widgets = {
#             'question_type': forms.Select(choices=Question.QUESTION_TYPES),
#             'multiple_choice_options': forms.HiddenInput(),  # Hidden by default, visible with JavaScript
#         }


def count_multiple_choice_answers(question):
    counts = defaultdict(int)
    for answer in question.answers.all():
        if answer.selected_option:  # Assuming you have a field for selected options
            counts[answer.selected_option] += 1
    return counts