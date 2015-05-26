from zope.interface import implements
from AccessControl import ClassSecurityInfo
try:
    from Products.LinguaPlone import public as atapi
except ImportError:
    from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.interface.file import IFileContent
from plone.app.blob.field import ImageField, FileField
from cs.argitalpena import argitalpenaMessageFactory as _
from cs.argitalpena.interfaces import Iargitalpena
from cs.argitalpena.config import PROJECTNAME
from ZODB.POSException import ConflictError
from Products.CMFPlone.utils import getToolByName

argitalpenaSchema = folder.ATFolderSchema.copy() + atapi.Schema((
    ImageField('image',
                required=False,
                languageIndependent=True,
                storage=atapi.AnnotationStorage(),
                sizes={'large'    : (768, 768),
                        'preview' : (400, 400),
                        'mini'    : (200, 200),
                        'thumb'   : (128, 128),
                        'tile'    :  (64, 64),
                        'icon'    :  (32, 32),
                        'listing' :  (16, 16),
                },
                widget=atapi.ImageWidget(label=_(u'Image',
                                                default=u'The image of this publication'),
                                         show_content_type=False,
                      ),
    ),

    FileField('file',
                searchable=1,
                languageIndependent=True,
                index_method = 'getIndexValue',
                primary=True,
                storage=atapi.AnnotationStorage(),
                widget=atapi.FileWidget(
                        label=_(u'File'),
                        description_msgid=_(u'File description'),
                ),
    ),


))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.
argitalpenaSchema['title'].storage = atapi.AnnotationStorage()
argitalpenaSchema['description'].storage = atapi.AnnotationStorage()
schemata.finalizeATCTSchema(argitalpenaSchema,
                            folderish=True,
                            moveDiscussion=False)


class argitalpena(folder.ATFolder):
    """A publication object that can save multiple files and an image"""
    implements(Iargitalpena, IFileContent)

    portal_type = "argitalpena"
    schema = argitalpenaSchema
    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    file = atapi.ATFieldProperty('file')
    image = atapi.ATFieldProperty('image')

    # XXX Why is this needed [erral]
    security = ClassSecurityInfo()
    security.declarePrivate('cmf_edit')

    def tag(self, **kwargs):
        """ to generate image tag """
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

    security.declarePrivate('getIndexValue')
    def getIndexValue(self, mimetype='text/plain'):
        """ an accessor method used for indexing the field's value
            XXX: the implementation is mostly based on archetype's
            `FileField.getIndexable` and rather naive as all data gets
            loaded into memory if a suitable transform was found.
            this should probably use `plone.transforms` in the future """

        field = self.getPrimaryField()
        source = field.getContentType(self)
        transforms = getToolByName(self, 'portal_transforms')
        if transforms._findPath(source, mimetype) is None:
            return ''
        value = str(field.get(self))
        filename = field.getFilename(self)
        try:
            return str(transforms.convertTo(mimetype, value,
                mimetype=source, filename=filename))
        except (ConflictError, KeyboardInterrupt):
            raise
        except:
            getLogger(__name__).exception('exception while trying to convert '
               'blob contents to "text/plain" for %r', self)


atapi.registerType(argitalpena, PROJECTNAME)
