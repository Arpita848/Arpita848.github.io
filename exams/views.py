from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Exam, Question, Option, UserExamResult

def home(request):
    return render(request, 'exams/home.html')

@login_required
def dashboard(request):
    user = request.user
    exams = Exam.objects.all()
    results = UserExamResult.objects.filter(user=user)

    # Prepare data for Chart.js
    labels = [res.exam.title for res in results]  # Exam titles
    scores = [res.score for res in results]       # Scores

    # Analytics
    total_attempts = results.count()
    avg_score = sum(scores)/total_attempts if total_attempts > 0 else 0

    context = {
        'exams': exams,
        'results': results,
        'labels': labels,
        'scores': scores,
        'total_attempts': total_attempts,
        'avg_score': round(avg_score, 2)
    }

    return render(request, 'exams/dashboard.html', context)

def take_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    return render(request, 'exams/take_exam.html', {'exam': exam})

def submit_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    questions = exam.questions.all()
    score = 0

    for question in questions:
        selected_option_id = request.POST.get(f'question_{question.id}')
        if selected_option_id:
            selected_option = Option.objects.get(id=selected_option_id)
            if selected_option.is_correct:
                score += 1

    UserExamResult.objects.create(user=request.user, exam=exam, score=score)

    return render(request, 'exams/exam_results.html', {
        'exam': exam,
        'score': score,
        'total': questions.count()
    })
