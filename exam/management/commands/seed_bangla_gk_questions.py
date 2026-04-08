from django.core.management.base import BaseCommand
from django.utils.text import slugify

from exam.models import Question, Subject


QUESTIONS = [
    {
        "question_text": "বাংলাদেশের রাজধানীর নাম কী?",
        "option_1": "চট্টগ্রাম",
        "option_2": "ঢাকা",
        "option_3": "রাজশাহী",
        "option_4": "খুলনা",
        "correct_option": 2,
    },
    {
        "question_text": "বাংলাদেশের জাতীয় পতাকার রঙ কোনটি?",
        "option_1": "সবুজ ও লাল",
        "option_2": "নীল ও সাদা",
        "option_3": "লাল ও হলুদ",
        "option_4": "কালো ও সাদা",
        "correct_option": 1,
    },
    {
        "question_text": "বাংলাদেশ স্বাধীনতা লাভ করে কোন সালে?",
        "option_1": "১৯৬৯",
        "option_2": "১৯৭০",
        "option_3": "১৯৭১",
        "option_4": "১৯৭২",
        "correct_option": 3,
    },
    {
        "question_text": "বাংলাদেশের জাতীয় ফুল কোনটি?",
        "option_1": "গোলাপ",
        "option_2": "শাপলা",
        "option_3": "সূর্যমুখী",
        "option_4": "জুঁই",
        "correct_option": 2,
    },
    {
        "question_text": "বাংলাদেশের জাতীয় ফল কোনটি?",
        "option_1": "আম",
        "option_2": "কাঁঠাল",
        "option_3": "কলা",
        "option_4": "লিচু",
        "correct_option": 2,
    },
    {
        "question_text": "বাংলাদেশের জাতীয় পাখি কোনটি?",
        "option_1": "দোয়েল",
        "option_2": "শালিক",
        "option_3": "কাক",
        "option_4": "টিয়া",
        "correct_option": 1,
    },
    {
        "question_text": "বাংলাদেশের সবচেয়ে বড় সমুদ্রবন্দর কোনটি?",
        "option_1": "মোংলা বন্দর",
        "option_2": "চট্টগ্রাম বন্দর",
        "option_3": "পায়রা বন্দর",
        "option_4": "নারায়ণগঞ্জ বন্দর",
        "correct_option": 2,
    },
    {
        "question_text": "বাংলাদেশের জাতীয় সঙ্গীতের রচয়িতা কে?",
        "option_1": "কাজী নজরুল ইসলাম",
        "option_2": "জসীমউদ্দীন",
        "option_3": "রবীন্দ্রনাথ ঠাকুর",
        "option_4": "শামসুর রাহমান",
        "correct_option": 3,
    },
    {
        "question_text": "বাংলাদেশের জাতীয় কবি কে?",
        "option_1": "রবীন্দ্রনাথ ঠাকুর",
        "option_2": "কাজী নজরুল ইসলাম",
        "option_3": "জীবনানন্দ দাশ",
        "option_4": "সুকান্ত ভট্টাচার্য",
        "correct_option": 2,
    },
    {
        "question_text": "বাংলাদেশে আন্তর্জাতিক মাতৃভাষা দিবস কবে পালিত হয়?",
        "option_1": "২১ ফেব্রুয়ারি",
        "option_2": "২৬ মার্চ",
        "option_3": "১৬ ডিসেম্বর",
        "option_4": "১৪ এপ্রিল",
        "correct_option": 1,
    },
    {
        "question_text": "বাংলাদেশের জাতীয় স্মৃতিসৌধ কোথায় অবস্থিত?",
        "option_1": "গাজীপুর",
        "option_2": "সাভার",
        "option_3": "কুমিল্লা",
        "option_4": "ময়মনসিংহ",
        "correct_option": 2,
    },
    {
        "question_text": "বাংলাদেশের দীর্ঘতম নদী কোনটি (বাংলাদেশ অংশে)?",
        "option_1": "যমুনা",
        "option_2": "পদ্মা",
        "option_3": "মেঘনা",
        "option_4": "তিস্তা",
        "correct_option": 1,
    },
    {
        "question_text": "বাংলাদেশের বৃহত্তম ম্যানগ্রোভ বন কোনটি?",
        "option_1": "রেমা-কালেঙ্গা",
        "option_2": "মধুপুর বন",
        "option_3": "সুন্দরবন",
        "option_4": "ভাওয়াল বন",
        "correct_option": 3,
    },
    {
        "question_text": "বাংলাদেশের মুদ্রার নাম কী?",
        "option_1": "রুপি",
        "option_2": "টাকা",
        "option_3": "দিনার",
        "option_4": "রিয়াল",
        "correct_option": 2,
    },
    {
        "question_text": "বাংলাদেশের জাতীয় সংসদের নাম কী?",
        "option_1": "জাতীয় পরিষদ",
        "option_2": "গণপরিষদ",
        "option_3": "জাতীয় সংসদ",
        "option_4": "পার্লামেন্ট হাউস",
        "correct_option": 3,
    },
    {
        "question_text": "বাংলাদেশের জাতীয় দিবস কোনটি?",
        "option_1": "১৬ ডিসেম্বর",
        "option_2": "২৬ মার্চ",
        "option_3": "২১ ফেব্রুয়ারি",
        "option_4": "১ মে",
        "correct_option": 2,
    },
    {
        "question_text": "বাংলাদেশের বিজয় দিবস কবে?",
        "option_1": "২৬ মার্চ",
        "option_2": "১৫ আগস্ট",
        "option_3": "১৬ ডিসেম্বর",
        "option_4": "২১ ফেব্রুয়ারি",
        "correct_option": 3,
    },
    {
        "question_text": "বাংলাদেশে নববর্ষ (পহেলা বৈশাখ) সাধারণত কোন তারিখে পালিত হয়?",
        "option_1": "১৪ এপ্রিল",
        "option_2": "১ জানুয়ারি",
        "option_3": "২১ মার্চ",
        "option_4": "৩০ জুন",
        "correct_option": 1,
    },
    {
        "question_text": "বাংলাদেশের প্রথম রাষ্ট্রপতি কে ছিলেন?",
        "option_1": "শেখ মুজিবুর রহমান",
        "option_2": "সৈয়দ নজরুল ইসলাম",
        "option_3": "জিয়াউর রহমান",
        "option_4": "এ. কিউ. এম. বদরুদ্দোজা চৌধুরী",
        "correct_option": 1,
    },
    {
        "question_text": "বাংলাদেশের সর্বোচ্চ পর্বতশৃঙ্গ কোনটি?",
        "option_1": "তাজিংডং",
        "option_2": "কেওক্রাডং",
        "option_3": "জাফলং পাহাড়",
        "option_4": "লালমাই পাহাড়",
        "correct_option": 1,
    },
]


class Command(BaseCommand):
    help = "Seed 20 Bangla Bangladeshi general knowledge MCQ questions"

    def handle(self, *args, **options):
        subject, _ = Subject.objects.get_or_create(
            name="সাধারণ জ্ঞান",
            defaults={
                "slug": slugify("general-knowledge-bn"),
                "description": "বাংলাদেশ বিষয়ক সাধারণ জ্ঞানের এমসিকিউ পরীক্ষা।",
            },
        )

        created_count = 0
        existing_count = 0

        for item in QUESTIONS:
            _, created = Question.objects.update_or_create(
                question_text=item["question_text"],
                defaults={
                    "subject": subject,
                    "option_1": item["option_1"],
                    "option_2": item["option_2"],
                    "option_3": item["option_3"],
                    "option_4": item["option_4"],
                    "correct_option": item["correct_option"],
                },
            )
            if created:
                created_count += 1
            else:
                existing_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeding complete. Created: {created_count}, Already existed: {existing_count}"
            )
        )

