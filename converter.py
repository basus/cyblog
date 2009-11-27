import os,yaml,shutil
import constants
from page import Page

class Converter:

    def __init__(self, config):
        """
        Initializes instance with configuration details
        """
        self.output = config.output
        self.layoutdir = config.layoutdir
        self.default = config.default_layout
        self.outdir = os.getcwd() + '/' + self.output
        self.blogdir = config.blog
        
        try:
            tsfile = open(config.timestamp)
            self.timestamp = pickle.load(tsfile)
            tsfile.close()
        except:
            self.timestamp = 0

    def process(self):
        """
        Walks through the filesystem and converts all appropriate files to HTML
        """
        for root, dir, files in os.walk('.'):
            if root.find('/.') == -1 and root.find('./'+self.output) == -1 and root[0] != '_':
                self.current_outdir = self.outdir + root[1:] + '/'
                
                for filename in files:
                    filepath = root +'/'+filename
                    modify_time = os.path.getmtime(filepath)

                    if modify_time  > self.timestamp and self.convertable(filename):
                        if root[2:] == self.blogdir:
                            make_post(filepath)
                        else:
                            try:
                                os.mkdir(self.current_outdir)
                            except:
                                pass
                            self.make_page(filepath)
                            shutil.copy(filepath, self.current_outdir+filename)

    def convertable(self, filename):
        """
        Checks if the given filename can be converted to HTML
        """
        return filename[-1] != '~' and filename[0] != '.' and filename[0] != '_' and filename.endswith(constants.formats)

    def make_post(self, filename):
        pass

    def make_page(self, filename):
        page = Page(open(filename).read(), filename, self.layoutdir)
        html = page.generate()
        htmlpath = self.outdir + page.output_file

        htmlfile = open(htmlpath, 'w')
        htmlfile.write(html)
        htmlfile.close()
        

    def process_files(self, root, files):
        for filename in files:
            filepath = root +'/'+filename
            modify_time = os.path.getmtime(filepath)

            if modify_time  > self.timestamp and filename[-1] != '~' and filename[0] != '.':
                if filename.endswith(constants.formats):

                    html, html_file = self.htmlgen(filepath)
                    html_filepath = self.outdir + '/' + html_file

                    html_file = open(html_filepath, 'w')
                    html_file.write(html)

                    html_file.close()
                elif filename[1] != '_':
                    shutil.copy(filepath, self.current_outdir+filename)

    def htmlgen(self, indoc):
        """
        Creates the HTML version of the markdown/yaml input
        """
        doc =  open(indoc).read().split('---\n')
        
        meta = doc[1]
        content = '---\n'.join(doc[2:])
        
        docinfo = yaml.load(meta)
        docinfo['filename'] = indoc
        docinfo['content'] = content

        if 'layout' in docinfo:
            layout_file = docinfo['layout']
        else:
            layout_file = self.default_layout
            
        layout = open(self.layoutdir + '/' + layout_file + '.html')
        page = Page(layout, docinfo)
        
        return (page.generate(), page.fileout())
