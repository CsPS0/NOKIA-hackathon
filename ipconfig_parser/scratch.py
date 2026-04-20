import re
import json
from pathlib import Path

def parse_ipconfig(content):
    adapters = []
    current_adapter = None
    current_key = None

    for line in content.splitlines():
        if not line.strip():
            continue
        
        # New adapter block
        if not line.startswith(" ") and line.endswith(":"):
            current_adapter = {
                "adapter_name": line[:-1].strip(),
                "description": "",
                "physical_address": "",
                "dhcp_enabled": "",
                "ipv4_address": "",
                "subnet_mask": "",
                "default_gateway": "",
                "dns_servers": []
            }
            adapters.append(current_adapter)
            current_key = None
            continue
            
        if current_adapter is not None:
            if ":" in line:
                key_part, val_part = line.split(":", 1)
                key_clean = key_part.replace(".", "").strip().lower()
                val_clean = val_part.strip()
                
                if key_clean == "description":
                    current_adapter["description"] = val_clean
                    current_key = "description"
                elif key_clean == "physical address":
                    current_adapter["physical_address"] = val_clean
                    current_key = "physical_address"
                elif key_clean == "dhcp enabled":
                    current_adapter["dhcp_enabled"] = val_clean
                    current_key = "dhcp_enabled"
                elif key_clean == "ipv4 address":
                    # Remove (Preferred) or (Deferred) etc
                    val_clean = val_clean.split("(")[0].strip()
                    current_adapter["ipv4_address"] = val_clean
                    current_key = "ipv4_address"
                elif key_clean == "subnet mask":
                    current_adapter["subnet_mask"] = val_clean
                    current_key = "subnet_mask"
                elif key_clean == "default gateway":
                    if val_clean:
                        if ":" not in val_clean or "." in val_clean: # basic ipv4 check or just take first?
                            current_adapter["default_gateway"] = val_clean
                    current_key = "default_gateway"
                elif key_clean == "dns servers":
                    if val_clean:
                        current_adapter["dns_servers"].append(val_clean)
                    current_key = "dns_servers"
                else:
                    current_key = None
            else:
                # Continuation of previous key
                val_clean = line.strip()
                if not val_clean:
                    continue
                if current_key == "dns_servers":
                    current_adapter["dns_servers"].append(val_clean)
                elif current_key == "default_gateway":
                    if not current_adapter["default_gateway"]:
                        current_adapter["default_gateway"] = val_clean
                    elif "." in val_clean and ":" not in current_adapter["default_gateway"]:
                        pass # already have ipv4
                    elif "." in val_clean:
                        current_adapter["default_gateway"] = val_clean
                        
    return adapters

for f in Path(".").glob("*.txt"):
    try:
        content = f.read_text(encoding="utf-16")
    except:
        content = f.read_text(encoding="utf-8")
    
    print(f.name)
    print(json.dumps(parse_ipconfig(content), indent=2))
