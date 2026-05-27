from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
import logging

FORMAT = ('%(asctime)-15s %(threadName)-15s %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)

store = ModbusSlaveContext(hr=ModbusSequentialDataBlock(0, [17]*10))
context = ModbusServerContext(slaves=store, single=True)

StartTcpServer(context=context, address=("0.0.0.0", 5020))