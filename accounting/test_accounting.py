from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model
from accounting.models import CreditRequest
from django.urls import reverse
from rest_framework.test import APIClient

from phones.models import Phone

User = get_user_model()


class AccountingTests(TestCase):

    def setUp(self):
        # creating two sellers and one admin
        self.seller1 = User.objects.create_user(username='seller1', password='123456')
        self.seller2 = User.objects.create_user(username='seller2', password='123456')

        self.admin = User.objects.create_user(username='admin', password='123456', is_superuser=True)

        # create phone
        self.phone1_id = Phone.objects.create(number="09187232987").id

        self.client = APIClient()

    @patch('accounting.views.recharge_task.delay')
    def test_credit_and_recharge(self, mock_recharge_task_delay):
        # Credit request 10 times for seller 1
        self.client.force_authenticate(user=self.seller1)  # seller 1 authenticate
        for _ in range(10):
            response = self.client.post(reverse('accounting:credit_request'), {
                'amount': 1000,
            })
            self.assertEqual(response.status_code, 201)

        # Approve credit by admin
        self.client.force_authenticate(user=self.admin)

        # todo request needed
        for request in CreditRequest.objects.all():
            request.status = 'approved'
            request.save()

        # seller1  credit result
        seller1_balance = sum([req.amount for req in CreditRequest.objects.filter(seller=self.seller1, status='approved')])
        self.assertEqual(seller1_balance, 10000)

        # 1000 recharge for seller1
        self.client.force_authenticate(user=self.seller1)
        for _ in range(5):
            response = self.client.post(reverse('accounting:recharge_request'), {
                'amount': 10,
                'phone': self.phone1_id
            })
            self.assertEqual(response.status_code, 201)

        # calculating final credit result
        seller1_final_balance = seller1_balance - (10 * 1000)
        seller1 = User.objects.get(id=self.seller1.id)
        self.assertEqual(seller1.credit_balance, seller1_final_balance)

        # seller2 credit validating (no transactions)
        seller2 = User.objects.get(id=self.seller2.id)
        self.assertEqual(seller2.credit_balance, 0)
