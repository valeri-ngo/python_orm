from datetime import date


# Create your models here.

class Student(models.Model):
    student_id = models.CharField(
        max_length=10,
        primary_key=True
    )
    first_name = models.CharField(
        max_length=100
    )
    last_name = models.CharField(
        max_length=100
    )
    birth_date = models.DateField()
    email = models.EmailField(
        unique=True
    )
    subjects = models.ManyToManyField(
        to='Subject',
        through='StudentEnrollment'
    )

class StudentEnrollment(models.Model):

    GRADE_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('F', 'F'),
    )

    student = models.ForeignKey(
        to='Student',
        on_delete=models.CASCADE
    )
    subject = models.ForeignKey(
        to='Subject',
        on_delete=models.CASCADE
    )
    enrollment_date = models.DateField(
        default=date.today
    )
    grade = models.CharField(
        max_length=1,
        choices=GRADE_CHOICES
    )
