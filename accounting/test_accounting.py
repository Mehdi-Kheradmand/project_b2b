from django.test import TestCase
from django.contrib.auth import get_user_model
from accounting.models import CreditRequest
from django.urls import reverse
from rest_framework.test import APIClient
from phones.models import Phone
from celery import current_app as celery_app

User = get_user_model()


class AccountingTests(TestCase):

    def setUp(self):
        """Set up test data and Celery configuration."""
        # Create sellers and an admin user
        self.seller1 = User.objects.create_user(username='seller1', password='123456', credit_balance=0)
        self.seller2 = User.objects.create_user(username='seller2', password='123456', credit_balance=0)
        self.admin = User.objects.create_user(username='admin', password='123456', is_superuser=True)

        # Create phone objects
        self.phone1_id = Phone.objects.create(number="09187232987").id
        self.phone2_id = Phone.objects.create(number="09187232988").id
        self.phone3_id = Phone.objects.create(number="09187232989").id

        # Initialize API client
        self.client = APIClient()

        # Configure Celery for synchronous task execution
        celery_app.conf.task_always_eager = True
        celery_app.conf.task_eager_propagates = True

        # Define constants for test amounts
        self.CREDIT_AMOUNT = 1000
        self.RECHARGE_AMOUNT = 10
        self.RECHARGE_COUNT = 1000

    def test_credit_and_recharge(self):
        """Test credit requests, approvals, and phone recharge."""

        # Step 1: Submit credit requests for seller1
        self.client.force_authenticate(user=self.seller1)
        for _ in range(10):
            response = self.client.post(reverse('accounting:credit_request'), {
                'amount': self.CREDIT_AMOUNT,
            })
            self.assertEqual(response.status_code, 201, "Credit request failed")

        # Step 2: Approve all credit requests as admin
        self.client.force_authenticate(user=self.admin)
        for cr_request in CreditRequest.objects.all():
            credit_process_response = self.client.patch(
                reverse('accounting:credit_process', kwargs={"cr_id": cr_request.id}),
                data={'status': "approved"}
            )
            self.assertEqual(credit_process_response.status_code, 200, "Failed to approve credit request")
            cr_request.refresh_from_db()
            self.assertEqual(cr_request.status, 'approved', "CreditRequest status not updated")

        # Step 3: Verify seller1's credit balance after approvals
        seller1_balance = sum(
            [c_req.amount for c_req in CreditRequest.objects.filter(seller=self.seller1, status='approved')]
        )
        print(f"Seller1 balance after credit approval: {seller1_balance}")
        self.assertEqual(seller1_balance, self.CREDIT_AMOUNT * 10, "Seller1 balance mismatch after approval")

        # Step 4: Submit recharge requests for seller1
        self.client.force_authenticate(user=self.seller1)
        for _ in range(self.RECHARGE_COUNT):
            response = self.client.post(reverse('accounting:recharge_request'), {
                'amount': self.RECHARGE_AMOUNT,
                'phone': self.phone1_id
            })
            self.assertEqual(response.status_code, 201, "Recharge request failed")

        # Step 5: Verify seller1's final credit balance
        seller1_final_balance = seller1_balance - (self.RECHARGE_AMOUNT * self.RECHARGE_COUNT)
        self.seller1.refresh_from_db()
        self.assertEqual(self.seller1.credit_balance, seller1_final_balance, "Final balance mismatch for seller1")

        # Step 6: Verify seller2's credit balance remains unchanged
        self.seller2.refresh_from_db()
        self.assertEqual(self.seller2.credit_balance, 0, "Seller2 credit balance should remain 0")
