import routeros_api
import macaddress
from settings import AP


class MAC(macaddress.MAC):
     formats = (
         'xx:xx:xx:xx:xx:xx',
     ) + macaddress.MAC.formats

class  MikrotikACL:
    def __init__(self, host) -> None:
        self.host = host
        

    def add_mac(self, mac, comment: str):
        try:
            try:
                self.api = routeros_api.connect(self.host,AP["user"], AP["password"],plaintext_login = False)
            except:
                self.api = routeros_api.connect(self.host,AP["user"], AP["password"],plaintext_login = True)

            self.api.get_binary_resource('/interface/wireless/access-list').call("add",{"mac-address":str(MAC(mac)).encode(), "comment":comment.encode()})
            return f"mac {mac} registrada exitosamente"
        except Exception as e:
            return str(e.__str__())