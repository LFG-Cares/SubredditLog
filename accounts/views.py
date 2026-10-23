from logging import getLogger

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods


logger = getLogger(__name__)

@never_cache
@login_required
@require_http_methods(['GET', 'POST'])
def api_token(request):
    """
    GET shows the current token state.
    POST issues (or reissues) a token and reveals it once.
    """
    if request.method == 'POST':
        raw_token = request.user.issue_token()
        logger.info(f'Token generated for {request.user.username}')
        return render(request, 'account/_api_token_created.html', {'token': raw_token})

    return render(request, 'account/_api_token.html')
