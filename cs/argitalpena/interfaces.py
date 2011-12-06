from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from cs.argitalpena import argitalpenaMessageFactory as _

# -*- extra stuff goes here -*-
class Iargitalpena(Interface):
    """A publication object that can save multiple files and an image"""
    


    title = schema.TextLine(title=_(u'Name'),
                            required=True,
                            )
			    
    description = schema.TextLine(title=_(u'Description'),
                                  description=_(u'Enter the description of this publication'),
                                  )
				  
    file = schema.TextLine(title=_(u'File'),
                           description=_(u'File description'),
                                  )

    image = schema.TextLine(title=_(u'Image', default=u'The image of this publication'),
                            description=_(u'Image description'),
                                  )
				  
