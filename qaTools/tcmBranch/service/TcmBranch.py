from qaTools.tcmBranch.utils.server import ConfluenceOperation as CO


class TcmBranch:
    def __init__(self):
        self.server = CO()

    def get_tcm_page(self):
        return self.server.get_tcm_pages_by_cql()


