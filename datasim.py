# dslink.py
import dslink
import random
from twisted.internet import task
import asyncio


class EDGEsmartDSLink(dslink.DSLink):
    def start(self):
        self.responder.profile_manager.create_profile("simstatus")
        self.responder.profile_manager.register_callback("simstatus", self.simstatus)

    def get_default_nodes(self, super_root):
        sim_status = dslink.Node("SimStatus", super_root)
        sim_status.set_display_name("Sim Status")
        sim_status.set_writable("config")
        sim_status.set_profile("simstatus")
        sim_status.set_invokable("write")
        sim_status.set_parameters([
            {
                "name": "Status",
                "type": "bool",
                "default": False
            }
        ])

        sim_node = dslink.Node("SimNode", super_root)
        sim_node.set_display_name("Sim Data")

        super_root.add_child(sim_status)
        super_root.add_child(sim_node)

        return super_root


    def simstatus(self, parameters):
        stat = bool(parameters[1]["Status"])
        while stat == True:
            await datasim()
            await asyncio.sleep(1)

    def datasim(self):
        int = random.randint(0,255)
        self.requester.invoke("/data/publish", dslink.Permission.WRITE, params={
            "Path": "/data/test",
            "Value": int,
            "CloseStream": True
        })

def main():
    loop = asyncio.get_event

if __name__ == "__main__":
    main()
    EDGEsmartDSLink(dslink.Configuration("zzzEDGEsmart", responder=True, requester=True))
