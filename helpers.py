# # helpers.py
#
# import math
# import pandas as pd
# import streamlit as st
# from fpdf import FPDF
# import tempfile
# import os
#
#
# def get_c_factor_from_backend(product, model, max_width, max_height):
#     """Get C-factor from product data with better error handling"""
#     try:
#         if (product and model and
#                 product in st.session_state.PRODUCT_DATA and
#                 model in st.session_state.PRODUCT_DATA[product]):
#
#             for size in st.session_state.PRODUCT_DATA[product][model]:
#                 if (isinstance(size, dict) and
#                         "width" in size and "height" in size and "c_factor" in size and
#                         size["width"] == max_width and size["height"] == max_height):
#                     return size["c_factor"]
#
#         # If exact match not found, try to find the closest size
#         if (product and model and
#                 product in st.session_state.PRODUCT_DATA and
#                 model in st.session_state.PRODUCT_DATA[product]):
#
#             sizes = st.session_state.PRODUCT_DATA[product][model]
#             if sizes:
#                 # Return the first available size's c_factor as fallback
#                 return sizes[0]["c_factor"]
#
#         return None
#     except Exception as e:
#         st.error(f"Error getting C-factor for {product}-{model}: {e}")
#         return None
#
#
# def damper_selection(airflow_lps, width_mm, height_mm, c_factor, max_width_mm, max_height_mm,
#                      safety_factor_percentage=0):
#     """Updated with safety factor as percentage input"""
#     try:
#         # Convert to float and handle None values
#         airflow_lps = float(airflow_lps or 0)
#         width_mm = float(width_mm or 0)
#         height_mm = float(height_mm or 0)
#         c_factor = float(c_factor or 0)
#         max_width_mm = float(max_width_mm or width_mm)
#         max_height_mm = float(max_height_mm or height_mm)
#         safety_factor_percentage = float(safety_factor_percentage or 0)
#
#         if width_mm <= 0 or height_mm <= 0:
#             raise ValueError("Width and Height must be > 0")
#         if c_factor <= 0:
#             raise ValueError("C-factor must be > 0")
#
#         airflow_m3s = airflow_lps / 1000.0
#         total_area_m2 = (width_mm / 1000) * (height_mm / 1000)
#         overall_velocity = airflow_m3s / total_area_m2
#
#         max_w = max_width_mm if max_width_mm > 0 else width_mm
#         max_h = max_height_mm if max_height_mm > 0 else height_mm
#
#         # Divide only the side that exceeds its max
#         sections_wide = max(1, math.ceil(width_mm / max_w))
#         sections_high = max(1, math.ceil(height_mm / max_h))
#         total_sections = sections_wide * sections_high
#
#         section_width = width_mm / sections_wide
#         section_height = height_mm / sections_high
#         section_area_m2 = (section_width / 1000) * (section_height / 1000)
#         section_airflow_m3s = airflow_m3s / total_sections
#         section_velocity = section_airflow_m3s / section_area_m2
#
#         section_pressure_drop = float(c_factor) * (section_velocity ** 2)
#
#         # NEW FORMULA: total_pressure_drop = section_pressure_drop + (total_sections * safety_factor_percentage% * section_pressure_drop)
#         safety_factor_decimal = safety_factor_percentage / 100.0
#         total_pressure_drop = section_pressure_drop + (total_sections * safety_factor_decimal * section_pressure_drop)
#
#         return {
#             "Width (mm)": f"{width_mm:.0f}",
#             "Height (mm)": f"{height_mm:.0f}",
#             "Airflow (L/s)": round(float(airflow_lps), 1),
#             "Total Area (m²)": round(total_area_m2, 3),
#             "Velocity (m/s)": round(overall_velocity, 2),
#             "Section Size": f"{section_width:.0f}×{section_height:.0f}",
#             "Section Area (m²)": round(section_area_m2, 3),
#             "No of Sections": total_sections,
#             "Section Velocity (m/s)": round(section_velocity, 2),
#             "Section Pressure Drop (Pa)": round(section_pressure_drop, 2),
#             "Total Pressure Drop (Pa)": round(total_pressure_drop, 2)
#         }
#     except Exception as e:
#         st.error(f"Calculation error: {e}")
#         return None
#
#
# def save_table_as_pdf(df, customer, project, report_date):
#     """Generate PDF and return as bytes - FIXED VERSION"""
#     try:
#         pdf = FPDF(orientation="L", unit="mm", format="A4")
#         pdf.add_page()
#
#         # Set font for header
#         pdf.set_font("Arial", 'B', 16)
#         pdf.cell(0, 10, "Pressure Drop Calculation", ln=True, align="C")
#         pdf.set_font("Arial", '', 12)
#         pdf.cell(0, 8, f"Customer: {customer}", ln=True)
#         pdf.cell(0, 8, f"Project: {project}", ln=True)
#         pdf.cell(0, 8, f"Date: {report_date}", ln=True)
#         pdf.ln(10)
#
#         # Create a copy and reset index
#         df_display = df.copy().reset_index(drop=True)
#
#         # Set font for table
#         pdf.set_font("Arial", 'B', 8)
#
#         # Calculate column widths
#         num_cols = len(df_display.columns)
#         page_width = 280  # A4 landscape width in mm minus margins
#         col_width = page_width / num_cols
#
#         # Header row
#         for col in df_display.columns:
#             # Truncate column names if too long
#             col_name = str(col)
#             if len(col_name) > 12:
#                 col_name = col_name[:10] + ".."
#             pdf.cell(col_width, 8, col_name, 1, 0, "C")
#         pdf.ln()
#
#         # Data rows
#         pdf.set_font("Arial", '', 7)
#         for _, row in df_display.iterrows():
#             for col in df_display.columns:
#                 cell_value = str(row[col]) if pd.notna(row[col]) else ""
#                 # Truncate long values
#                 if len(cell_value) > 15:
#                     cell_value = cell_value[:13] + ".."
#                 pdf.cell(col_width, 8, cell_value, 1, 0, "C")
#             pdf.ln()
#
#         # Return PDF as bytes using output(dest='S') method
#         pdf_output = pdf.output(dest='S')  # 'S' returns as string
#         pdf_bytes = pdf_output.encode('latin-1')
#
#         return pdf_bytes
#
#     except Exception as e:
#         st.error(f"PDF generation error: {e}")
#         return b""
#
#


# helpers.py
# helpers.py

import math
import pandas as pd
import streamlit as st
from fpdf import FPDF
import tempfile
import os


def get_c_factor_from_backend(category, product, model, max_width, max_height):
    """Get C-factor from product data with proper category handling"""
    try:
        # Debug info
        print(
            f"🔍 ULTRA DEBUG: Looking for C-factor: Category='{category}', Product='{product}', Model='{model}', Size={max_width}×{max_height}")

        # Check if session state has the data
        if "PRODUCT_DATA" not in st.session_state:
            print("❌ PRODUCT_DATA not in session state!")
            return None

        product_data = st.session_state.PRODUCT_DATA
        print(f"📊 Available categories: {list(product_data.keys())}")

        # Check if category exists
        if category not in product_data:
            print(f"❌ Category '{category}' not found!")
            return None

        category_data = product_data[category]
        print(f"📊 Available products in '{category}': {list(category_data.keys())}")

        # Check if product exists in category
        if product not in category_data:
            print(f"❌ Product '{product}' not found in category '{category}'!")
            return None

        product_models = category_data[product]
        print(f"📊 Available models in '{product}': {list(product_models.keys())}")

        # Check if model exists in product
        if model not in product_models:
            print(f"❌ Model '{model}' not found in product '{product}'!")
            return None

        sizes = product_models[model]
        print(f"📊 Available sizes in '{model}': {sizes}")

        # Convert to integers for comparison
        max_width = int(max_width)
        max_height = int(max_height)
        print(f"🔍 Looking for exact match: {max_width}×{max_height}")

        # Look for exact size match
        for i, size_data in enumerate(sizes):
            print(
                f"  Checking size {i}: {size_data['width']}×{size_data['height']} (type: {type(size_data['width'])}×{type(size_data['height'])})")

            if (int(size_data["width"]) == int(max_width) and
                    int(size_data["height"]) == int(max_height)):
                c_factor = size_data["c_factor"]
                print(f"✅ EXACT MATCH FOUND! C-factor = {c_factor}")
                return c_factor

        print(f"❌ NO EXACT MATCH FOUND for {max_width}×{max_height}")
        print(f"💡 Available sizes: {[(s['width'], s['height']) for s in sizes]}")

        # Try fallback to first available size
        if sizes:
            fallback = sizes[0]
            print(f"🔄 Using fallback: {fallback['width']}×{fallback['height']} with C-factor {fallback['c_factor']}")
            return fallback["c_factor"]

        return None

    except Exception as e:
        print(f"🚨 CRITICAL ERROR in get_c_factor_from_backend: {e}")
        import traceback
        print(f"Stack trace: {traceback.format_exc()}")
        return None


def damper_selection(airflow_lps, width_mm, height_mm, c_factor, max_width_mm, max_height_mm,
                     safety_factor_percentage=0):
    """Updated with safety factor as percentage input"""
    try:
        # Convert to float and handle None values
        airflow_lps = float(airflow_lps or 0)
        width_mm = float(width_mm or 0)
        height_mm = float(height_mm or 0)
        c_factor = float(c_factor or 0)
        max_width_mm = float(max_width_mm or width_mm)
        max_height_mm = float(max_height_mm or height_mm)
        safety_factor_percentage = float(safety_factor_percentage or 0)

        if width_mm <= 0 or height_mm <= 0:
            raise ValueError("Width and Height must be > 0")
        if c_factor <= 0:
            raise ValueError("C-factor must be > 0")

        airflow_m3s = airflow_lps / 1000.0
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

        # NEW FORMULA: total_pressure_drop = section_pressure_drop + (total_sections * safety_factor_percentage% * section_pressure_drop)
        safety_factor_decimal = safety_factor_percentage / 100.0
        total_pressure_drop = section_pressure_drop + (total_sections * safety_factor_decimal * section_pressure_drop)

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
    """Generate PDF and return as bytes - FIXED VERSION"""
    try:
        pdf = FPDF(orientation="L", unit="mm", format="A4")
        pdf.add_page()

        # Set font for header
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "Pressure Drop Calculation", ln=True, align="C")
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 8, f"Customer: {customer}", ln=True)
        pdf.cell(0, 8, f"Project: {project}", ln=True)
        pdf.cell(0, 8, f"Date: {report_date}", ln=True)
        pdf.ln(10)

        # Create a copy and reset index
        df_display = df.copy().reset_index(drop=True)

        # Set font for table
        pdf.set_font("Arial", 'B', 8)

        # Calculate column widths
        num_cols = len(df_display.columns)
        page_width = 280  # A4 landscape width in mm minus margins
        col_width = page_width / num_cols

        # Header row
        for col in df_display.columns:
            # Truncate column names if too long
            col_name = str(col)
            if len(col_name) > 12:
                col_name = col_name[:10] + ".."
            pdf.cell(col_width, 8, col_name, 1, 0, "C")
        pdf.ln()

        # Data rows
        pdf.set_font("Arial", '', 7)
        for _, row in df_display.iterrows():
            for col in df_display.columns:
                cell_value = str(row[col]) if pd.notna(row[col]) else ""
                # Truncate long values
                if len(cell_value) > 15:
                    cell_value = cell_value[:13] + ".."
                pdf.cell(col_width, 8, cell_value, 1, 0, "C")
            pdf.ln()

        # Return PDF as bytes using output(dest='S') method
        pdf_output = pdf.output(dest='S')  # 'S' returns as string
        pdf_bytes = pdf_output.encode('latin-1')

        return pdf_bytes

    except Exception as e:
        st.error(f"PDF generation error: {e}")
        return b""