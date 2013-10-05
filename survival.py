from pyspades.constants import *

def apply_script(protocol, connection, config):
  
  class survivalConnection(connection):
    
	def spawn(self):
		self.weapon = RIFLE_WEAPON
		return connection.spawn(self)
  
  return protocol, survivalConnection
