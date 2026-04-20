import json
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import List, Dict, Any

@dataclass
class Adapter:
    adapter_name: str
    description: str = ""
    physical_address: str = ""
    dhcp_enabled: str = ""
    ipv4_address: str = ""
    subnet_mask: str = ""
    default_gateway: str = ""
    dns_servers: List[str] = field(default_factory=list)

def parse_ipconfig(content: str) -> List[Dict[str, Any]]:
    adapters: List[Adapter] = []
    current_adapter: Adapter | None = None
    current_key: str | None = None


    prop_pattern = re.compile(r"^\s+([a-zA-Z0-9\s-]+?)(?:\s*\.\s*)*:\s*(.*)$")

    for line in content.splitlines():
        if not line.strip():
            continue
        

        if not line.startswith(" ") and line.endswith(":"):
            adapter_name = line[:-1].strip()
            current_adapter = Adapter(adapter_name=adapter_name)
            adapters.append(current_adapter)
            current_key = None
            continue
            
        if current_adapter is not None:
            match = prop_pattern.match(line)
            if match:
                key_raw, val_raw = match.groups()
                key_clean = key_raw.strip().lower()
                val_clean = val_raw.strip()
                

                if "description" in key_clean:
                    current_adapter.description = val_clean
                    current_key = "description"
                elif "physical address" in key_clean:
                    current_adapter.physical_address = val_clean
                    current_key = "physical_address"
                elif "dhcp enabled" in key_clean:
                    current_adapter.dhcp_enabled = val_clean
                    current_key = "dhcp_enabled"
                elif "ipv4 address" in key_clean:
                    val_clean = val_clean.split("(")[0].strip()
                    current_adapter.ipv4_address = val_clean
                    current_key = "ipv4_address"
                elif "subnet mask" in key_clean:
                    current_adapter.subnet_mask = val_clean
                    current_key = "subnet_mask"
                elif "default gateway" in key_clean:
                    if val_clean and (":" not in val_clean or "." in val_clean):
                        current_adapter.default_gateway = val_clean
                    current_key = "default_gateway"
                elif "dns servers" in key_clean:
                    if val_clean:
                        current_adapter.dns_servers.append(val_clean)
                    current_key = "dns_servers"
                else:
                    current_key = None
            else:

                val_clean = line.strip()
                if not val_clean:
                    continue
                if current_key == "dns_servers":
                    current_adapter.dns_servers.append(val_clean)
                elif current_key == "default_gateway":
                    if not current_adapter.default_gateway:
                        current_adapter.default_gateway = val_clean
                    elif "." in val_clean and ":" not in current_adapter.default_gateway:
                        pass 
                    elif "." in val_clean:
                        current_adapter.default_gateway = val_clean
                        
    return [asdict(adapter) for adapter in adapters]

def main() -> None:
    result = []
    base_dir = Path(__file__).parent
    
    for file_path in sorted(base_dir.glob("*.txt")):
        if file_path.name == "input.txt" or file_path.name == "output.json": 
            continue
        try:
            content = file_path.read_text(encoding="utf-16")
        except UnicodeError:
            content = file_path.read_text(encoding="utf-8")
            
        adapters = parse_ipconfig(content)
        result.append({
            "file_name": file_path.name,
            "adapters": adapters
        })
    
    output_path = base_dir / "output.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
