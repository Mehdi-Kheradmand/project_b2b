from django.urls import path
from .views import PhoneView


urlpatterns = [
    path('', PhoneView.as_view(), name='Phones'),
    # path('<str:phone_id>', PhoneView.as_view(), name='PhonesById'),
]
