from django.test import TestCase
from terms.models import *
# Create your tests here.


class TermsAccessibilityTest(TestCase):
    def setUp(self):
        Category.objects.create(name='cat1')
        # create users
        user1 = User.objects.create_user('john', 'john@thebeatles.com', 'johnpassword')
        user2 = User.objects.create_user('paul', 'paul@thebeatles.com', 'paulpassword')
        user3 = User.objects.create_user('george', 'george@thebeatles.com', 'georgepassword')
        user4 = User.objects.create_user('ringo', 'ringo@thebeatles.com', 'ringopassword')
        # create terms
        term1 = Term.objects.create(name='term #1', definition="sample description",
         category=Category.objects.get(name='cat1'),
          user=User.objects.get(username='john'))
        term2 = Term.objects.create(name='term #2', definition="sample description",
         category=Category.objects.get(name='cat1'),
          user=User.objects.get(username='paul'))
        # grant access to terms for users
        term1.grant_access(user1, user2)
        term2.grant_access(user3)

    def test_accessibility(self):
        self.assertGreater(Term.objects.get(name='term #1').popularity, Term.objects.get(name='term #2').popularity)

    def tearDown(self):
        Term.objects.get(name='term #2').forbid_access(User.objects.get(username='george'))
        Term.objects.get(name='term #1').forbid_access(User.objects.get(username='john'), User.objects.get(username='paul'))
        # delete terms
        Term.objects.get(name='term #2').delete()
        Term.objects.get(name='term #1').delete()
        # delete users
        User.objects.get(username='ringo').delete()
        User.objects.get(username='george').delete()
        User.objects.get(username='paul').delete()
        User.objects.get(username='john').delete()
        Category.objects.get(name='cat1').delete()
