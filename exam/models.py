from django.db import models

OPTION_CHOICES = (
    (1, "Option 1"),
    (2, "Option 2"),
    (3, "Option 3"),
    (4, "Option 4"),
)


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Question(models.Model):
    subject = models.ForeignKey(
        Subject, on_delete=models.PROTECT, related_name="questions", null=True, blank=True
    )
    question_text = models.TextField(unique=True)
    option_1 = models.CharField(max_length=255)
    option_2 = models.CharField(max_length=255)
    option_3 = models.CharField(max_length=255)
    option_4 = models.CharField(max_length=255)
    correct_option = models.PositiveSmallIntegerField(choices=OPTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return f"Q{self.pk}: {self.question_text[:60]}"

    def get_option_text(self, option_number: int) -> str:
        return {
            1: self.option_1,
            2: self.option_2,
            3: self.option_3,
            4: self.option_4,
        }[option_number]

    @property
    def correct_answer_text(self) -> str:
        return self.get_option_text(self.correct_option)


class ExamAttempt(models.Model):
    subject = models.ForeignKey(
        Subject, on_delete=models.PROTECT, related_name="attempts", null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        subject_name = self.subject.name if self.subject else "No subject"
        return f"Attempt #{self.pk} ({subject_name})"


class Answer(models.Model):
    attempt = models.ForeignKey(
        ExamAttempt, on_delete=models.CASCADE, related_name="answers"
    )
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    selected_option = models.PositiveSmallIntegerField(
        choices=OPTION_CHOICES, null=True, blank=True
    )
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("attempt", "question")

    def __str__(self) -> str:
        return f"Attempt {self.attempt_id} - Q{self.question_id}"

    @property
    def selected_answer_text(self) -> str | None:
        if self.selected_option is None:
            return None
        return self.question.get_option_text(self.selected_option)
