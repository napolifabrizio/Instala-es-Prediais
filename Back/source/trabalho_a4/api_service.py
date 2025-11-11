from typing import Optional

class ApiService:
    def __init__(self):
        # Constantes baseadas na NBR 8160:1999 (para referência residencial)
        self.SIMPLE_RESIDENTIAL_MINIMUM_VOLUME = 18
        self.DUAL_RESIDENTIAL_MINIMUM_VOLUME = 31

    def calculate_residential(self, num_sinks: int, num_people: Optional[int] = 0):
        value = 0
        if num_sinks == 1:
            value = {
                "title": "Recomendação: Caixa de Gordura Simples (CGS)",
                "volume_liters": self.SIMPLE_RESIDENTIAL_MINIMUM_VOLUME,
                "message": "Volume mínimo para 1 cozinha, conforme NBR 8160."
            }
        elif num_sinks == 2:
            value = {
                "title": "Recomendação: Caixa de Gordura Dupla (CGD)",
                "volume_liters": self.DUAL_RESIDENTIAL_MINIMUM_VOLUME,
                "message": "Volume mínimo para 2 cozinhas, conforme NBR 8160."
            }
        else:
            # Fórmula NBR 8160 (4.2.5.4): V = 2 * N
            volume = (2 * num_people)
            value = {
                "title": "Recomendação: Caixa de Gordura Especial (CGE)",
                "volume_liters": volume,
                "volume_m3": volume / 1000,
                "message": f"Cálculo para {num_people} pessoas em edificação coletiva (V = 2 * N)."
            }
        return value

    def calculate_commercial(self, num_meals: int):
        volume = (2 * num_meals) + 20
        value = {
            "title": "Cálculo para Uso Comercial",
            "volume_liters": volume,
            "volume_m3": volume / 1000,
            "message": f"Cálculo baseado em {num_meals} refeições diárias (V = 2N + 20)."
        }
        return value

    def get_siphon_box_pipes(
        self,
        sinks: int = 0,
        showers: int = 0,
        tubs: int = 0,
        laundry: int = 0,
        utility_sinks: int = 0,
        floor_drains: int = 0
    ):
        # === 1. UHC (Unidades Hunter de Contribuição) ===
        UHC_SINKS = 1
        UHC_SHOWERS = 2
        UHC_TUBS = 2
        UHC_LAUNDRY = 3
        UHC_UTILITY_SINKS = 3
        UHC_FLOOR_DRAINS = 1

        total_uhc = (
            (sinks * UHC_SINKS) +
            (showers * UHC_SHOWERS) +
            (tubs * UHC_TUBS) +
            (laundry * UHC_LAUNDRY) +
            (utility_sinks * UHC_UTILITY_SINKS) +
            (floor_drains * UHC_FLOOR_DRAINS)
        )

        if total_uhc == 0:
            return {"error": "Nenhum aparelho foi informado para cálculo."}

        # === 2. Determinação do diâmetro da caixa sinfonada ===
        if total_uhc <= 2:
            d_saida = 40
        elif total_uhc <= 6:
            d_saida = 50
        elif total_uhc <= 20:
            d_saida = 75
        else:
            d_saida = 100

        d_saida = max(d_saida, 50)  # mínimo NBR 8160
        d_entrada = 40 if d_saida == 50 else 50  # simplificação usual

        # === 3. Tubo de queda (Dq) ===
        # Regra simplificada: depende do total de UHC
        if total_uhc <= 6:
            d_queda = 75
        elif total_uhc <= 20:
            d_queda = 100
        else:
            d_queda = 150

        # === 4. Tubo de gordura (Dg) ===
        # Usa o mesmo da saída, mas com mínimo de 75 mm (prática comum)
        d_gordura = max(d_saida, 75)

        # === 5. Tubo de ventilação (Dv) ===
        # NBR 8160 recomenda 40 ou 50 mm
        d_vent = 40 if d_saida <= 75 else 50

        # === 6. Perda de carga (estimativa simplificada) ===
        # h_f = k * (L/D)^1.75  (modelo empírico)
        k = 0.02  # fator empírico médio
        L = 3     # metros (comprimento médio de ramal)
        hf = round(k * ((L / (d_saida / 1000)) ** 1.75), 3)

        value = {
            "outlet_pipe_mm": d_saida,
            "inlet_pipe_mm": d_entrada,
            "fall_pipe_mm": d_queda,
            "grease_pipe_mm": d_gordura,
            "vent_pipe_mm": d_vent,
            "head_loss_m": hf,
            "total_uhc": total_uhc,
            "message": (
                f"Cálculo para {total_uhc} UHCs (Unidades Hunter). "
                f"Perda de carga estimada: {hf} mca."
            )
        }

        return value

