def apply_script(protocol, connection, config):
  
  class survivalConnection(connection):
    pass
  
  return protocol, survivalConnection
