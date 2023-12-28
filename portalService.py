import os
from portalUtils.SafeFileIO import SafeFileIO
from portalUtils.Logger import Logger


portal_service_logger = Logger.get_logger("SKY", "portalService")


def load_server_port():
    try:
        port_settings_path = os.path.join(os.getcwd(), "port_settings")
        port_settings_content = SafeFileIO.safe_read_file_content(port_settings_path)
        port_setting_list = port_settings_content.split("\n")
        server_port = port_setting_list[0]
        return server_port
    except Exception as e:
        portal_service_logger.error(e)
        return 12880


port_ = load_server_port()
