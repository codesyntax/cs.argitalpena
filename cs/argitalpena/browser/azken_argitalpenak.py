
__version__ = '$Id$'


from Products.Five import BrowserView

from Acquisition import aq_inner
class Azkenak(BrowserView):

	def __call__(self):
		context=aq_inner(self.context)
		lang=self.request.LANGUAGE
		#import pdb;pdb.set_trace()
                
		conterFilter={'portal_type':'DonEdukia'}
		karpetak=context.getFolderContents(conterFilter)
		argitalpenlista=[]
		for i in karpetak:
			azkena={}
                        filtroa={'portal_type':'argitalpena','sort_on':'effective', 'Language':lang, 'sort_order':'reverse'}
                        if i.getObject().getFolderContents(filtroa):
                            azkena={'url':i.getURL(), 'title':i.Title, 'publicacion':i.getObject().getFolderContents(filtroa)[0]}
                            argitalpenlista.append(azkena)
		from Products.CMFPlone import Batch
    		b_start = context.REQUEST.get('b_start', 0)
    		batch = Batch(argitalpenlista, 10, int(b_start), orphan=0)
    		return batch
