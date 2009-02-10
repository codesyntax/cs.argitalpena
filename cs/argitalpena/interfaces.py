from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from cs.argitalpena import argitalpenaMessageFactory as _

# -*- extra stuff goes here -*-
class Iargitalpena(Interface):
    """Description of the Example Type"""
    


    title = schema.TextLine(title=_(u'Name'),
                            required=True,
                            )
			    
    description = schema.TextLine(title=_(u'Description'),
                                  description=_(u'A short summary of this product'),
                                  )
				  
    file = schema.TextLine(title=_(u'File'),
                                  description=_(u'File'),
                                  )

    image = schema.TextLine(title=_(u'Image'),
                                  description=_(u'Image'),
                                  )
				  
