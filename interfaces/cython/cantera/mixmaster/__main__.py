import logging
from main import MixMaster

def main():
    logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)-8s: %(message)s', datefmt='%m/%d/%Y %H:%M %p',
                        filename='mixmaster.log', filemode='w', level=logging.DEBUG)

    # For console output from logging
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    #Main code
    MixMaster()

    logging.info('Mixmaster Closing')

if __name__ == '__main__':
    main()
