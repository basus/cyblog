import pickle, time, sys
from converter import Converter

sys.path.append('.')

try:
    import config
except:
    import default as config

converter = Converter(config)
converter.process()

tsfile = open(config.timestamp, 'w')
pickle.dump(time.time(), tsfile)
tsfile.close()
