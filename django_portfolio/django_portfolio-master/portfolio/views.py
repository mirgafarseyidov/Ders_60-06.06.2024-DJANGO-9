from django.shortcuts import render, redirect
from .models import Portfolio
from .forms import PortfolioForm
from .models import Contact
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import pdfkit
from django.conf import settings
from django.utils import translation
from django.urls.base import resolve, reverse
from django.urls.exceptions import Resolver404
from urllib.parse import urlparse



def portfolio_create(request):
    if request.method == 'POST':
        form = PortfolioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('portfolio_create')  
    else:
        form = PortfolioForm()
    return render(request, 'portfolio_form.html', {'form': form})


def contactPage(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        contact = Contact(
            name=name,
            email=email,
            message=message,
        )

        contact.save()

        html_message = render_to_string(
            "email.html",
            {
                "name": name,
            },
        )

        email_message = EmailMessage(
            subject="Yeni Müraciət",
            body=html_message,
            from_email="",
            to=[email],
        )

        email_message.content_subtype = "html"

        email_message.send()

        messages.success(request, "Ugutla gonderildi...")

    return render(request, "contact.html")

def resume(request, id):
    user_profile = Portfolio.objects.get(id=id)
    template = loader.get_template("resume.html")
    html = template.render({"user_profile": user_profile})
    options = {
        "page-size": "Letter",
        "encoding": "UTF-8",
    }
    pdf = pdfkit.from_string(html, False, options)
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="download.pdf"'
    return response


def resumeList(request):
    profiles = Portfolio.objects.all()
    context = {"profiles": profiles}
    return render(request, "list.html", context)



def set_language(request, language):
    for lang, _ in settings.LANGUAGES:
        translation.activate(lang)
        try:
            view = resolve(urlparse(request.META.get("HTTP_REFERER")).path)
        except Resolver404:
            view = None
        if view:
            break
    if view:
        translation.activate(language)
        next_url = reverse(view.url_name, args=view.args, kwargs=view.kwargs)
        response = HttpResponseRedirect(next_url)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    else:
        response = HttpResponseRedirect("/")
    return response