import paramiko
import macaddress
from settings import AP


class MAC(macaddress.MAC):
     formats = (
         'xx:xx:xx:xx:xx:xx',
     ) + macaddress.MAC.formats

class UbiquitiACL:
    """Construct SSH connection"""
    def __init__(self,host) -> None:
        self.host = host
        self.ubnt = paramiko.SSHClient()
        self.ubnt.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def add_mac(self, mac , comment):
        try:

            self.ubnt.connect(self.host,22,AP["user"], AP["password"], timeout=10)
            stdin, stdout, stderr = self.ubnt.exec_command("cat /tmp/system.cfg | grep wireless.1.mac_acl.")
            self.data = stdout.readlines()


            last_number = 0
            for x in self.data:
                if x.startswith("wireless.1.mac_acl."):
                    parts = x.split(".")
                try:
                    last_number = max(last_number, int(parts[-2]))
                except:
                    pass
            
                mac_address = MAC(mac)
                command = f"echo -e 'wireless.1.mac_acl.{last_number+1}.mac={mac_address}\nwireless.1.mac_acl.{last_number+1}.comment={comment}\nwireless.1.mac_acl.{last_number+1}.status=enabled' >> /tmp/system.cfg"
                self.ubnt.exec_command(command)
            
            return f"mac {mac} registrada exitasamente"
        except Exception as e:
            return e.__str__()