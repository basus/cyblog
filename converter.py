import os,yaml,shutil
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
                current_outdir = self.outdir + root[1:] + '/'
                try:
                    os.mkdir(current_outdir)
                except:
                    pass
                
                for filename in files:
                    filepath = root +'/'+filename.lstrip('.')
                    modify_time = os.path.getmtime(filepath)

                    if modify_time  > self.timestamp and filename[-1] != '~':
                        if filename.endswith('.markdown') or filename.endswith('.mkdwn'):

                            html, html_file = self.htmlgen(filepath)
                            html_file = open(self.outdir + '/'+ html_file, 'w')
                            html_file.write(html)
                            
                            html_file.close()
                        elif filename[1] != '_':
                            shutil.copy(filepath, current_outdir+filename)

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
