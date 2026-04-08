from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .models import Answer, ExamAttempt, Question, Subject


def home(request: HttpRequest) -> HttpResponse:
    subjects = Subject.objects.prefetch_related("questions").all()
    return render(request, "exam/home.html", {"subjects": subjects})


def take_exam(request: HttpRequest, subject_id: int) -> HttpResponse:
    subject = get_object_or_404(Subject, pk=subject_id)
    questions = list(Question.objects.filter(subject=subject))

    if request.method == "POST":
        attempt = ExamAttempt.objects.create(subject=subject)

        answers_to_create: list[Answer] = []
        for q in questions:
            raw = request.POST.get(f"q_{q.id}")
            selected = int(raw) if raw in {"1", "2", "3", "4"} else None
            is_correct = selected == q.correct_option
            answers_to_create.append(
                Answer(
                    attempt=attempt,
                    question=q,
                    selected_option=selected,
                    is_correct=is_correct,
                )
            )

        Answer.objects.bulk_create(answers_to_create)
        return redirect(reverse("exam:results", kwargs={"attempt_id": attempt.id}))

    return render(
        request,
        "exam/take_exam.html",
        {"questions": questions, "subject": subject},
    )


def results(request: HttpRequest, attempt_id: int) -> HttpResponse:
    attempt = get_object_or_404(ExamAttempt, pk=attempt_id)
    total_questions = attempt.answers.count()
    answered = attempt.answers.exclude(selected_option__isnull=True).count()
    unanswered = total_questions - answered
    correct = attempt.answers.filter(is_correct=True).count()
    wrong = attempt.answers.filter(
        selected_option__isnull=False, is_correct=False
    ).count()
    return render(
        request,
        "exam/results.html",
        {
            "attempt": attempt,
            "subject": attempt.subject,
            "total_questions": total_questions,
            "answered": answered,
            "unanswered": unanswered,
            "correct": correct,
            "wrong": wrong,
        },
    )


def wrong_answers(request: HttpRequest, attempt_id: int) -> HttpResponse:
    attempt = get_object_or_404(ExamAttempt, pk=attempt_id)
    wrong_qs = (
        Answer.objects.select_related("question")
        .filter(attempt=attempt, selected_option__isnull=False, is_correct=False)
        .order_by("question_id")
    )
    return render(
        request,
        "exam/wrong_answers.html",
        {
            "attempt": attempt,
            "wrong_answers": wrong_qs,
        },
    )


def unanswered_answers(request: HttpRequest, attempt_id: int) -> HttpResponse:
    attempt = get_object_or_404(ExamAttempt, pk=attempt_id)
    unanswered_qs = (
        Answer.objects.select_related("question")
        .filter(attempt=attempt, selected_option__isnull=True)
        .order_by("question_id")
    )
    return render(
        request,
        "exam/unanswered_answers.html",
        {
            "attempt": attempt,
            "unanswered_answers": unanswered_qs,
        },
    )
