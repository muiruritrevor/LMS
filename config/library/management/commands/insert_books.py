from django.core.management.base import BaseCommand
from library.models import Book
from django.utils.dateparse import parse_date

class Command(BaseCommand):
    help = 'Bulk insert sample books into the database'

    def handle(self, *args, **options):
        books_data = [
            {
                "title": "To Kill a Mockingbird",
                "author": "Harper Lee",
                "isbn": "9780446310789",
                "publish_date": "1960-07-11",
                "genre": "Fiction",
                "total_copies": 5,
                "available_copies": 5,
                "status": Book.Status.AVAILABLE
            },
            {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "isbn": "9780743273565",
                "publish_date": "1925-04-10",
                "genre": "Fiction",
                "total_copies": 4,
                "available_copies": 4,
                "status": Book.Status.AVAILABLE
            },
            {
                "title": "Weep Not, Child",
                "author": "Ngũgĩ wa Thiong'o",
                "isbn": "9780143106692",
                "publish_date": "1964-01-17",
                "genre": "African Literature",
                "total_copies": 3,
                "available_copies": 3,
                "status": Book.Status.AVAILABLE
            },
            {
                "title": "A Grain of Wheat",
                "author": "Ngũgĩ wa Thiong'o",
                "isbn": "9780143106760",
                "publish_date": "1967-06-30",
                "genre": "African Literature",
                "total_copies": 2,
                "available_copies": 2,
                "status": Book.Status.AVAILABLE
            },
            {
                "title": "The Power of Now",
                "author": "Eckhart Tolle",
                "isbn": "9781577314806",
                "publish_date": "1997-09-29",
                "genre": "Self-help",
                "total_copies": 5,
                "available_copies": 5,
                "status": Book.Status.AVAILABLE
            },
            {
                "title": "Atomic Habits",
                "author": "James Clear",
                "isbn": "9780735211292",
                "publish_date": "2018-10-16",
                "genre": "Self-help",
                "total_copies": 6,
                "available_copies": 6,
                "status": Book.Status.AVAILABLE
            },
            {
                "title": "Think and Grow Rich",
                "author": "Napoleon Hill",
                "isbn": "9781585424337",
                "publish_date": "1937-03-26",
                "genre": "Self-help/Finance",
                "total_copies": 4,
                "available_copies": 4,
                "status": Book.Status.AVAILABLE
            },
            {
                "title": "The Intelligent Investor",
                "author": "Benjamin Graham",
                "isbn": "9780060555665",
                "publish_date": "1949-10-01",
                "genre": "Finance",
                "total_copies": 3,
                "available_copies": 3,
                "status": Book.Status.AVAILABLE
            },
            {
                "title": "A Brief History of Time",
                "author": "Stephen Hawking",
                "isbn": "9780553380163",
                "publish_date": "1988-04-01",
                "genre": "Science/Cosmology",
                "total_copies": 4,
                "available_copies": 4,
                "status": Book.Status.AVAILABLE
            },
            {
                "title": "Cosmos",
                "author": "Carl Sagan",
                "isbn": "9780345539434",
                "publish_date": "1980-09-28",
                "genre": "Science/Astronomy",
                "total_copies": 3,
                "available_copies": 3,
                "status": Book.Status.AVAILABLE
            },
            {
                "title": "The Total Money Makeover",
                "author": "Dave Ramsey",
                "isbn": "9781595555274",
                "publish_date": "2003-09-11",
                "genre": "Personal Finance",
                "total_copies": 4,
                "available_copies": 4,
                "status": Book.Status.AVAILABLE
            },
            {
                "title": "Astrophysics for People in a Hurry",
                "author": "Neil deGrasse Tyson",
                "isbn": "9780393609394",
                "publish_date": "2017-05-02",
                "genre": "Science/Astrophysics",
                "total_copies": 4,
                "available_copies": 4,
                "status": Book.Status.AVAILABLE
            },
            {
                "title": "Mindset: The New Psychology of Success",
                "author": "Carol S. Dweck",
                "isbn": "9780345472328",
                "publish_date": "2006-02-28",
                "genre": "Self-help/Psychology",
                "total_copies": 3,
                "available_copies": 3,
                "status": Book.Status.AVAILABLE
            },
            {
                "title": "The Universe in a Nutshell",
                "author": "Stephen Hawking",
                "isbn": "9780553802023",
                "publish_date": "2001-11-06",
                "genre": "Science/Cosmology",
                "total_copies": 3,
                "available_copies": 3,
                "status": Book.Status.AVAILABLE
            },
            {
                "title": "You Are a Badass at Making Money",
                "author": "Jen Sincero",
                "isbn": "9780735222977",
                "publish_date": "2017-04-18",
                "genre": "Self-help/Finance",
                "total_copies": 4,
                "available_copies": 4,
                "status": Book.Status.AVAILABLE
            },
            {
                "title": "The Elegant Universe",
                "author": "Brian Greene",
                "isbn": "9780375708114",
                "publish_date": "1999-10-11",
                "genre": "Science/Physics",
                "total_copies": 3,
                "available_copies": 3,
                "status": Book.Status.AVAILABLE
            }
        ]

        # Convert string dates to date objects
        for book in books_data:
            book['publish_date'] = parse_date(book['publish_date'])

        books_to_create = [Book(**book_data) for book_data in books_data]
        
        # Use bulk_create to insert all books at once
        created_books = Book.objects.bulk_create(books_to_create)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully added {len(created_books)} books to the database'))