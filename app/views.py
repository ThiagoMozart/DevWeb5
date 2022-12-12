from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify

from core.forms import SearchProductForm, ProductForm
from core.models import History, Chapter, News, Image, Product


def index(request):
    image = Image.objects.get(name="Krieg War")
    news = News.objects.all()
    context = {
        "phrase": "News",
        "news": news,
        "krieg": image,
    }

    return render(request, 'app/pages/index.html', context=context)


def shop(request):
    form = SearchProductForm(request.GET)

    if form.is_valid():
        name = form.cleaned_data['name']
        products = Product.objects.filter(name__icontains=name).order_by("name")

        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        page_obj = paginator.get_page(page)

        context = {
            "phrase": "product",
            "products": page_obj,
            "form": form,
            "name": name,
        }

        return render(request, 'app/pages/shop.html', context=context)
    else:
        raise ValueError('Unexpected error when trying to get a product')


def selling(request):
    if request.POST:
        product_id = request.session.get('product_id')

        if product_id:
            product = get_object_or_404(Product, pk=product_id)
            product_form = ProductForm(request.POST, request.FILES, instance=product)

        else:
            product_form = ProductForm(request.POST, request.FILES)

        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.slug = slugify(product.name)
            product.save()

            if product_id:
                messages.add_message(request, messages.INFO, 'Item edited with sucess!')
                del request.session['product_id']

            else:
                messages.add_message(request, messages.INFO, 'Item registered for Selling')

            return redirect('app:show_product', id=product.id)

    else:
        try:
            del request.session['product_id']
        except KeyError:
            pass

        product_form = ProductForm()

    context = {
        "phrase": "Selling",
        "form": product_form
    }

    return render(request, 'app/pages/selling.html', context=context)


def show_product(request, id):
    product = get_object_or_404(Product, pk=id)
    request.session['product_id_del'] = id

    context = {
        "phrase": "Show Product",
        "product": product,
    }

    return render(request, 'app/pages/show_product.html', context=context)


def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product_form = ProductForm(instance=product)
    request.session["product_id"] = id

    context = {
        "phrase": "Edit Product",
        "form": product_form
    }

    return render(request, 'app/pages/selling.html', context=context)


def remove_product(request):
    product_id = request.session.get('product_id_del')
    product = get_object_or_404(Product, id=product_id)
    product.image.delete()
    product.delete()

    del request.session['product_id_del']
    messages.add_message(request, messages.INFO, 'Product Removed!')

    context = {
        "phrase": "remove product",
        "product": product
    }

    return render(request, 'app/pages/show_product.html', context=context)


def history(request):
    histories = History.objects.select_related("image")
    context = {
        "phrase": "History",
        "histories": histories,
    }

    return render(request, 'app/pages/history.html', context=context)


def chapter(request):
    chapters = Chapter.objects.select_related("image")
    context = {
        "phrase": "Chapter",
        "chapters": chapters
    }

    return render(request, 'app/pages/chapter.html', context=context)


def login(request):
    image = Image.objects.get(name="Login Image")
    context = {
        "phrase": "Login",
        "LoginImage": image
    }

    return render(request, 'app/pages/login.html', context=context)


def register(request):
    image = Image.objects.get(name="Register Image")
    context = {
        "phrase": "Resgiter",
        "RegisterImage": image
    }

    return render(request, 'app/pages/register.html', context=context)


