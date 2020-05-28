from django.urls import path
from .views import (
	Home,
	PemesananListView,
	PemesananCreateView,
	PemesananDetailView,
	PemesananDeleteView,
	CreateCheckOut,
	FormCheckOut,
	PemesananDetail,
	CheckDetailView,
	PemesananUpdateView,
	UserPost
	)
from django.views.decorators.http import require_POST

urlpatterns = [
	path('pemesanan/detail/<int:pk>/bayar/checkout/', CheckDetailView.as_view(), name='app-checkout-detail'),
	path('pemesanan/detail/<int:pk>/bayar/', CreateCheckOut.as_view(), name = 'app-create-checkout'),
	# path('my_form/', require_POST(FormCheckOut.as_view()), name = 'my_form_view_url'),
	path('pemesanan/detail/<int:pk>/delete/', PemesananDeleteView.as_view(), name='app-delete'),
	path('pemesanan/detail/<int:pk>', PemesananDetailView.as_view(), name='app-detail'),
	path('pemesanan/detail/<int:pk>/update', PemesananUpdateView.as_view(), name='app-update'),
	path('pemesanan', PemesananCreateView.as_view(), name='app-create'),
	# path('home',PemesananListView.as_view(), name='app-list' ),
	path('home', UserPost, name = 'app-list'),
	path('', Home.as_view(), name = 'app-home'),
]
