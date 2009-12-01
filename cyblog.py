import pickle, time, sys, yaml, constants
from converter import Converter

def configure(configfile):
    """Loads the configuration file and fills in any missing options from
    defaults in the constants file."""
    config = yaml.load(configfile)
    
    for option in constants.options.keys():
        if not option in config.keys():
            config[option] = constants.options[option]
    config['ignores'] = [config['layouts'], config['output']]
    return config

sys.path.append('.')

config = configure(open(constants.configfile))

converter = Converter(config)
converter.process()

tsfile = open(config['timestamp'], 'w')
pickle.dump(time.time(), tsfile)
tsfile.close()
