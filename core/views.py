from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import (
    ListView,
    View,
    )

from .models import (
    Category, 
    Vendor, 
    Product,
    Productimages,
    CartOrder, 
    CartOrderItems, 
    ProductReview,
    Wishlist,
    Address,
    Blog,
    Contact,
    )

import json


class HomeView(ListView):
    model = None
    template_name = 'home/index.html'

    def get_queryset(self):
        return None

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['feat_list'] = Product.objects.filter(product_status="published", featured=True)
        context['new_list'] = Product.objects.filter(product_status="published", new=True)

        return context

class ShopView(ListView):
    model = Product
    template_name = 'shop/index.html'
    paginate_by = 12

def s_product(request, pk):
    product = Product.objects.get(pk=pk)
    img_product = Productimages.objects.filter(product=pk)
    feat_list = Product.objects.filter(product_status="published", featured=True)

    context = {
        'product':product,
        'img_product':img_product,
        'feat_list':feat_list,
    }
    
    return render(request, 'sproduct/index.html', context)

class BlogView(ListView):
    model = Blog
    template_name = 'blog/index.html'
    paginate_by = 6

def s_blog(request, pk):

    post = Blog.objects.get(pk=pk)

    context = {
        "post":post
    }

    return render(request, "s_blog/index.html", context)

def about(request):
    return render( request, 'about/index.html')

def contact_view(request):
    if request.method =="GET":
        return render( request, 'contact/index.html')
    else:
        name = request.POST.get("name")
        email = request.POST.get("email")
        assunto = request.POST.get("assunto")
        texto = request.POST.get("texto")

        base = Contact.objects.create(name=name, email=email, assunto=assunto, texto=texto)
        base.save()

        return redirect("core:home")

class CartView(View):
    def get(self, request):

        prod_cart = []
        all_freight = []

        if 'cart' in request.session and request.session['cart']:
            for i in request.session['cart']:
                prod = Product.objects.get(pk=i)
                prod_cart.append(prod)

                freight_value = prod.freight
                all_freight.append(freight_value)

            freight = sum(all_freight)

            context = {
                "prod_cart":prod_cart,
                "freight":freight,
            }
        else:
            context = {
                "prod_cart":[],
                "freight":0
            }  

        return render(request, 'cart/index.html', context)

    def post(self, request):
        data = json.loads(request.body)
        pk = data.get('pk')
        pk = str(pk)

        if 'cart' not in request.session:
            request.session['cart'] = []
        
        request.session['cart'].append(pk)
        request.session.modified = True

        # URL de referência de onde o usuário veio
        referer = request.META.get('HTTP_REFERER')
        
        if referer:
            return redirect(referer)

        return redirect('core:home')

    def delete(self, request):
        list_prod = []
    
        for i in request.session['cart']:
            list_prod.append(i)

        data = json.loads(request.body)
        pk = data.get('pk')
        pk = str(pk)

        list_prod.remove(pk)

        request.session['cart'] = list_prod
        request.session.modified = True

        return redirect('core:cart')







