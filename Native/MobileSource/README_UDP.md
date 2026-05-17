UDP integration for Beholder (Mobile → Desktop)

Overview
--------
This explains how to send detected ArUco marker data from a mobile device (or any UDP client) to the desktop Beholder app using UDP. The desktop app listens on port 8484 by default (`Native/MobileSource/UDPManager.js`).

Message format
--------------
- Each UDP packet is a single text string.
- Markers are separated by commas.
- Each marker is four space-separated numbers: `id x y rotation`
  - `id` — integer marker id
  - `x`, `y` — pixel coordinates (or normalized coords depending on your client)
  - `rotation` — rotation in radians

Example payload (two markers):
```
0 320 240 1.57,1 100 200 0.78
```

Quick test from desktop (Node.js)
--------------------------------
1. Run the Beholder app on your desktop and ensure it is listening. You should see a log like "server listening x.x.x.x:8484" in the app console.

2. From this repository run the test sender:

```bash
# send to localhost
node Native/MobileSource/send_udp_test.js 127.0.0.1 8484 "0 320 240 1.57,1 100 200 0.78"

# send to a remote desktop (replace DESKTOP_IP)
node Native/MobileSource/send_udp_test.js DESKTOP_IP 8484 "0 320 240 1.57"
```

Mobile implementation options
-----------------------------
- Native (Android/iOS): use OpenCV on the device, detect ArUco markers, and send UDP packets to `DESKTOP_IP:8484`.
- Web (quick): use OpenCV.js in the mobile browser to detect markers and send detection strings to a small server (or use WebRTC/WebSocket to forward to desktop).

Notes
-----
- Ensure mobile device and desktop are on the same LAN and that no firewall blocks UDP port 8484.
- The desktop `UDPManager` expects marker indices and will update internal marker objects accordingly.

