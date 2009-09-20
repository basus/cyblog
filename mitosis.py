import os, yaml, shutil, pickle, time

# for root, dir, files in os.walk('.'):
#     if not root == '.git':
#         for filename in dir:
#             print filename
#         print "DONE"

class mitosis:

    def __init__(self):
        self.output = 'mitosis'
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
                print '\n'
                current_outdir = self.outdir + root[1:] + '/'
                try:
                    os.mkdir(current_outdir)
                except:
                    pass
                for filename in files:
                    modify_time = os.path.getmtime(root +'/'+filename.lstrip('.'))
                    print modify_time, self.timestamp
                    if modify_time  > self.timestamp and filename[-1] != '~':
                        if filename.endswith('.markdown') or filename.endswith('.mkdwn'):
                            fl = open(current_outdir + filename, 'w')
                            fl.close()
                        else:
                            print root+filename
                            shutil.copy(root+'/'+filename.lstrip('.'), current_outdir+filename)

converter = mitosis()
converter.process()

tsfile = open('timestamp', 'w')
pickle.dump(time.time()+10, tsfile)
tsfile.close()
