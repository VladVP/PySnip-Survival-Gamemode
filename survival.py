from pyspades.constants import *
from commnads import add, admin, alias

survival_mode = True #Do you have a problem with this vlad?
SURVIVAL_ENABLED = "Survival mode has been enabled"
SURVIVAL_DISABLED = "Survival mode has been disabled"

@alias('ts') #Stands for toggle survival
@admin
def survival(connection):
	protocol = connection.protocol
	survival_mode = not survival_mode
	if survival_mode:
		protocol.send_chat(SURVIVAL_ENABLED)
	else:
		protocol.send_chat(SURVIVAL_DISABLED)
		
add(survival)
	

def apply_script(protocol, connection, config):
  
  class survivalConnection(connection):
    
	def spawn(self):
		if survival_mode:
			self.weapon = RIFLE_WEAPON
		return connection.spawn(self)
  
  return protocol, survivalConnection
