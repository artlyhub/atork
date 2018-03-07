from django.conf.urls import url

from crowdfund.api.views import FundItemAPIView, FunderAPIView

urlpatterns = [
    # url(r'^item/$', FundItemAPIView.as_view(), name="item"),
    # url(r'^item-image/(?P<pk>\d+)/$',
    #     ImageDetailsAPIView.as_view(), name="item-image-details"),
    # url(r'^item/$', ItemAPIView.as_view(), name="item"),
    # url(r'^item/(?P<pk>\d+)/$',
    #     ItemDetailsAPIView.as_view(), name="item-details"),
]
