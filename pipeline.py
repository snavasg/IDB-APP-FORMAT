# pipeline.py
import io, pandas as pd
from openpyxl import Workbook
from tables import (develop_chal_table, create_result_measure_table,
                    create_summary_next_steps_table, create_theory_of_change_table)

def run_pipeline(excel_file: bytes) -> tuple[str, bytes]:
    """
    Recibe el contenido binario de un .xlsx,
    devuelve (nombre_archivo_resultado, contenido en bytes).
    """
    # 1. Leer hojas en DataFrames --------------------------
    input_buffer = io.BytesIO(excel_file)
    df  = pd.read_excel(input_buffer, sheet_name="SDO & Result Indicators")
    df2 = pd.read_excel(input_buffer, sheet_name="Solutions & Outputs")

    # 2. Generar workbook ----------------------------------
    wb = Workbook()
    develop_chal_table(wb, data=df)
    create_result_measure_table(wb, data=df)
    create_summary_next_steps_table(wb, data=df)
    create_theory_of_change_table(wb, results_df=df, components_df=df2)

    # 3. Guardar en memoria y devolver ---------------------
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return "resultado.xlsx", output.read()
