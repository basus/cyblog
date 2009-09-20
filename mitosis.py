import os, yaml, shutil, pickle, time

# for root, dir, files in os.walk('.'):
#     if not root == '.git':
#         for filename in dir:
#             print filename
#         print "DONE"

try:
    tsfile = open('timestamp')
    timestamp = pickle.load(tsfile)
    tsfile.close()
except:
    timestamp = 0

output = 'mitosis'
outdir = os.getcwd() + '/' + output

for root, dir, files in os.walk('.'):
    if root.find('/.') == -1 and root.find('./'+output) == -1:
        print '\n'
        current_outdir = outdir + root[1:] + '/'
        try:
            os.mkdir(current_outdir)
        except:
            pass
        for filename in files:
            modify_time = os.path.getmtime(root +'/'+filename.lstrip('.'))
            print modify_time, timestamp
            if modify_time  > timestamp:
                if filename.endswith('.markdown') or filename.endswith('.mkdwn'):
                    fl = open(current_outdir + filename, 'w')
                    fl.close()
                else:
                    print root+filename
                    shutil.copy(root+'/'+filename.lstrip('.'), current_outdir+filename)

tsfile = open('timestamp', 'w')
pickle.dump(time.time()+10, tsfile)
tsfile.close()
