from django.shortcuts import render


def HomePageView(request):
    template_name = 'vk3/index.html'
    return render(request, template_name, {})
