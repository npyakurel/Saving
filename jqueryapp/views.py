

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from django.views.generic import *
from .forms import *


class ClientMixin(object):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = Item.objects.all()
        qs = Order.objects.filter(
            user=self.request.user, ordered=False)
        if qs.exists():
            context['count'] = qs[0].items.count()
        else:
            context['count'] = 0
        print(context['count'], 'rrr')
        context['object'] = Order.objects.get(
            user=self.request.user, ordered=False)

        return context


class HomeView(ClientMixin, TemplateView):
    template_name = 'home.html'


class ItemDetailView(ClientMixin, DetailView):
    model = Item
    template_name = 'itemdetail.html'
    context_object_name = 'itemdetail'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_id'] = self.kwargs['pk']
        print(context['item_id'])
        return context


class OrderSummeryView(ClientMixin, TemplateView):
    template_name = 'ordersummery.html'

    # def get(self, *args, **kwargs):
    #     try:
    #         order = Order.objects.get(user=self.request.user, ordered=False)
    #         context = {
    #             'object': order
    #         }
    #         return render(self.request, self.template_name, context)
    #     except ObjectDoesNotExist:
    #         messages.error(self.request, 'you do not have active order')
    #         return redirect('/')


def add_to_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    print(item.title)
    print(item, 'narendra')
    order_item, created = OrderItem.objects.get_or_create(
        item=item, user=request.user, ordered=False)
    print(order_item, created, 'ram thapa')
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    print(order_qs, 'order_qs')

    if order_qs.exists():
        order = order_qs[0]
        print(order, 'order')
        if order.items.filter(item__id=item.id).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, 'this item quantity was updated')
            return redirect('jqueryapp:ordersummery')
        else:

            order.items.add(order_item)
            messages.info(request, 'this item was added to your cart')
            return redirect('jqueryapp:ordersummery')
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, 'this item was added to your cart')
    return redirect('jqueryapp:ordersummery')


def remove_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__id=item.id).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False)[0]
            order.items.remove(order_item)
            messages.info(request, 'this item was removed from your cart')
            return redirect('jqueryapp:ordersummery')
        else:
            messages.info(request, 'this item was not in your cart')
            return redirect('jqueryapp:ordersummery')
    else:
        messages.info(request, 'you donot have an active order')

        return redirect('jqueryapp:ordersummery')


def remove_single_item_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__id=item.id).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()

            else:
                order.items.remove(order_item)

            messages.info(request, 'the item quantity was updated')

            return redirect('jqueryapp:ordersummery')
        else:
            messages.info(request, 'this item was not in your cart')
            return redirect('jqueryapp:product', pk=pk)
    else:
        messages.info(request, 'you donot have an active order')

        return redirect('jqueryapp:product', pk=pk)


class CheckOutView(ClientMixin, TemplateView):
    template_name = 'checkout.html'
