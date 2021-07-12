import json
from .models import *


def cartData(request):
    if request.user.is_authenticated:
        profile = request.user.profile
        order, created = Order.objects.get_or_create(
            profile=profile, complete=False)
        items = order.orderitem_set.all()

    return {'order': order, 'items': items}
