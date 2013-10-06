from commands import add, admin, alias
from pyspades.constants import *
from pyspades.server import weapon_reload

respawn_ = False
survival_mode = True

SURVIVAL_ENABLED = "Survival mode has been enabled"
SURVIVAL_DISABLED = "Survival mode has been disabled"
NO_CHANGE = "You can't do this as survival mode is enabled"

@alias('ts') #Stands for toggle survival
@admin
def survival(connection):
	global survival_mode
	protocol = connection.protocol
	survival_mode = not survival_mode
	if survival_mode:
		protocol.send_chat(SURVIVAL_ENABLED)
		respawnall(connection) #WORKING
	else:
		protocol.send_chat(SURVIVAL_DISABLED)
		respawnall(connection) #WORKING

@alias('ra')
@admin
def respawnall(connection):
        global respawn_
        connection.respawn_ = True
add(respawnall)
add(survival)


def apply_script(protocol, connection, config):
  
  class survivalConnection(connection):     
    
	def spawn(self):
		if survival_mode:
			self.weapon = RIFLE_WEAPON
		return connection.spawn(self)

	def on_spawn(self, pos):
		if survival_mode:
			weapon_reload.player_id = self.player_id
			weapon_reload.clip_ammo = 0
			weapon_reload.reserve_ammo = 0
			self.grenades = 0
			self.weapon_object.clip_ammo = 0
			self.weapon_object.reserve_ammo = 0
			self.send_contained(weapon_reload)
		return connection.on_spawn(self, pos)

	def on_weapon_set(self, weapon):
		if survival_mode:
			self.send_chat(NO_CHANGE)
			return False
		return connection.on_weapon_set(self, weapon)

	def on_position_update(self):
		global respawn_
		if self.respawn_:
			while(self.respawn_):
				self.kill()
				self.respawn_ = False
		return connection.on_position_update(self)

	#def on_kill(self, killer, type, grenade): #FIX THIS
		#if survival_mode:
			#self.kick()
			#weapon_reload.player_id = killer.player_id
        		#weapon_reload.clip_ammo = killer.weapon_object.current_ammo
        		#weapon_reload.reserve_ammo = killer.weapon_object.current_stock + 5
			#killer.send_contained(weapon_reload)
		#return connection.on_kill(self, killer, type, grenade)
  
  return protocol, survivalConnection
