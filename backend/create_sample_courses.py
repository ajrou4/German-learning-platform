"""
Script to create sample German courses for testing.
Run with: python manage.py shell < create_sample_courses.py
"""

from courses.models import Course, Module
from lessons.models import Lesson, Vocabulary

# Clear existing data (optional)
print("Creating sample courses...")

# Create A1 Course
a1_course = Course.objects.create(
    title="German for Absolute Beginners",
    description="Start your German learning journey! Learn basic greetings, introductions, and everyday phrases.",
    level="A1",
    order=1,
    is_published=True
)

# Create A2 Course
a2_course = Course.objects.create(
    title="Elementary German",
    description="Build on your basics! Learn to talk about your daily routine, hobbies, and simple past events.",
    level="A2",
    order=2,
    is_published=True
)

# Create B1 Course
b1_course = Course.objects.create(
    title="Intermediate German",
    description="Take your German to the next level! Discuss opinions, make plans, and understand longer texts.",
    level="B1",
    order=3,
    is_published=True
)

# Create B2 Course
b2_course = Course.objects.create(
    title="Upper Intermediate German",
    description="Master complex grammar and vocabulary. Understand news, movies, and have detailed conversations.",
    level="B2",
    order=4,
    is_published=True
)

# Create C1 Course
c1_course = Course.objects.create(
    title="Advanced German",
    description="Achieve fluency! Express yourself spontaneously and use German flexibly in professional contexts.",
    level="C1",
    order=5,
    is_published=True
)

# Create C2 Course
c2_course = Course.objects.create(
    title="Proficient German",
    description="Perfect your German! Understand virtually everything and express yourself with precision.",
    level="C2",
    order=6,
    is_published=True
)

# Add modules to A1 course
module1 = Module.objects.create(
    course=a1_course,
    title="Greetings and Introductions",
    description="Learn how to greet people and introduce yourself in German.",
    order=1
)

module2 = Module.objects.create(
    course=a1_course,
    title="Numbers and Time",
    description="Master German numbers, dates, and telling time.",
    order=2
)

module3 = Module.objects.create(
    course=a1_course,
    title="Family and Friends",
    description="Talk about your family members and friends.",
    order=3
)

# Add some sample lessons to Module 1
lesson1 = Lesson.objects.create(
    module=module1,
    title="Basic Greetings",
    description="Learn essential German greetings for different times of day.",
    content="""
# Basic Greetings in German

## Morning Greetings
- **Guten Morgen** - Good morning
- **Morgen** - Morning (informal)

## Afternoon/Evening
- **Guten Tag** - Good day
- **Guten Abend** - Good evening

## Informal Greetings
- **Hallo** - Hello
- **Hi** - Hi
- **Servus** - Hi/Bye (Southern Germany/Austria)

## Saying Goodbye
- **Auf Wiedersehen** - Goodbye (formal)
- **Tschüss** - Bye (informal)
- **Bis bald** - See you soon
    """,
    lesson_type="READING",
    order=1,
    estimated_duration=15
)

lesson2 = Lesson.objects.create(
    module=module1,
    title="Introducing Yourself",
    description="Learn how to introduce yourself and ask for names.",
    content="""
# Introducing Yourself

## Basic Introduction
- **Ich heiße...** - My name is...
- **Ich bin...** - I am...
- **Wie heißt du?** - What's your name? (informal)
- **Wie heißen Sie?** - What's your name? (formal)

## Examples
- Hallo! Ich heiße Anna. - Hello! My name is Anna.
- Guten Tag! Ich bin Thomas. - Good day! I am Thomas.

## Asking About Others
- **Wie geht es dir?** - How are you? (informal)
- **Wie geht es Ihnen?** - How are you? (formal)

## Responses
- **Gut, danke!** - Good, thanks!
- **Sehr gut!** - Very good!
- **Es geht.** - So-so.
    """,
    lesson_type="READING",
    order=2,
    estimated_duration=20
)

# Add vocabulary for lesson 1
vocab_words = [
    ("Guten Morgen", "Good morning", "Greeting used in the morning"),
    ("Hallo", "Hello", "Informal greeting"),
    ("Auf Wiedersehen", "Goodbye", "Formal farewell"),
    ("Tschüss", "Bye", "Informal farewell"),
    ("Danke", "Thank you", "Expression of gratitude"),
    ("Bitte", "Please/You're welcome", "Polite request or response to thanks"),
]

for german, english, notes in vocab_words:
    Vocabulary.objects.create(
        lesson=lesson1,
        german_word=german,
        english_translation=english,
        example_sentence=f"Example: {german}",
        notes=notes
    )

print(f"✅ Created {Course.objects.count()} courses")
print(f"✅ Created {Module.objects.count()} modules")
print(f"✅ Created {Lesson.objects.count()} lessons")
print(f"✅ Created {Vocabulary.objects.count()} vocabulary words")

print("\nCourses created:")
for course in Course.objects.all():
    print(f"  - {course.level}: {course.title}")
