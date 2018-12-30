from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import generic
from orders.models import Order
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .task import order_created
from wkhtmltopdf.views import PDFTemplateView


class OrderPDFTemplateView(PDFTemplateView):
    def get_context_data(self, **kwargs):
        base = super(OrderPDFTemplateView, self)
        context = base.get_context_data(**kwargs)
        order = get_object_or_404(Order, id=kwargs['order_id'])
        context['order'] = order
        return context


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()
            order_created.delay(order.id)
            request.session['order_id'] = order.id
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})