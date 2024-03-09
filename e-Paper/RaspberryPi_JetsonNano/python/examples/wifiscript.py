import wireless

class WiFiManager:
    def get_current_ssid(self):
        try:
            wifi = wireless.Wireless()
            status = wifi.current()
            return status
        except Exception as e:
            print(f"Error getting current SSID: {e}")
        return None

# Example usage
wifi_manager = WiFiManager()
current_ssid = wifi_manager.get_current_ssid()
if current_ssid:
    print(f"Current SSID: {current_ssid}")
else:
    print("Not connected to any network.")
