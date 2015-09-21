import itertools
import mimetools
import mimetypes
from cStringIO import StringIO
import urllib
import urllib2
import codecs
import os
import string

class MultiPartForm(object):
    """Accumulate the data to be used when posting a form."""

    def __init__(self):
        self.form_fields = []
        self.files = []
        self.boundary = mimetools.choose_boundary()
        return
    
    def get_content_type(self):
        return 'multipart/form-data; boundary=%s' % self.boundary

    def add_field(self, name, value):
        """Add a simple field to the form data."""
        self.form_fields.append((name, value))
        return

    def add_file(self, fieldname, filename, fileHandle, mimetype=None):
        """Add a file to be uploaded."""
        body = fileHandle.read()
        if mimetype is None:
            mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        self.files.append((fieldname, filename, mimetype, body))
        return
    
    def __str__(self):
        """Return a string representing the form data, including attached files."""
        # Build a list of lists, each containing "lines" of the
        # request.  Each part is separated by a boundary string.
        # Once the list is built, return a string where each
        # line is separated by '\r\n'.  
        parts = []
        part_boundary = '--' + self.boundary
        
        # Add the form fields
        parts.extend(
            [ part_boundary,
              'Content-Disposition: form-data; name="%s"' % name,
              '',
              value,
            ]
            for name, value in self.form_fields
            )
        
        # Add the files to upload
        #file
        parts.extend(
            [ part_boundary,
              'Content-Disposition: form-data; name="%s"; filename="%s"' % \
                 (field_name, filename),
              'Content-Type: %s' % content_type,
              '',
              body,
            ]
            for field_name, filename, content_type, body in self.files
            )
        
        # Flatten the list and add closing boundary marker,
        # then return CR+LF separated data
        flattened = list(itertools.chain(*parts))
        flattened.append('--' + self.boundary + '--')
        flattened.append('')
        return '\r\n'.join(flattened)
        ##return '\r\n'.join([x.decode('utf-8', errors='ignore') for x in flattened])

def upload(filename,name='audioFile', url='https://upload.clyp.it/upload'):
    form = MultiPartForm()
    form.add_file(name, os.path.basename(filename),fileHandle=codecs.open(filename, "rb"))
    request = urllib2.Request(url)
    ##request.add_header('User-agent', 'The Machine')
    body = str(form)
    request.add_header('Content-type', form.get_content_type())
    request.add_header('Content-length', len(body))
    ##request.add_header('Connection', 'keep-alive')
    ##request.add_header('Host', 'upload.clyp.it')
    request.add_data(body)
    return urllib2.urlopen(request).read()

##    print
##    print 'OUTGOING DATA:'
##    print request.headers
##    print request.get_data()

    
