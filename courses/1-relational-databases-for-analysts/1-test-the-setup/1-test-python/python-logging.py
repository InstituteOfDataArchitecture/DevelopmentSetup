import logging

agent_tr = sum(range(7, 12), 2)
agent_bjb = sum(range(1, 4), 1)

logging.basicConfig(
    filename='/workspace/logfile.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

logging.info('The logfile number is: ' + str(agent_tr))

print('The terminal number is: ' + str(agent_bjb).zfill(3))