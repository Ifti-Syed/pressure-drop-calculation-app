import math
import pandas as pd
import streamlit as st
from fpdf import FPDF
import io


def get_c_factor_from_backend(product, model, max_width, max_height):
    try:
        if (product in st.session_state.PRODUCT_DATA and
                model in st.session_state.PRODUCT_DATA[product]):
            for size in st.session_state.PRODUCT_DATA[product][model]:
                if size["width"] == max_width and size["height"] == max_height:
                    return size["c_factor"]
        return None
    except Exception as e:
        st.error(f"Error getting C-factor: {e}")
        return None


def damper_selection(airflow_lps, width_mm, height_mm, c_factor, max_width_mm, max_height_mm):
    """Keep current correct logic — only dimension exceeding limit gets divided."""
    try:
        airflow_m3s = float(airflow_lps) / 1000.0
        width_mm, height_mm = float(width_mm), float(height_mm)
        if width_mm <= 0 or height_mm <= 0:
            raise ValueError("Width and Height must be > 0")

        total_area_m2 = (width_mm / 1000) * (height_mm / 1000)
        overall_velocity = airflow_m3s / total_area_m2

        max_w = max_width_mm if max_width_mm > 0 else width_mm
        max_h = max_height_mm if max_height_mm > 0 else height_mm

        # Divide only the side that exceeds its max
        sections_wide = max(1, math.ceil(width_mm / max_w))
        sections_high = max(1, math.ceil(height_mm / max_h))
        total_sections = sections_wide * sections_high

        section_width = width_mm / sections_wide
        section_height = height_mm / sections_high
        section_area_m2 = (section_width / 1000) * (section_height / 1000)
        section_airflow_m3s = airflow_m3s / total_sections
        section_velocity = section_airflow_m3s / section_area_m2

        section_pressure_drop = float(c_factor) * (section_velocity ** 2)
        total_pressure_drop = section_pressure_drop * total_sections * 1.05

        return {
            "Width (mm)": f"{width_mm:.0f}",
            "Height (mm)": f"{height_mm:.0f}",
            "Airflow (L/s)": round(float(airflow_lps), 1),
            "Total Area (m²)": round(total_area_m2, 3),
            "Velocity (m/s)": round(overall_velocity, 2),
            "Max Section Width (mm)": f"{max_w:.0f}",
            "Max Section Height (mm)": f"{max_h:.0f}",
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
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Pressure Drop Calculation Tool", ln=True, align="C")
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 8, f"Customer: {customer}", ln=True)
    pdf.cell(0, 8, f"Project: {project}", ln=True)
    pdf.cell(0, 8, f"Date: {report_date}", ln=True)
    pdf.ln(5)

    df = df.copy()
    pdf.set_font("Arial", 'B', 10)
    col_width = (pdf.w - 20) / len(df.columns)
    for col in df.columns:
        pdf.cell(col_width, 8, str(col), 1, 0, "C")
    pdf.ln()
    pdf.set_font("Arial", '', 9)
    for _, row in df.iterrows():
        for col in df.columns:
            pdf.cell(col_width, 8, str(row[col]), 1, 0, "C")
        pdf.ln()
    return io.BytesIO(pdf.output(dest="S").encode("latin1"))
