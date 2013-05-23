from Acquisition import aq_inner
from Products.Five import BrowserView
from Products.CMFPlone.PloneBatch import Batch


class AzkenArgitalpenak(BrowserView):

    def azken_argitalpenak(self):
        context = aq_inner(self.context)
        lang = self.request.get('LANGUAGE', '')
        conterFilter = {'portal_type': 'DonEdukia'}
        karpetak = context.getFolderContents(conterFilter)
        argitalpenlista = []
        for i in karpetak:
            azkena = {}
            filtroa = {'portal_type': 'argitalpena',
                       'sort_on': 'effective',
                       'Language': lang,
                       'sort_order': 'reverse'}

            if i.getObject().getFolderContents(filtroa):
                azkena = {'url': i.getURL(),
                          'title': i.Title,
                          'publicacion': i.getObject().getFolderContents(filtroa)[0]}
                argitalpenlista.append(azkena)

        b_start = context.REQUEST.get('b_start', 0)
        batch = Batch(argitalpenlista, 10, int(b_start), orphan=0)
        return batch
