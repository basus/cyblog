import os
from jinja2 import Template
from markdown import markdown

class Page:
    """
    Represents an HTML page, built from a layout and a dictionary containing
    fills for the the hooks in the layout
    """

    def __init__(self, layout, docinfo):
        self.layout = layout
        self.docinfo = docinfo
        self.process_inserts()


    def generate(self):
        """
        Fills in the layout with appropriate data for the hooks
        """
        template = Template(self.layout.read())
        return template.render(self.inserts)

    def process_inserts(self):
        """
        Use the docinfo to generate a dictionary mapping hooks to their
        replacement values
        """
        self.inserts = self.docinfo

        self.inserts['page'] = {}
        for key, value in self.docinfo.iteritems():
            self.inserts['page'][key] = value

        self.inserts['content'] = markdown(self.inserts['content'])

    def fileout(self):
        filecore = os.path.splitext(self.docinfo['filename'])[0]
        try:
            date = self.inserts['date'].replace('-','/')
        except:
            date = ''
        return date + filecore + '.html'
