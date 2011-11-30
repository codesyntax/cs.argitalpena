from zope.interface import implements, directlyProvides
from AccessControl import ClassSecurityInfo
try:
    from Products.LinguaPlone import public as atapi
except ImportError:
    from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from plone.app.blob.field import ImageField,FileField
from cs.argitalpena import argitalpenaMessageFactory as _
from cs.argitalpena.interfaces import Iargitalpena
from cs.argitalpena.config import PROJECTNAME

argitalpenaSchema = folder.ATFolderSchema.copy() + atapi.Schema((
    ImageField('image',
                         required=False,
                         languageIndependent=True,
			 storage = atapi.AnnotationStorage(),
                         sizes= {'large'   : (768, 768),
                                 'preview' : (400, 400),
                                 'mini'    : (200, 200),
                                 'thumb'   : (128, 128),
                                 'tile'    :  (64, 64),
                                 'icon'    :  (32, 32),
                                 'listing' :  (16, 16),
                                 },
                         widget=atapi.ImageWidget(label=_(u'Image', default=u'The image of this argitalpena'),
                                                  show_content_type=False,
                                                  ),
                         ),

	FileField('file',
                  searchable=0,
		  languageIndependent=True,
                  storage = atapi.AnnotationStorage(),
                  widget=atapi.FileWidget(
                     label=_(u'file'),
                     description_msgid=_(u'description_file'),
                     ),
                  ),

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

argitalpenaSchema['title'].storage = atapi.AnnotationStorage()
argitalpenaSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(argitalpenaSchema, folderish=True, moveDiscussion=False)

class argitalpena(folder.ATFolder):
    """Description of the Example Type"""
    implements(Iargitalpena)

    portal_type = "argitalpena"
    schema = argitalpenaSchema
    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    file=atapi.ATFieldProperty('file')
    image=atapi.ATFieldProperty('image')
    security = ClassSecurityInfo()
    security.declarePrivate('cmf_edit')
    def tag(self, **kwargs):
        
        if 'title' not in kwargs:
            kwargs['title'] = self.title
        return self.getField('image').tag(self, **kwargs)
    
    def __bobo_traverse__(self, REQUEST, name):
        
        if name.startswith('image'):
            field = self.getField('image')
            image = None
            if name == 'image':
                image = field.getScale(self)
            else:
                scalename = name[len('image_'):]
                if scalename in field.getAvailableSizes(self):
                    image = field.getScale(self, scale=scalename)
            if image is not None and not isinstance(image, basestring):
                # image might be None or '' for empty images
                return image

        return folder.ATFolder.__bobo_traverse__(self, REQUEST, name)

atapi.registerType(argitalpena, PROJECTNAME)
