class PlataformaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'plataforma' in request.GET:
            request.session['plataforma'] = request.GET['plataforma']
        return self.get_response(request)
