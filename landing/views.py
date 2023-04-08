from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib import messages
from .forms import ReviewForm


class HomeView(TemplateView):
    template_name = 'foliox/index.html'

    def get(self, request, *args, **kwargs):
        form = ReviewForm()
        return render(request, self.template_name, context={"form": form})


    def post(self, request, *args, **kwargs):
        form = ReviewForm(data=request.POST) 
        if form.is_valid():
            form.save()
            messages.success(request, "پیام شما با موفقیت برای من ارسال شد")
            url = reverse("home") + "#contact"
            return redirect(url)
        return render(request, self.template_name, context={"form": form, "scroll_to": "contact_form"})
        