import os,shutil
import constants
from page import Page
from page import Post

class Converter:
    """
    A class that handles walking the filesystem and either converting to HTML
    or copying non-convertible files to the output directory.
    """

    def __init__(self, config):
        """
        Initializes instance with configuration details
        """
        self.layoutdir = config['layouts']
        self.default = config['default_layout']
        self.outdir = os.path.abspath(os.path.expanduser(config['output']))
        self.blogdir = config['blog']
        self.source = os.path.abspath(os.path.expanduser(config['source']))
        self.ignores = config['ignores']
        
        try:
            tsfile = open(config['timestamp'])
            self.timestamp = pickle.load(tsfile)
            tsfile.close()
        except:
            self.timestamp = 0

    def process(self):
        """
        Walks through the filesystem and converts all appropriate files to HTML
        """
        for root, dirs, files in os.walk(self.source):
            if not self.visitable(root):
                continue
            self.current_outdir = root.replace(self.source,self.outdir)
            try:
                os.mkdir(self.current_outdir)
            except:
                    pass

            for filename in files:
                filepath = os.path.join(root,filename)
                modify_time = os.path.getmtime(filepath)

                if modify_time  > self.timestamp:
                    if root.endswith(self.blogdir) and self.convertable(filename):
                        blogdir = self.current_outdir.strip(self.blogdir)
                        self.make_post(blogdir, filepath)
                    elif self.convertable(filename):
                        self.make_page(filepath)
                    elif self.copyable(filename):
                        outpath = os.path.join(self.current_outdir,filename)
                        shutil.copy(filepath, outpath)

    def visitable(self, directory):
        """Checks if the given directory should be visited """
        for each in self.ignores:
            if directory.endswith(each):
                return False
        if '/.' in directory:
            return False
        else:
            return True
        
    def convertable(self, filename):
        """ Checks if the given filename can be converted to HTML"""
        return filename.endswith(constants.formats) and self.copyable(filename)

    def copyable(self, filename):
        """Checks if the given filename is hidden, a backup or a cyblog ignore """
        return filename[-1] != '~' and filename[0] != '.' and filename[0] != '_'

    def make_post(self, root, filepath):
        """Creates the HTML version of a blog post and then writes it to disk """
        post = Post(filepath, self.layoutdir)
        html = post.generate()
        postpath = os.path.join(root, post.prefix)
        try:
            os.makedirs(postpath)
        except:
            pass
        htmlfile = os.path.join(postpath, post.htmlname)
        self.write_out(html, htmlfile)

    def make_page(self, filepath):
        """Creates the HTML version of a Page and writes it to disk """
        page = Page(filepath, self.layoutdir)
        html = page.generate()
        htmlpath = os.path.join(self.outdir,page.htmlname)
        self.write_out(html, htmlpath)

    def write_out(self, html, htmlpath):
        """Given a chunk of HTML and a filepath, writes the HTML to the file """
        htmlfile = open(htmlpath, 'w')
        htmlfile.write(html)
        htmlfile.close()
