from django import forms

class SubjectForm(forms.Form):
    subject_name = forms.CharField(
        label='Subject Name',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'bg-gray-300 rounded-xl px-4 py-6 w-full',
                                      'placeholder': 'korean'}),
        required=True,
    )

class GroupNameForm(forms.Form):
    group_name = forms.CharField(
        label='Group Name',
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'bg-gray-300 rounded-xl px-4 py-6 w-full',
                                      'placeholder': 'week 1'}),
        required=True,
    )