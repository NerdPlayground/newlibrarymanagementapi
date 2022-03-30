from students.models import Student
from library_cards.models import LibraryCard

def verify_patron(request):
    student= Student.objects.get(user=request.user)
    library_card= LibraryCard.objects.get(student=student)
    return library_card.active