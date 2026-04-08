from django.urls import path

from . import views


app_name = "exam"

urlpatterns = [
    path("", views.home, name="home"),
    path("exam/<int:subject_id>/", views.take_exam, name="take_exam"),
    path("results/<int:attempt_id>/", views.results, name="results"),
    path("results/<int:attempt_id>/wrong/", views.wrong_answers, name="wrong_answers"),
    path(
        "results/<int:attempt_id>/unanswered/",
        views.unanswered_answers,
        name="unanswered_answers",
    ),
]

