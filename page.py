import os, yaml
from jinja2 import Template
from markdown import markdown

class Page:
    """
    Represents an HTML page, built from a layout and a dictionary containing
    fills for the the hooks in the layout
    """

    def __init__(self, filename, layoutdir, def_layout='default'):
        self.data = open(filename).read()
        self.filename = filename
        self.layoutdir = layoutdir
        self.default_layout = def_layout
        self.extract_yaml()
        self.template = Template(self.layout.read())
        self.output_path = os.path.splitext(filename)[0] + '.html'
        print self.output_path
        
    def extract_yaml(self):
        """
        Separates the YAML and the content
        """
        splitdata = self.data.split('---\n')
        meta = splitdata[1]
        self.content = '---\n'.join(splitdata[2:])

        self.info = yaml.load(meta)
        self.info['filename'] = self.filename
        self.info['page'] = {}

        for key, value in self.info.iteritems():
            self.info['page'][key] = value

        try:
            layout_file = self.info['layout']
        except:
            layout_file = self.default_layout
        self.layout = open(self.layoutdir + '/' + layout_file + '.html')


    def generate(self):
        """
        Fills in the layout with appropriate data for the hooks
        """
        return self.template.render(self.info)


class Post:

    def __init__(self, filepath,layoutdir):
        filename = filepath.split('/')[-1]
        expandedname = filename.split('-',3)
        self.date = expandedname[:3]
        self.title = '-'.join(expandedname[3:]).split('.')[0]
        self.page = Page(filepath, layoutdir)
        self.make_output_path()

    def generate(self):
        return self.page.generate()

    def make_output_path(self):
        self.prefix = '/'.join(self.date)
        self.output_path = './' + self.prefix + '/' + self.title + '.html'
