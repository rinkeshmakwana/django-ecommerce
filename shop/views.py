from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View

from .forms import CheckoutForm, PaymentForm
from .models import Product, OrderProduct, Order, Address, Category


class HomeListView(ListView):
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'products'
    ordering = ['-list_date']


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    # queryset = Product.objects.filter(category__name='Electronics')  # newly added
    ordering = ['-list_date']
    paginate_by = 20

    # newly added
    def get_queryset(self):
        self.category = get_object_or_404(Category, name=self.kwargs['category'])
        return Product.objects.filter(category=self.category)


class ProductDetailView(DetailView):
    model = Product
    template_name = "shop/product_detail.html"


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = "shop/product_form.html"
    fields = ['product_name', 'product_description', 'product_price', 'product_image', 'product_rating']

    def form_valid(self, form):
        form.instance.product_seller = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = ['product_name', 'product_description', 'product_price', 'product_rating']

    def form_valid(self, form):
        form.instance.product_seller = self.request.user
        return super().form_valid(form)

    def test_func(self):
        product = self.get_object()
        if self.request.user == product.product_seller:
            return True
        return False


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = '/'

    def test_func(self):
        product = self.get_object()
        if self.request.user == product.product_seller:
            return True
        return False


def about(request):
    return render(request, 'shop/about.html')


@login_required
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_product, created = OrderProduct.objects.get_or_create(product=product, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order product is in the order
        if order.products.filter(product__slug=product.slug).exists():
            order_product.quantity += 1
            order_product.save()
            messages.info(request, "This item quantity has been updated.")
            return redirect('product-detail', slug=slug)
        else:
            order.products.add(order_product)
            messages.info(request, "This item was added to your cart.")
            return redirect('product-detail', slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.products.add(order_product)
        messages.info(request, 'Item added to your cart')

    return redirect('product-detail', slug=slug)


@login_required
def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_product = OrderProduct.objects.filter(product=product, user=request.user, ordered=False)[0]
            order.products.remove(order_product)
            messages.info(request, "Item removed from your cart")
            return redirect("shopping_cart")
        else:
            messages.info(request, "Item was not in your cart")
            return redirect("product-detail", slug=slug)
    else:
        messages.info(request, "you dont have an active order")
        return redirect("product-detail", slug=slug)


@login_required
def remove_single_product_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_product = OrderProduct.objects.filter(product=product, user=request.user, ordered=False)[0]
            if order_product.quantity > 1:
                order_product.quantity -= 1
                order_product.save()
            else:
                order.products.remove(order_product)
            messages.info(request, "Item quantity updated.")
            return redirect("product-detail", slug=slug)
        else:
            messages.info(request, "Item was not in your cart")
            return redirect("product-detail", slug=slug)
    else:
        messages.info(request, "you dont have an active order")
        return redirect("product-detail", slug=slug)


@login_required
def buy_now(request, slug):
    add_to_cart(request, slug)
    return redirect('shopping_cart')


class ShoppingCartView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'shop/shopping_cart.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You dont have an active order")
            return redirect("/")


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


class CheckoutView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'object': order
            }

            address_qs = Address.objects.filter(user=self.request.user, default=True)
            if address_qs.exists():
                context.update({'default_address': address_qs[0]})

            return render(self.request, 'shop/checkout.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You dont have an active order")
            return redirect("/")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        print(self.request.POST)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                use_default_address = form.cleaned_data.get('use_default_address')
                if use_default_address:
                    print("Using default address")
                    address_qs = Address.objects.filter(user=self.request.user, default=True)
                    if address_qs.exists():
                        address = address_qs[0]
                        order.address = address
                        order.save()
                    else:
                        messages.info(self.request, "No default address available")
                        return redirect('checkout')
                else:
                    print("user is entering new address")
                    address = form.cleaned_data.get('address')
                    city = form.cleaned_data.get('city')
                    state = form.cleaned_data.get('state')
                    country = form.cleaned_data.get('country')
                    zip = form.cleaned_data.get('zip')

                    if is_valid_form([address, city, state, country, zip]):
                        address = Address(
                            user=self.request.user,
                            address=address,
                            city=city,
                            state=state,
                            country=country,
                            zip=zip
                        )
                        address.default = True
                        address.save()
                        order.address = address
                        order.save()
                    else:
                        messages.info(self.request, "Please fill in required fields.")

                payment_option = form.cleaned_data.get('payment_option')
                if payment_option == 'C':
                    return redirect('payment', payment_option='card')
                elif payment_option == 'P':
                    return redirect('payment', payment_option='paypal')
                else:
                    messages.warning(self.request, "Invalid payment option selected")
                    return redirect('checkout')

        except ObjectDoesNotExist:
            messages.warning(self.request, "You dont have an active order.")
            return redirect('shopping_cart')


class PaymentView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.address:
            context = {
                'order': order
            }
            return render(self.request, 'shop/payment.html', context)
        else:
            messages.warning(self.request, "you havent added address yet.")
            return redirect("checkout")

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        form = PaymentForm(self.request.POST)

        return redirect('/')
