from django.shortcuts import render, get_object_or_404, redirect
from .models import VocabularyWord, UserAnswer, Subject, GroupName
from django.urls import reverse
from .forms import SubjectForm, GroupNameForm
import random
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Django rest
from rest_framework import generics
from .models import VocabularyWord
from .serializers import VocabularyWordSerializer

# Create your views here.
def pt(name):
    print(f"\n{name} is started. . . \n\n")

# register login
def register(request):
    pt('register')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()  # Save the newly created user
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            new_user = form.save()  # Save the newly created user
            login(request, user)
            
            # Create associated data for the new user
            GroupName.objects.create(
                group_name='others',
                user=new_user  # Pass the new_user here
            )
            Subject.objects.create(
                name='english',
                user=new_user  # Pass the new_user here
            )
            VocabularyWord.objects.create(
                word='Welcome',
                definition='It is good to see you here!',
                subject=Subject.objects.get(name='english', user=new_user),  # Pass the new_user here
                group_by=GroupName.objects.get(group_name='others', user=new_user),  # Pass the new_user here
                user=new_user  # Pass the new_user here as well
            )
            return redirect('core:core')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})


def user_login(request):
    pt('user_login')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('core:core')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

@login_required
def core(request):
    pt('core')
    try:
        correct = UserAnswer.objects.filter(is_correct=True, user=request.user)[::-1]
        incorrect = UserAnswer.objects.filter(is_correct=False, user=request.user)[::-1]
        try:
                all_item_pks = request.session.get('all_items', [])
                # Retrieve the VocabularyWord objects using the primary keys
                all_items = VocabularyWord.objects.filter(pk__in=all_item_pks, user=request.user)
                print(all_items)
                for item in all_items:
                    vocabulary_word = random.choice(all_items)
                    if item in UserAnswer.objects.all():
                        vocabulary_word = random.choice(all_items)
                    else:
                        break
                subjects = Subject.objects.filter(user=request.user)
                groups = GroupName.objects.filter(user=request.user)
                context = {
                    'vocabulary_word': vocabulary_word,
                    'correct': correct,
                    'incorrect': incorrect,
                    'subjects': subjects,
                    'groups': groups,
                }
                print('try finish')
                return render(request, 'core/core.html', context)
        except:
            all_items = VocabularyWord.objects.filter(user=request.user)
            for item in all_items:
                vocabulary_word = random.choice(all_items)
                if item in UserAnswer.objects.filter(user=request.user):
                    vocabulary_word = random.choice(all_items)
                else:
                    break
            subjects = Subject.objects.filter(user=request.user)
            groups = GroupName.objects.filter(user=request.user)
            
            context = {
                'vocabulary_word': vocabulary_word,
                'correct': correct,
                'incorrect': incorrect,
                'subjects': subjects,
                'groups': groups,
                
            }
            return render(request, 'core/core.html', context)
    except:
        return redirect('core:manage_words')

@login_required
def core_reversed(request):
    pt('core_reversed')
    correct = UserAnswer.objects.filter(is_correct=True, user=request.user)[::-1]
    incorrect = UserAnswer.objects.filter(is_correct=False, user=request.user)[::-1]
    try:
        all_item_pks = request.session.get('all_items', [])
        # Retrieve the VocabularyWord objects using the primary keys
        all_items = VocabularyWord.objects.filter(user=request.user, pk__in=all_item_pks)
        print(all_items)
        for item in all_items:
            vocabulary_word = random.choice(all_items)
            if item in UserAnswer.objects.all():
                vocabulary_word = random.choice(all_items)
            else:
                break
        subjects = Subject.objects.filter(user=request.user)
        groups = GroupName.objects.filter(user=request.user)

        context = {
            'vocabulary_word': vocabulary_word,
            'correct': correct,
            'incorrect': incorrect,
            'subjects': subjects,
            'groups': groups,
            
        }
        print('try finish')
        return render(request, 'core/core_reversed.html', context)
    except:
        all_items = VocabularyWord.objects.filter(user=request.user)
        for item in all_items:
            vocabulary_word = random.choice(all_items)
            if item in UserAnswer.objects.filter(user=request.user):
                vocabulary_word = random.choice(all_items)
            else:
                break
        subjects = Subject.objects.filter(user=request.user)
        groups = GroupName.objects.filter(user=request.user)
        context = {
            'vocabulary_word': vocabulary_word,
            'correct': correct,
            'incorrect': incorrect,
            'subjects': subjects,
            'groups': groups,
        }
        return render(request, 'core/core_reversed.html', context)


def check_answer(request, vw):
    pt('check_answer')
    vocabulary_word = get_object_or_404(VocabularyWord, pk=vw)
    answer = str(request.POST.get('answer')).lower()
    print(f"Answer received: {answer}")
    if ', ' in vocabulary_word.definition:
        sd = vocabulary_word.definition.split(', ')
        print(sd)
        is_correct = answer in sd
    else:
        is_correct = answer == str(vocabulary_word.definition).lower()

    if answer is not None:
        user_answer = UserAnswer.objects.create(
            vocabulary_word=vocabulary_word,
            answer=answer,
            is_correct=is_correct,
            user = request.user
        )
    return redirect(reverse('core:core'))

def check_answer_reversed(request, vw):
    pt('check_answer_reversed')
    vocabulary_word = get_object_or_404(VocabularyWord, pk=vw)
    answer = str(request.POST.get('answer')).lower()
    print(f"Answer received: {answer}")
    is_correct = answer == str(vocabulary_word.word).lower()

    if answer is not None:
        user_answer = UserAnswer.objects.create(
            vocabulary_word=vocabulary_word,
            answer=answer,
            is_correct=is_correct,
            user = request.user
        )
    return redirect(reverse('core:core_reversed'))

def reset(request):
    pt('reset')
    UserAnswer.objects.all().delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def manage_words(request):
    pt('manage_words')
    subjects = Subject.objects.filter(user=request.user)
    groups = GroupName.objects.filter(user=request.user)
    
    vocabulary_words = VocabularyWord.objects.filter(user=request.user)
    subject_form = SubjectForm()
    group_form = GroupNameForm()
    return render(request, 'core/manage_words.html', {
        'words': vocabulary_words,
        'subject_form': subject_form,
        'group_form': group_form,
        'subjects': subjects,
        'groups': groups
    })

@login_required
def manage_words_filter(request, sub_name):
    pt('manage_words_filter')
    subjects = Subject.objects.filter(user=request.user)
    groups = GroupName.objects.filter(user=request.user)
    subject_form = SubjectForm()
    group_form = GroupNameForm()
    if sub_name != 'reset':
        if subject_form.is_valid() and group_form.is_valid():
            filter1 = VocabularyWord.objects.filter(Q(user=request.user) & Q(subject__name=sub_name))
            filter2 = VocabularyWord.objects.filter(Q(user=request.user) & Q(group_by__group_name=sub_name))
            vocabulary_words = filter1 | filter2
        else:
            vocabulary_words = VocabularyWord.objects.filter(user=request.user, subject__name=sub_name)
    else:
        vocabulary_words = VocabularyWord.objects.filter(user=request.user)     
    return render(request, 'core/manage_words.html', {
        'words': vocabulary_words,
        'subject_form': subject_form,
        'subjects': subjects,
        'group_form': group_form,
        'groups': groups,
    })

@login_required
def generate_words(request):
    pt('generate_words')
    if request.method == 'POST':
        subject_form = SubjectForm(request.POST)
        group_form = GroupNameForm(request.POST)

        if subject_form.is_valid():
            subject_name = subject_form.cleaned_data['subject_name'].lower()
            existing_subject = Subject.objects.filter(name=subject_name, user=request.user).first()
            if existing_subject is None:
                Subject.objects.create(name=subject_name, user=request.user)

        if group_form.is_valid():
            group_name = group_form.cleaned_data.get('group_name').lower()
            if group_name is not None:
                existing_group = GroupName.objects.filter(group_name=group_name, user=request.user).first()
                if existing_group is None:
                    GroupName.objects.create(group_name=group_name, user=request.user)

    
    input_string = request.POST.get('words')

    w = []
    d = []

    lines = input_string.strip().split('\n')

    for line in lines:
        parts = line.strip().split('-')
        if len(parts) == 2:
            w.append(parts[0].strip())
            d.append(parts[1].strip())
    if w and d:
        for i in range(len(w)):
            # Assuming subject_name is set correctly in your code
            subject_instance = Subject.objects.get(name=subject_name, user=request.user)
            group_instance = GroupName.objects.get(group_name=group_name, user=request.user)
            VocabularyWord.objects.create(
                group_by = group_instance,
                subject=subject_instance,
                word=w[i],
                definition=d[i],
                user=request.user,
            )

    return redirect('core:manage_words')

def delete_words(request):
    pt('delete_words')
    selected_words = request.POST.getlist('selected_words')
    VocabularyWord.objects.filter(pk__in=selected_words).delete()
    Subject.objects.filter(pk__in=selected_words).delete()
    GroupName.objects.filter(pk__in=selected_words).delete()

    vocabulary_words = VocabularyWord.objects.all()
    return redirect(reverse("core:manage_words"))

def core_filter(request, name):
    pt('core_filter')


    # Check if the name matches any Subject
    subject_match = Subject.objects.filter(name=name, user=request.user).exists()
    if subject_match:
        all_items = VocabularyWord.objects.filter(subject__name=name, user=request.user)
    else:
        all_items = VocabularyWord.objects.filter(group_by__group_name=name, user=request.user)

    request.session['all_items'] = list(all_items.values_list('pk', flat=True))


    # Redirect to 'core_reversed' without changing the URL
    link = request.META.get('HTTP_REFERER')
    if 'core_reversed' in link:
        return redirect(reverse("core:core_reversed"))
    else:
        return redirect(reverse("core:core"))

# Django rest
class VocabularyWordList(generics.ListCreateAPIView):
    queryset = VocabularyWord.objects.all()
    serializer_class = VocabularyWordSerializer

class VocabularyWordDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = VocabularyWord.objects.all()
    serializer_class = VocabularyWordSerializer
