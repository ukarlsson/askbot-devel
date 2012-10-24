class LanguageMiddleware(object):

    def process_request(self, request):
        if not request.session.has_key('language'):
            request.session['language'] = 'en'
