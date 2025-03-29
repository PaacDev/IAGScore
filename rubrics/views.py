"""
This module contains the views for the rubrics app.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .forms import RubricForm

@login_required
@require_http_methods(["GET", "POST"])
@csrf_protect
def rubric_page(request):
    """
    View for import a new rubric.
    """
    if request.method == 'POST':
        form = RubricForm(request.POST, request.FILES)
        if form.is_valid():
            print('valid form')
            rubric_file = request.FILE['rubric_file']
            print('NO valid form')
            if not rubric_file.name.endswith('.md'):
                print('NO MD')
                messages.error(request, 'El archivo subido no es Markdown')
                return redirect('rubrics_page')
    
    else:
        print('GET')
        form = RubricForm()

    return render(request, 'rubrics/rubrics_page.html')