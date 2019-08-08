import os, ConfigParser

"""
Read ini config file using config parser 
and get job processing limit 
and partition the list of jobs as per the limit.
"""


def chunks(jobs,processing_limit):
    """
    partition the list of values based on the given limit
    :param jobs: list
    :param processing_limit: int
    :return:
    """
    # For item i in a range that is a length of l,
    for i in range(0, len(jobs), processing_limit):
        # Create an index range for l of n items:
        yield jobs[i:i+processing_limit]


def readfile(ini_file):
    """
    Read the config file for configurable parameters.
    Read Config from the given path.
    :param ini_file:configuration input file for script
    :return: inputs - sections values pair
    """
    try:
        config = ConfigParser.ConfigParser()
        config.read(ini_file)
        inputs = {}
        if not any(config.sections()):
            print("No Valid Input Configuration Found ")
            return None
        for section in config.sections():
            inputs[section] = {}
            if not any(config.items(section)):
                print("No Valid Input Configuration Found for {0}".format(section))
                return None
            for option, value in config.items(section):
                inputs[section][option] = value
        return inputs
    except Exception as e:
        print("Given Module Config File is not valid. Could not Parse : {0}".format(e))
    return None


file_name = os.path.join(os.path.abspath(os.getcwd()),'config.ini')
"""assume ini file  contains
[TEST_HEADER]
 LIMIT=10
"""
configs = readfile(file_name)
section , sub_section = 'TEST_HEADER', 'LIMIT'  ## assume its integer value
limit = configs.get('',{}).get(sub_section.lower())
if str(limit).isdigit():
    jobs = [data for data in range(1,10000)]
    print list(chunks(jobs,int(limit)))
else:
    print("Expecting an int value ")