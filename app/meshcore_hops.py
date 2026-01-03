import appdaemon.plugins.hass.hassapi as hass

class MeshCoreHops(hass.Hass):

    def initialize(self):
        self.log("MeshCoreHops initialized")
        
        # Listen for meshcore messages
        self.listen_event(self.handle_message, "meshcore_message")

    def handle_message(self, event_name, data, kwargs):
        try:
            # Get basic message info
            sender_name = data.get("sender_name", "Unknown")
            entity_id = data.get("entity_id")
            pubkey_prefix = data.get("pubkey_prefix")
            
            if not pubkey_prefix:
                return
            
            # Get hop information from rx_log_data
            rx_log_data = data.get("rx_log_data", [])
            
            if not rx_log_data:
                return
            
            # Process each reception path
            for rx_data in rx_log_data:
                path_len = rx_data.get("path_len")
                if path_len is None:
                    path_len = 0
                    
                snr = rx_data.get("snr")
                rssi = rx_data.get("rssi")
                path = rx_data.get("path", "")
                
                # Create/update a sensor for this contact with hop info
                sensor_id = f"sensor.meshcore_hops_{pubkey_prefix}"
                
                self.set_state(
                    sensor_id,
                    state=str(path_len),  # Must be string
                    attributes={
                        "friendly_name": f"{sender_name} Hops",
                        "sender_name": sender_name,
                        "entity_id": entity_id,
                        "path_length": path_len,
                        "snr": snr if snr is not None else 0,
                        "rssi": rssi if rssi is not None else 0,
                        "path": path if path else "",
                        "icon": "mdi:routes",
                        "unit_of_measurement": "hops"
                    }
                )
                
                self.log(f"{sender_name}: {path_len} hops, SNR: {snr}, RSSI: {rssi}")
                
        except Exception as e:
            self.log(f"Error handling message: {e}", level="ERROR")
            import traceback
            self.log(traceback.format_exc(), level="ERROR")