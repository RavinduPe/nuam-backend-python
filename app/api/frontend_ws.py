from app.services.network_state import network_state
from app.services.websocket_manager import manager
import json

async def frontend_ws(websocket):
    await manager.connect(websocket)
    try:
        while True:
            data_str = await websocket.receive_text()
            try:
                data = json.loads(data_str)
            except json.JSONDecodeError:
                data = {}

            # ✅ Handle subnet mask update
            subnet_mask = data.get("subnetMask")
            if subnet_mask:
                network_state.update_subnet(subnet_mask)
                print(f"Subnet updated: {network_state.subnet_mask}, Total IPs: {network_state.total_ips}")

            # Prepare updated dashboard
            from app.services.network_transformer import build_dashboard_response
            from app.core.database import SessionLocal

            db = SessionLocal()
            try:
                # Only update the network stats, other data untouched
                dashboard = build_dashboard_response({}, {})  # pass metrics & topology
                # Replace networkStats with new IP pool info
                dashboard["networkStats"]["totalIPs"] = network_state.total_ips
                dashboard["networkStats"]["poolRange"] = network_state.pool_range

                await manager.broadcast({
                    "ip_address_management": dashboard
                })
            finally:
                db.close()

    except manager.WebSocketDisconnect:
        manager.disconnect(websocket)