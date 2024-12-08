import uuid
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def generate_telegram_link_code(request):
    profile = request.user.profile
    profile.link_code = str(uuid.uuid4())
    profile.save()
    # Показываем пользователю link_code, который ему нужно отправить боту
    return render(request, 'users/link_code.html', {'link_code': profile.link_code})
