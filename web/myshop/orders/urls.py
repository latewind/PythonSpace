from django.conf.urls import url

from orders.models import Order
from orders.views import OrderPDFTemplateView
from . import views
from wkhtmltopdf.views import PDFTemplateView

urlpatterns = [
    url(r'^create/$',
        views.order_create,
        name='order_create'),
    url(r'^admin/order/(?P<order_id>\d+)/$',
        views.admin_order_detail,
        name='admin_order_detail'),
    url(r'^admin/order_pdf/(?P<order_id>\d+)$', OrderPDFTemplateView.as_view(template_name='orders/order/pdf.html',
                                                                       filename='order.pdf'), name='order_pdf'),
]
