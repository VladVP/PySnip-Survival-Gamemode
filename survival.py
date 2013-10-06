from commands import add, admin, alias
from pyspades.constants import *
from pyspades.server import weapon_reload

survival_mode = True #Do you have a problem with this vlad?
SURVIVAL_ENABLED = "Survival mode has been enabled"
SURVIVAL_DISABLED = "Survival mode has been disabled"

@alias('ts') #Stands for toggle survival
@admin
def survival(connection):
	global survival_mode
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
	
	def on_spawn(self, pos):
		if survival_mode:
			weapon_reload.player_id = killer.player_id
        		weapon_reload.clip_ammo = killer.weapon_object.current_ammo
        		weapon_reload.reserve_ammo = killer.weapon_object.current_stock + 5
        		killer.send_contained(weapon_reload)
		return connection.on_spawn(self, pos)
	
	def on_weapon_set(self, weapon):
		if survival_mode:
			return False
		return connection.on_weapon_set(self, weapon)
		
	def on_kill(self, killer, type, grenade): 
		if survival_mode:
			self.kick()
			weapon_reload.player_id = killer.player_id
        		weapon_reload.clip_ammo = killer.weapon_object.current_ammo
        		weapon_reload.reserve_ammo = killer.weapon_object.current_stock + 5
			killer.send_contained(weapon_reload)
		return connection.on_kill(self, killer, type, grenade)
  
  return protocol, survivalConnection
