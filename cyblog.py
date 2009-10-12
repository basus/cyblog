import os, yaml, shutil, pickle, time, sys
from page import Page

# for root, dir, files in os.walk('.'):
#     if not root == '.git':
#         for filename in dir:
#             print filename
#         print "DONE"

class cyblog:

    def __init__(self):
        self.output = 'cyblog'
        self.layoutdir = '_layouts'
        self.outdir = os.getcwd() + '/' + self.output
        try:
            tsfile = open('timestamp')
            self.timestamp = pickle.load(tsfile)
            tsfile.close()
        except:
            self.timestamp = 0

    def process(self):
        for root, dir, files in os.walk('.'):
            if root.find('/.') == -1 and root.find('./'+self.output) == -1:
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
                        else:
                            shutil.copy(filepath, current_outdir+filename)

    def htmlgen(self, indoc):
        """
        creates the html version of the markdown/yaml input
        """
        doc =  open(indoc).read().split('---\n')
        
        meta = doc[1]
        content = doc[2]
        
        docinfo = yaml.load(meta)
        docinfo['filename'] = indoc
        docinfo['content'] = content

        if 'layout' in docinfo:
            layout_file = docinfo['layout']
        else:
            layout_file = config.default_layout
            
        layout = open(self.layoutdir + '/' + layout_file + '.html')
        page = Page(layout, docinfo)
        
        return (page.generate(), page.fileout())

sys.path.append('.')
import config

converter = cyblog()
converter.process()

tsfile = open('timestamp', 'w')
pickle.dump(time.time()+10, tsfile)
tsfile.close()
