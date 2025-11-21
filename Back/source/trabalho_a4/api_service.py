from typing import Optional

class ApiService:
    def __init__(self):
        # Constantes baseadas na NBR 8160:1999 (para referência residencial)
        self.SIMPLE_RESIDENTIAL_MINIMUM_VOLUME = 18
        self.DUAL_RESIDENTIAL_MINIMUM_VOLUME = 31

    def calculate_residential(self, num_sinks: int, num_people: Optional[int] = 0):
        value = 0
        # Frequência padrão residencial: Semestral
        maintenance_msg = "A cada 6 meses (Semestral)"

        if num_sinks == 1:
            value = {
                "title": "Recomendação: Caixa de Gordura Simples (CGS)",
                "volume_liters": self.SIMPLE_RESIDENTIAL_MINIMUM_VOLUME,
                "message": "Volume mínimo para 1 cozinha, conforme NBR 8160.",
                "maintenance_interval": maintenance_msg
            }
        elif num_sinks == 2:
            value = {
                "title": "Recomendação: Caixa de Gordura Dupla (CGD)",
                "volume_liters": self.DUAL_RESIDENTIAL_MINIMUM_VOLUME,
                "message": "Volume mínimo para 2 cozinhas, conforme NBR 8160.",
                "maintenance_interval": maintenance_msg
            }
        else:
            # Fórmula NBR 8160 (4.2.5.4): V = 2 * N
            volume = (2 * num_people)
            value = {
                "title": "Recomendação: Caixa de Gordura Especial (CGE)",
                "volume_liters": volume,
                "volume_m3": volume / 1000,
                "message": f"Cálculo para {num_people} pessoas em edificação coletiva (V = 2 * N).",
                # Para edifícios, a carga é maior, recomenda-se limpeza trimestral
                "maintenance_interval": "A cada 3 meses (Trimestral)"
            }
        return value

    def calculate_commercial(self, num_meals: int):
        volume = (2 * num_meals) + 20

        # Lógica para definir a frequência de manutenção comercial
        if num_meals <= 100:
            maintenance = "Mensal"
        elif num_meals <= 400:
            maintenance = "Semanal"
        else:
            maintenance = "Diária"

        value = {
            "title": "Cálculo para Uso Comercial",
            "volume_liters": volume,
            "volume_m3": volume / 1000,
            "message": f"Cálculo baseado em {num_meals} refeições diárias (V = 2N + 20).",
            "maintenance_interval": maintenance
        }
        return value

    # Renomeado para 'calculate_' para manter padrão, ajuste no handler se necessário
    def calculate_siphon_pipes(self,
        sinks: int = 0,
        showers: int = 0,
        tubs: int = 0,
        laundry: int = 0,
        utility_sinks: int = 0,
        floor_drains: int = 0
    ):
        # Unidades Hunter de Contribuição (UHC) - NBR 8160.
        # Tabela 1 NBR 8160 (Valores de UHC)
        UHC_SINKS = 1           # Lavatório
        UHC_SHOWERS = 2         # Chuveiro
        UHC_TUBS = 2            # Banheira
        UHC_LAUNDRY = 3         # Máq. Lavar Roupa
        UHC_UTILITY_SINKS = 3   # Tanque
        UHC_FLOOR_DRAINS = 1    # Ralo de Piso Seco

        # 1. Somar o total de UHCs
        total_uhc = (
            (sinks * UHC_SINKS) +
            (showers * UHC_SHOWERS) +
            (tubs * UHC_TUBS) +
            (laundry * UHC_LAUNDRY) +
            (utility_sinks * UHC_UTILITY_SINKS) +
            (floor_drains * UHC_FLOOR_DRAINS)
        )

        if total_uhc == 0:
            return {"error": "Nenhum aparelho foi selecionado. O cálculo não pôde ser realizado."}

        # 2. Tabela 2 NBR 8160 (Diâmetro x UHC para ramais de esgoto)
        calculated_diameter = 0
        if total_uhc <= 2:
            calculated_diameter = 40
        elif total_uhc <= 6:
            calculated_diameter = 50
        elif total_uhc <= 20:
            calculated_diameter = 75
        else: # Mais de 20 UHCs
            calculated_diameter = 100

        # 3. Regra Mínima (NBR 8160 item 4.2.2.3)
        # O diâmetro de saída de uma caixa sifonada deve ser no mínimo 50mm.
        outlet_pipe_mm = max(calculated_diameter, 50)
        value = {
            "outlet_pipe_mm": outlet_pipe_mm,
            "inlet_info": "Entradas de 50mm e 40mm compatíveis.",
            "message": f"Cálculo baseado em {total_uhc} UHCs (Unidades Hunter de Contribuição)."
        }
        return value