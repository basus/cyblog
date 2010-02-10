import os, yaml
from jinja2 import Template
from markdown import markdown

class Page:
    """
    Represents an HTML page, built from a layout and a dictionary containing
    fills for the the hooks in the layout
    """

    def __init__(self, filepath, layoutdir, def_layout='default'):
        """
        Initializes the Page object with given parameters and does setup of the
        template and HTML name of the page
        """
        self.data = open(filepath).read()
        self.filepath = filepath
        self.layoutdir = layoutdir
        self.default_layout = def_layout
        self.extract_yaml()
        self.template = Template(self.layout.read())
        self.make_htmlname()

    def make_htmlname(self):
        """ Creates the HTML name for the page"""
        filename = os.path.split(self.filepath)[1]
        self.htmlname = os.path.splitext(filename)[0] + '.html'
        
    def extract_yaml(self):
        """
        Separates the YAML and the content
        """
        splitdata = self.data.split('---\n')
        meta = splitdata[1]
        self.content = '---\n'.join(splitdata[2:])

        self.info = yaml.load(meta)
        self.info['page'] = {}
        self.info['content'] = markdown(self.content)

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
    """
    Represents a blog post. Wrapper around a Page but with extraction of post
    parameters such as permalink structure.
    """

    def __init__(self, filepath,layoutdir):
        """Creates the Page object to be wrapped and sets up the permalink """
        self.filename = filepath.split('/')[-1]
        self.make_permalink
        self.page = Page(filepath, layoutdir)
        self.has_categories = self.page.info.has_key('categories')

    def make_permalink(self, structure):
        """Creates the permalink for the post """
        expansion = self.filename.split('-', 3)
        permalink = {}
        permalink['year'] = expansion[0]
        permalink['month'] = expansion[1]
        permalink['day'] = expansion[2]
        permalink['title'] = expansion[3].split('.')[0]

        if structure = 'pretty':
            structure = ':year/:month/:day/:title'
            
        self.prefix = structure.lstrip('/')
        self.prefix = self.prefix.replace(':year', permalink['year'])
        self.prefix = self.prefix.replace(':day', permalink['day'])
        self.prefix = self.prefix.replace(':month', permalink['month'])
        self.prefix = self.prefix.replace(':title', permalink['title'])
        
        if structure.endswith('.html'):
            (self.prefix, self.htmlname) = os.path.split(self.prefix)
        else:
            self.htmlname = 'index.html'

        # if self.has_categories:
        #     prefixes = []
        #     htmlnames = []
        #     for category in self.page.info['categories']:
        #         prefix = self.prefix.replace(':categories', category)
        #         prefixes.append(prefix)

        # expandedname = self.filename.split('-',3)
        # self.date = expandedname[:3]
        # self.prefix = '/'.join(self.date)
        # self.title = expandedname[3].split('.')[0]
        # self.htmlname = self.title + '.html'
        

    def generate(self):
        """Wrapper around the Page's HTML generation function """
        return self.page.generate()

