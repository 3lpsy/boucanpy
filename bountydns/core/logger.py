import logging

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S'))

logger = logging.getLogger('dnsserver')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
