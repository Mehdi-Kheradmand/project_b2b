import logging
from django.db import transaction
from django.db.models import F
from django.utils import timezone
from celery import shared_task
from accounting.models import RechargeRequest, Transaction, CreditRequest
from phones.models import Phone
from django.contrib.auth import get_user_model
User = get_user_model()

logger = logging.getLogger(__name__)


@shared_task(queue="default", autoretry_for=(Exception,), retry_backoff=True, max_retries=5)
def recharge_task(recharge_request_id: int):
    logger.info('Starting recharge task')

    # check seller credit balance
    try:
        recharge_request = RechargeRequest.objects.select_related('seller', 'phone').get(id=recharge_request_id)
        seller = recharge_request.seller
        requested_phone = Phone.objects.get(id=recharge_request.phone_id)

        if seller.credit_balance >= recharge_request.amount:
            with transaction.atomic():
                # increase phone charge_balance
                requested_phone.charge_balance += recharge_request.amount
                requested_phone.save()

                # create transaction record
                Transaction.objects.create(
                    seller=recharge_request.seller,
                    amount=recharge_request.amount,
                    phone=requested_phone,
                    transaction_type='decrease',
                    description='Phone recharge process'
                )

                # change recharge_request status
                recharge_request.status = 'processed'
                recharge_request.processed_at = timezone.now()
                recharge_request.save()

                # decrease seller credit
                User.objects.filter(id=seller.id).update(credit_balance=F('credit_balance') - recharge_request.amount)

                logger.info('recharge task completed')
        else:
            # Insufficient credit
            recharge_request.status = 'failed'
            recharge_request.description = "Insufficient credit"
            recharge_request.processed_at = timezone.now()
            recharge_request.save()
            logger.warning(f"Insufficient credit for RechargeRequest ID: {recharge_request_id}")

    except Exception as e:
        # Log the error
        logger.error(f"Error processing recharge request {recharge_request_id}: {str(e)}")
        raise e  # celery will retry the task


@shared_task(queue="high_priority", autoretry_for=(Exception,), retry_backoff=True, max_retries=5)
def credit_approve_task(admin_id: int, credit_request_id: int):
    logger.info('Starting credit_approve task')

    try:  # Process the credit request (approve)
        credit_request = CreditRequest.objects.select_related('seller').get(id=credit_request_id, status='pending')
        seller = credit_request.seller

        with transaction.atomic():
            # create a transaction record
            Transaction.objects.create(
                seller=seller,
                amount=credit_request.amount,
                transaction_type='increase',
                description='Credit request approved'
            )

            # Update the credit request
            credit_request.status = "approved"
            credit_request.processed_at = timezone.now()
            credit_request.processed_by_id = admin_id
            credit_request.save()

            # update seller credit
            User.objects.filter(id=seller.id).update(credit_balance=F('credit_balance') + credit_request.amount)

    except Exception as e:
        logging.error(f"Error processing credit request {credit_request_id}: {str(e)}")  # Log the error
        raise e  # celery will retry the task


@shared_task
def test_task():
    logger.error("is working")
    logger.error("is working")
    logger.error("is working")
    logger.error("done")
    print("it is working")
