# MeshCore Home Assistant Panel

AppDaemon apps and dashboard cards for Home Assistant that enhance the MeshCore integration with:

- **Dynamic map visualisation** with time-based filtering
- **Real-time hop count and SNR tracking** from messages
- **Filterable contact lists** by node type and time threshold
- **Signal quality metrics** (RSSI, SNR) from mesh network paths

## Features

✅ Dynamic contact filtering by time threshold and node type  
✅ Live map visualization with automatic updates  
✅ Message hop tracking with signal quality (SNR/RSSI)  
✅ Clean, multi-column dashboard views  

## Screenshots

### Dynamic Contact List with Hops and SNR
![Contact List](dashboard/screenshots/meshcore-contacts.png)

### Live Map Visualization
![Map View](dashboard/screenshots/meshcore-map.png)

### Filtered by Node Type
![Filtered View](dashboard/screenshots/meshcore-helpers.png)

## Requirements

- Home Assistant with [MeshCore integration](https://github.com/meshcore-dev/meshcore-ha) installed
- AppDaemon add-on
- HACS Frontend cards:
  - [auto-entities](https://github.com/thomasloven/lovelace-auto-entities)
  - [config-template-card](https://github.com/iantrich/config-template-card)
  - [multiple-entity-row](https://github.com/benct/lovelace-multiple-entity-row)
  - [card-mod](https://github.com/thomasloven/lovelace-card-mod)
  - [ha-map-card](https://github.com/nathan-gs/ha-map-card)
  - [mushroom-cards](https://github.com/piitaya/lovelace-mushroom) (for input controls)

## Installation

### 1. Create Required Helpers

Go to **Settings → Devices & Services → Helpers** and create:

**Input Number - Threshold Hours**
- Name: `MeshCore Threshold Hours`
- Entity ID: `input_number.meshcore_threshold_hours`
- Minimum: `1`
- Maximum: `168` (7 days) I like 672 hours
- Step: `1`
- Unit: `hours`
- Default: `12`

**Input Select - Node Type Filter**
- Name: `MeshCore Type`
- Entity ID: `input_select.meshcore_type`
- Options:
```
  All
  Client
  Repeater
  Room Server
```

### 2. Install AppDaemon Apps

[Continue with AppDaemon installation...]

### 2. Install AppDaemon Apps

#### Finding Your AppDaemon Directory

The location depends on your installation method:

**Home Assistant OS / Supervised (AppDaemon add-on):**
```
/addon_configs/a0d7b954_appdaemon/apps/
```
Access via: `\\your-ha-ip\addon_configs\########_appdaemon\apps\`

**Docker / Manual Installation:**
```
/config/appdaemon/apps/
```
Access via: `\\your-ha-ip\config\appdaemon\apps\`

**To find your path:**
1. Install File Editor or Studio Code Server add-on
2. Look for existing AppDaemon files like `hello.py`
3. Note the directory path shown

#### Installation Steps

1. Copy the app files to your AppDaemon apps directory:
   - `meshcore_map.py`
   - `meshcore_hops.py`

2. Edit `apps.yaml` in the same directory and add:
```yaml
   meshcore_map:
     module: meshcore_map
     class: MeshCoreMapEntities

   meshcore_hops:
     module: meshcore_hops
     class: MeshCoreHops
```

3. Restart AppDaemon (Settings → Add-ons → AppDaemon → Restart)

4. Verify by checking AppDaemon logs for:
```
   INFO AppDaemon: Calling initialize() for meshcore_map
   INFO AppDaemon: Calling initialize() for meshcore_hops
   INFO meshcore_map: MeshCoreMapEntities initialized
   INFO meshcore_hops: MeshCoreHops initialized
```

5. Confirm `sensor.meshcore_map_entities` exists in Developer Tools → States
