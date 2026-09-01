import subprocess
import json
import logging

class MotherboardInstallerModule:
    """
    Módulo para identificar a placa-mãe e gerar as entradas formatadas
    para o motor de instalação do seu programa.
    """

    # Mapeamento de programas oficiais dos fabricantes no Winget
    VENDOR_WINGET_MAP = {
        # --- PLACAS-MÃE & DESKTOPS ---
        "ASUSTeK COMPUTER INC.": [
            {"id": "Asus.ArmouryCrate", "log_name": "ASUS Armoury Crate", "desc": "RGB, Fans e utilitários ASUS"}
        ],
        "Micro-Star International Co., Ltd.": [
            {"id": "MSI.MSICenter", "log_name": "MSI Center", "desc": "Utilitários e monitoramento MSI"}
        ],
        "Gigabyte Technology Co., Ltd.": [
            {"id": "Gigabyte.GIGABYTEControlCenter", "log_name": "GIGABYTE Control Center", "desc": "Controle de hardware Gigabyte"}
        ],
        
        # --- INTEGRALIZADORES / NOTEBOOKS ---
        "Dell Inc.": [
            {"id": "Dell.CommandUpdate", "log_name": "Dell Command Update", "desc": "Atualizador oficial de drivers e BIOS da Dell"}
        ],
        "Lenovo": [
            {"id": "Lenovo.SystemUpdate", "log_name": "Lenovo System Update", "desc": "Atualizador automático de drivers da Lenovo"}
        ],
        "HP": [
            {"id": "HP.SupportAssistant", "log_name": "HP Support Assistant", "desc": "Diagnóstico e atualização de drivers da HP"}
        ],
        "Acer": [
            {"id": "Acer.CareCenter", "log_name": "Acer Care Center", "desc": "Gerenciador de sistema e suporte Acer"}
        ],
        "SAMSUNG": [
            {"id": "Samsung.SamsungUpdate", "log_name": "Samsung Update", "desc": "Gerenciador de drivers Samsung"}
        ]
    }

    # Softwares e Drivers genéricos para Chipsets e Redes
    GENERIC_DRIVERS_MAP = {
        "intel": [
            {
                "id": "Intel.DriverAndSupportAssistant",
                "log_name": "Intel Driver & Support Assistant",
                "desc": "Verifica e instala drivers de Chipset, Wi-Fi e Bluetooth da Intel"
            }
        ],
        "amd": [
            {
                "id": "AMD.AutoDetectAndInstall",
                "log_name": "AMD Software & Driver Auto-Detect",
                "desc": "Detecta e instala drivers de Chipset e gráficos AMD"
            }
        ],
        "realtek": [
            {
                "id": "Realtek.AudioConsole",
                "log_name": "Realtek Audio Console",
                "desc": "Gerenciador de áudio integrado Realtek"
            }
        ]
    }

    @staticmethod
    def get_motherboard_info():
        """Obtém fabricante e modelo via PowerShell."""
        try:
            cmd = 'Get-CimInstance -ClassName Win32_BaseBoard | Select-Object Manufacturer, Product | ConvertTo-Json'
            result = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)
            
            return {
                "manufacturer": data.get("Manufacturer", "Desconhecido").strip(),
                "model": data.get("Product", "Desconhecido").strip()
            }
        except Exception as e:
            logging.error(f"Erro ao obter informações da placa-mãe: {e}")
            return {"manufacturer": "Desconhecido", "model": "Desconhecido"}

    @classmethod
    def get_recommended_arrays(cls):
        """
        Identifica o hardware e gera os arrays no formato que o seu sistema consome:
        [id_programa, nome_log, situacao_booleana, tipo_operacao]
        """
        info = cls.get_motherboard_info()
        manufacturer = info["manufacturer"]
        detected_apps = []

        # 1. Busca utilitários específicos do Fabricante
        for vendor, apps in cls.VENDOR_WINGET_MAP.items():
            if vendor.lower() in manufacturer.lower():
                for app in apps:
                    detected_apps.append({
                        "id": app["id"],
                        "name": app["log_name"],
                        "desc": app["desc"]
                    })
                break

        # 2. Adiciona assistentes de driver genéricos (Intel / AMD)
        # Verifica pelo nome do modelo/fabricante se é plataforma Intel ou AMD
        combined_text = (manufacturer + " " + info["model"]).lower()
        if "amd" in combined_text or "ryzen" in combined_text:
            for app in cls.GENERIC_DRIVERS_MAP["amd"]:
                detected_apps.append({"id": app["id"], "name": app["log_name"], "desc": app["desc"]})
        else:
            # Padrão para plataformas Intel/Genéricas
            for app in cls.GENERIC_DRIVERS_MAP["intel"]:
                detected_apps.append({"id": app["id"], "name": app["log_name"], "desc": app["desc"]})

        # 3. Converte para o formato de Array do seu projeto:
        # Estrutura esperada: [id, nome_log, checado_bool, tipo]
        formatted_arrays = []
        for item in detected_apps:
            program_array = [
                item["id"],          # ex: "Asus.ArmouryCrate"
                item["name"],        # ex: "ASUS Armoury Crate"
                True,                # True por padrão se for selecionado automaticamente
                "install"            # Tipo: instalação
            ]
            formatted_arrays.append((program_array, item["desc"]))

        return info, formatted_arrays