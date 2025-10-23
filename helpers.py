import math
import pandas as pd
import streamlit as st
from fpdf import FPDF
import io


def get_c_factor_from_backend(product, model, max_width, max_height):
    try:
        if (product in st.session_state.PRODUCT_DATA and
                model in st.session_state.PRODUCT_DATA[product]):
            sizes = st.session_state.PRODUCT_DATA[product][model]
            for size in sizes:
                if size["width"] == max_width and size["height"] == max_height:
                    return size["c_factor"]
        return None
    except Exception as e:
        st.error(f"Error getting C-factor: {e}")
        return None


def damper_selection(airflow_lps, width_mm, height_mm, c_factor, max_width_mm, max_height_mm):
    try:
        airflow_m3s = float(airflow_lps) / 1000.0
        width_mm = float(width_mm)
        height_mm = float(height_mm)
        if width_mm <= 0 or height_mm <= 0:
            raise ValueError("Width and Height must be > 0")

        # Calculate overall area and velocity (for the entire opening)
        total_area_m2 = (width_mm / 1000.0) * (height_mm / 1000.0)
        overall_velocity = airflow_m3s / total_area_m2

        max_w = float(max_width_mm) if max_width_mm and max_width_mm > 0 else width_mm
        max_h = float(max_height_mm) if max_height_mm and max_height_mm > 0 else height_mm

        # Calculate number of sections based on MAXIMUM allowed size
        sections_wide = max(1, math.ceil(width_mm / max_w))
        sections_high = max(1, math.ceil(height_mm / max_h))
        total_sections = sections_wide * sections_high

        # Calculate ACTUAL section dimensions (using MAX size, not divided size)
        # This is the key difference - we use the maximum allowed size for sections
        section_width = min(width_mm, max_w)
        section_height = min(height_mm, max_h)
        section_area_m2 = (section_width / 1000.0) * (section_height / 1000.0)
        section_airflow_m3s = airflow_m3s / total_sections
        section_velocity = section_airflow_m3s / section_area_m2

        # Calculate section pressure drop and total pressure drop
        section_pressure_drop = float(c_factor) * (section_velocity ** 2)
        total_pressure_drop = section_pressure_drop * total_sections * 1.05

        return {
            "Width (mm)": f"{width_mm:.0f}",
            "Height (mm)": f"{height_mm:.0f}",
            "Airflow (L/s)": round(float(airflow_lps), 1),
            "Total Area (m²)": round(total_area_m2, 3),
            "Velocity (m/s)": round(overall_velocity, 2),
            "Section Size": f"{section_width:.0f}×{section_height:.0f}",
            "Section Area (m²)": round(section_area_m2, 3),
            "No of Sections": total_sections,
            "Section Velocity (m/s)": round(section_velocity, 2),
            "Section Pressure Drop (Pa)": round(section_pressure_drop, 2),
            "Total Pressure Drop (Pa)": round(total_pressure_drop, 2)
        }
    except Exception as e:
        st.error(f"Calculation error: {e}")
        return None
def save_table_as_pdf(df, customer, project, report_date):
    pdf = FPDF(orientation="L", unit="mm", format="A4")
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Pressure Drop Calculation Tool", ln=True, align="C")

    # Customer Info
    pdf.set_font("Arial", '', 12)
    pdf.ln(5)
    pdf.cell(0, 8, f"Customer: {customer}", ln=True)
    pdf.cell(0, 8, f"Project: {project}", ln=True)
    pdf.cell(0, 8, f"Date: {report_date}", ln=True)
    pdf.ln(5)

    # Define column order for export (same flow as display table)
    export_column_order = [
        "S.no","Product", "Model", "w(mm)", "H(mm)", "Airflow", "T_Area", "Vel",
        "SecSize", "SecArea", "No_Sec", "SecVel", "SecPd", "T_Pd"
    ]

    # Reorder DataFrame columns according to export_column_order
    existing_columns = [col for col in export_column_order if col in df.columns]
    df_ordered = df[existing_columns]

    # Table Header
    pdf.set_font("Arial", 'B', 10)
    page_width = pdf.w - 2 * pdf.l_margin
    col_width = page_width / len(df_ordered.columns) if len(df_ordered.columns) > 0 else page_width
    th_height = 8

    for col in df_ordered.columns:
        pdf.cell(col_width, th_height, str(col), border=1, align='C')
    pdf.ln()

    # Table Rows
    pdf.set_font("Arial", '', 10)
    for _, row in df_ordered.iterrows():
        for col in df_ordered.columns:
            pdf.cell(col_width, th_height, str(row[col]), border=1, align='C')
        pdf.ln()

    # Correct way to get bytes
    pdf_bytes = pdf.output(dest="S").encode("latin1")
    return io.BytesIO(pdf_bytes)

# http://192.168.2.228:8501/
# streamlit run app.py --server.address 0.0.0.0 --server.port 8501