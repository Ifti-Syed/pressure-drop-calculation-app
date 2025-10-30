# app.py
import streamlit as st
from datetime import date
import pandas as pd

from config import DEFAULT_PRODUCTS, CATEGORIES
from helpers import damper_selection, get_c_factor_from_backend, save_table_as_pdf
import styles

# Load CSS/styles
styles.load_styles()

# ------------------- Page Config -------------------
st.set_page_config(page_title="Pressure Drop Calculation Tool", page_icon="🌀", layout="wide")

# ------------------- Session State Initialization -------------------
if "PRODUCT_DATA" not in st.session_state:
    st.session_state.PRODUCT_DATA = DEFAULT_PRODUCTS.copy()
if "damper_table" not in st.session_state:
    st.session_state.damper_table = pd.DataFrame()
if "rows_to_delete" not in st.session_state:
    st.session_state.rows_to_delete = []
if "uploaded_filename" not in st.session_state:
    st.session_state.uploaded_filename = None
if "export_columns" not in st.session_state:
    st.session_state.export_columns = []

# ------------------- Header -------------------
st.markdown("<div class='top-bar'><h2>🌀 Pressure Drop Calculation Tool</h2></div>", unsafe_allow_html=True)

# ------------------- Customer Info -------------------
col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    customer = st.text_input("Customer Name", value=st.session_state.get("customer", ""))
with col2:
    project = st.text_input("Project Name", value=st.session_state.get("project", ""))
with col3:
    report_date = st.date_input("Date", value=date.today())

st.session_state.customer = customer
st.session_state.project = project

st.markdown("---")

# ------------------- Bulk Upload -------------------
st.subheader("📂 Bulk Upload Data (CSV / Excel)")
uploaded_file = st.file_uploader(
    "Upload CSV/Excel with columns: Category, Width (mm), Height (mm), Airflow (L/s), Product, Model, Max Width (mm), Max Height (mm), Tag No, Safety Factor (%)",
    type=["csv", "xlsx", "xls"]
)

if uploaded_file is not None:
    if uploaded_file.name != st.session_state.uploaded_filename:
        try:
            if uploaded_file.name.lower().endswith(".csv"):
                try:
                    df = pd.read_csv(uploaded_file)
                except Exception:
                    df = pd.read_csv(uploaded_file, encoding="latin1", on_bad_lines="skip")
            else:
                df = pd.read_excel(uploaded_file)

            st.success(f"✅ File '{uploaded_file.name}' uploaded ({len(df)} rows).")
            st.dataframe(df.head())

            required = ["Width (mm)", "Height (mm)", "Airflow (L/s)", "Product", "Model", "Max Width (mm)",
                        "Max Height (mm)"]
            missing = [c for c in required if c not in df.columns]
            if missing:
                st.warning(f"Missing columns: {', '.join(missing)}")
            else:
                results = []
                errors = []
                for idx, row in df.iterrows():
                    try:
                        airflow_val = row.get("Airflow (L/s)", 0)
                        w_val = row.get("Width (mm)", 0)
                        h_val = row.get("Height (mm)", 0)
                        product_val = row.get("Product", "")
                        model_val = row.get("Model", "")
                        mw_val = row.get("Max Width (mm)", 0)
                        mh_val = row.get("Max Height (mm)", 0)
                        tag_no = row.get("Tag No", f"Tag_{idx + 1}")
                        category_val = row.get("Category", "Life Safety Damper")
                        safety_val = row.get("Safety Factor (%)", 5.0)

                        c_val = get_c_factor_from_backend(product_val, model_val, mw_val, mh_val)

                        if c_val is None:
                            errors.append(
                                f"Row {idx + 1}: No C-factor found for {product_val} - {model_val} with size {mw_val}×{mh_val}mm")
                            continue

                        res = damper_selection(airflow_val, w_val, h_val, c_val, mw_val, mh_val, safety_val)
                        if res:
                            res["Category"] = category_val
                            res["Product"] = product_val
                            res["Model"] = model_val
                            res["Tag No"] = tag_no
                            res["Safety Factor (%)"] = float(safety_val)
                            results.append(res)
                    except Exception as e:
                        errors.append(f"Row {idx + 1}: {str(e)}")

                if errors:
                    st.warning(f"⚠️ {len(errors)} errors found during processing:")
                    for error in errors:
                        st.write(f"• {error}")

                if results:
                    bulk_df = pd.DataFrame(results)
                    st.session_state.damper_table = pd.concat([st.session_state.damper_table, bulk_df],
                                                              ignore_index=True)
                    st.session_state.uploaded_filename = uploaded_file.name
                    st.success(f"✅ Calculated and added {len(results)} rows.")
                    st.dataframe(bulk_df)
                else:
                    st.info("No valid calculation results produced from the file.")
        except Exception as e:
            st.error(f"Upload error: {e}")
    else:
        st.info(f"File '{uploaded_file.name}' already processed. Upload another file to add more rows.")

st.markdown("---")

# ------------------- Manual Calculation -------------------
st.subheader("Manual Calculation")

# First line: Category, Product, Model, Size
col1, col2, col3, col4 = st.columns(4)

with col1:
    category = st.selectbox("Category", CATEGORIES, key="category_select")

with col2:
    product = st.selectbox("Product", ["Select Product"] + list(st.session_state.PRODUCT_DATA.keys()),
                           key="product_select")

model = "Select Model"
selected = "Select Size"
max_width = max_height = c_factor = 0

if product != "Select Product":
    with col3:
        model = st.selectbox("Model", ["Select Model"] + list(st.session_state.PRODUCT_DATA[product].keys()),
                             key="model_select")

if model != "Select Model":
    sizes = st.session_state.PRODUCT_DATA[product][model]
    sorted_sizes = sorted(sizes, key=lambda x: x['width'] * x['height'], reverse=True)
    size_options = [f"{s['width']}×{s['height']} mm" for s in sorted_sizes]

    with col4:
        default_index = 0 if size_options else 0
        selected = st.selectbox("Select Size", options=size_options, index=default_index, key="size_select")

    if selected != "Select Size":
        idx = size_options.index(selected)
        max_width, max_height, c_factor = sorted_sizes[idx]["width"], sorted_sizes[idx]["height"], sorted_sizes[idx][
            "c_factor"]

# Second line: Tag, Airflow, Width, Height, Safety Factor
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    tag_no = st.text_input("Tag No", value="", placeholder="Enter tag number", key="tag_input")

with col2:
    airflow = st.number_input("Airflow (L/s)", min_value=0.0, value=0.0, step=1.0, key="airflow_input")

with col3:
    width = st.number_input("Width (mm)", min_value=0.0, value=0.0, key="width_input")

with col4:
    height = st.number_input("Height (mm)", min_value=0.0, value=0.0, key="height_input")

with col5:
    safety_factor_local = st.number_input("Safety Factor (%)", min_value=0.0, value=5.0, step=0.5,
                                          key="safety_factor_local")

width_mm = width
height_mm = height

# Third line: Display calculated values
if width_mm > 0 and height_mm > 0 and airflow > 0 and c_factor > 0:
    preview = damper_selection(airflow, width_mm, height_mm, c_factor, max_width, max_height, safety_factor_local)
    if preview:
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Total Velocity (m/s)", value=preview["Velocity (m/s)"], disabled=True)
        with col2:
            st.text_input("Total Pressure Drop (Pa)", value=preview["Total Pressure Drop (Pa)"], disabled=True)
else:
    st.info("Enter Width, Height, Airflow and select a valid size to preview calculation.")

if st.button("➕ Add to Table", width='stretch'):
    if product == "Select Product" or model == "Select Model" or selected == "Select Size":
        st.warning("Select product, model and size first.")
    elif not tag_no:
        st.warning("Please enter a Tag No.")
    else:
        res = damper_selection(airflow, width_mm, height_mm, c_factor, max_width, max_height, safety_factor_local)
        if res:
            res["Category"] = category
            res["Product"] = product
            res["Model"] = model
            res["Tag No"] = tag_no
            res["Safety Factor (%)"] = float(safety_factor_local)
            st.session_state.damper_table = pd.concat([st.session_state.damper_table, pd.DataFrame([res])],
                                                      ignore_index=True)
            st.success("✅ Manual calculation added to table.")
            st.rerun()

st.markdown("---")

# ------------------- Project Summary -------------------
st.subheader("📊 Project Summary")

if not st.session_state.damper_table.empty:
    st.write(f"**Customer:** {customer} | **Project:** {project} | **Date:** {report_date}")

    display_table = st.session_state.damper_table.copy()

    # Ensure Safety Factor column exists
    if "Safety Factor (%)" not in display_table.columns:
        display_table["Safety Factor (%)"] = 5.0
    else:
        display_table["Safety Factor (%)"] = display_table["Safety Factor (%)"].fillna(5.0)

    # Add helper columns
    display_table.insert(0, "Sr No", [str(i) for i in range(1, len(display_table) + 1)])
    display_table.insert(1, "Select", False)

    # Define column order
    column_order = [
        "Sr No", "Select", "Tag No", "Category", "Product", "Model",
        "Width (mm)", "Height (mm)", "Airflow (L/s)", "Safety Factor (%)",
        "Total Area (m²)", "Velocity (m/s)", "Max Section Width (mm)", "Max Section Height (mm)",
        "Section Size", "Section Area (m²)", "No of Sections",
        "Section Velocity (m/s)", "Section Pressure Drop (Pa)", "Total Pressure Drop (Pa)"
    ]

    existing_columns = [col for col in column_order if col in display_table.columns]
    display_table = display_table[existing_columns]

    # Prepare dropdown options
    all_products = list(st.session_state.PRODUCT_DATA.keys())
    all_models = []
    for product_name in all_products:
        for model_name in st.session_state.PRODUCT_DATA[product_name].keys():
            all_models.append(model_name)
    all_models = list(set(all_models))

    # Column config
    column_config = {
        "Sr No": st.column_config.TextColumn("Sr No", disabled=True),
        "Select": st.column_config.CheckboxColumn("Select"),
        "Tag No": st.column_config.TextColumn("Tag No"),
        "Category": st.column_config.SelectboxColumn("Category", options=CATEGORIES),
        "Product": st.column_config.SelectboxColumn("Product", options=all_products),
        "Model": st.column_config.SelectboxColumn("Model", options=all_models),
        "Width (mm)": st.column_config.NumberColumn("Width (mm)", format="%d"),
        "Height (mm)": st.column_config.NumberColumn("Height (mm)", format="%d"),
        "Airflow (L/s)": st.column_config.NumberColumn("Airflow (L/s)", format="%.1f"),
        "Safety Factor (%)": st.column_config.NumberColumn("Safety Factor (%)", format="%.2f"),
        "Total Area (m²)": st.column_config.NumberColumn("Total Area (m²)", format="%.3f", disabled=True),
        "Velocity (m/s)": st.column_config.NumberColumn("Velocity (m/s)", format="%.2f", disabled=True),
        "Max Section Width (mm)": st.column_config.NumberColumn("Max Section Width (mm)", format="%d"),
        "Max Section Height (mm)": st.column_config.NumberColumn("Max Section Height (mm)", format="%d"),
        "Section Size": st.column_config.TextColumn("Section Size", disabled=True),
        "Section Area (m²)": st.column_config.NumberColumn("Section Area (m²)", format="%.3f", disabled=True),
        "No of Sections": st.column_config.NumberColumn("No of Sections", format="%d", disabled=True),
        "Section Velocity (m/s)": st.column_config.NumberColumn("Section Velocity (m/s)", format="%.2f", disabled=True),
        "Section Pressure Drop (Pa)": st.column_config.NumberColumn("Section Pressure Drop (Pa)", format="%.2f",
                                                                    disabled=True),
        "Total Pressure Drop (Pa)": st.column_config.NumberColumn("Total Pressure Drop (Pa)", format="%.2f",
                                                                  disabled=True),
    }

    # Render editable table
    edited_df = st.data_editor(
        display_table,
        key="data_editor",
        num_rows="dynamic",
        width='stretch',
        hide_index=True,
        column_config=column_config
    )

    # ------------------- MOVE UP/DOWN BUTTONS -------------------
    st.subheader("🔄 Rearrange Rows")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬆️ Move Selected Rows Up", width='stretch', type="secondary"):
            selected_indices = edited_df[edited_df["Select"] == True].index.tolist()
            if not selected_indices:
                st.warning("Please select rows to move first (use the checkboxes).")
            else:
                # Convert to list for manipulation
                current_data = st.session_state.damper_table.reset_index(drop=True)
                selected_indices = sorted(selected_indices)

                # Move selected rows up
                for idx in selected_indices:
                    if idx > 0 and (idx - 1) not in selected_indices:
                        # Swap current row with the one above
                        current_data.iloc[idx - 1], current_data.iloc[idx] = current_data.iloc[idx].copy(), \
                        current_data.iloc[idx - 1].copy()

                st.session_state.damper_table = current_data.reset_index(drop=True)
                st.success("✅ Selected rows moved up!")
                st.rerun()

    with col2:
        if st.button("⬇️ Move Selected Rows Down", width='stretch', type="secondary"):
            selected_indices = edited_df[edited_df["Select"] == True].index.tolist()
            if not selected_indices:
                st.warning("Please select rows to move first (use the checkboxes).")
            else:
                # Convert to list for manipulation
                current_data = st.session_state.damper_table.reset_index(drop=True)
                selected_indices = sorted(selected_indices, reverse=True)

                # Move selected rows down
                for idx in selected_indices:
                    if idx < len(current_data) - 1 and (idx + 1) not in selected_indices:
                        # Swap current row with the one below
                        current_data.iloc[idx], current_data.iloc[idx + 1] = current_data.iloc[idx + 1].copy(), \
                        current_data.iloc[idx].copy()

                st.session_state.damper_table = current_data.reset_index(drop=True)
                st.success("✅ Selected rows moved down!")
                st.rerun()

    # Handle edits and recalculations
    if not edited_df.equals(display_table):
        for idx in range(len(edited_df)):
            try:
                row = edited_df.iloc[idx]
                w_val = float(row.get("Width (mm)", 0) or 0)
                h_val = float(row.get("Height (mm)", 0) or 0)
                af_val = float(row.get("Airflow (L/s)", 0) or 0)
                prod = row.get("Product", "")
                mod = row.get("Model", "")
                max_w = float(row.get("Max Section Width (mm)", 0) or 0)
                max_h = float(row.get("Max Section Height (mm)", 0) or 0)
                safety_val = float(row.get("Safety Factor (%)", 5.0) or 5.0)

                c_val = get_c_factor_from_backend(prod, mod, max_w, max_h)
                if c_val is None:
                    if prod in st.session_state.PRODUCT_DATA and mod in st.session_state.PRODUCT_DATA[prod]:
                        sizes = st.session_state.PRODUCT_DATA[prod][mod]
                        sorted_sizes = sorted(sizes, key=lambda x: x['width'] * x['height'], reverse=True)
                        if sorted_sizes:
                            max_w = sorted_sizes[0]["width"]
                            max_h = sorted_sizes[0]["height"]
                            c_val = sorted_sizes[0]["c_factor"]
                            edited_df.at[idx, "Max Section Width (mm)"] = max_w
                            edited_df.at[idx, "Max Section Height (mm)"] = max_h

                if c_val:
                    new_result = damper_selection(af_val, w_val, h_val, c_val, max_w, max_h, safety_val)
                    if new_result:
                        for calc_col in new_result:
                            if calc_col in edited_df.columns:
                                edited_df.at[idx, calc_col] = new_result[calc_col]
            except Exception as e:
                st.error(f"Error recalculating row {idx + 1}: {e}")

        # Update session state
        edited_data = edited_df.drop(columns=['Select', 'Sr No'], errors='ignore')
        st.session_state.damper_table = edited_data.reset_index(drop=True)
        st.rerun()

    # Update selected rows for deletion
    if "Select" in edited_df.columns:
        st.session_state.rows_to_delete = edited_df[edited_df["Select"] == True].index.tolist()

    # Delete and Clear functionality
    st.subheader("📤 Table Actions")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🗑️ Delete Selected", width='stretch', type="primary"):
            if st.session_state.rows_to_delete:
                st.session_state.damper_table = st.session_state.damper_table.drop(
                    st.session_state.rows_to_delete).reset_index(drop=True)
                st.session_state.rows_to_delete = []
                st.success("✅ Selected rows deleted successfully!")
                st.rerun()
            else:
                st.warning("Please select rows to delete first.")

    with col2:
        if st.button("🧹 Clear All", width='stretch', type="primary"):
            if not st.session_state.damper_table.empty:
                st.session_state.damper_table = pd.DataFrame()
                st.success("✅ Table cleared!")
                st.rerun()
            else:
                st.info("No data to clear.")

    # Export Settings
    available_columns = [col for col in st.session_state.damper_table.columns if col not in ['Select', 'Sr No']]

    if not st.session_state.export_columns:
        st.session_state.export_columns = available_columns

    selected_columns = st.multiselect(
        "Select columns to export:",
        options=available_columns,
        default=st.session_state.export_columns,
        key="column_selector"
    )

    st.session_state.export_columns = selected_columns

    # Short column mapping
    short_column_mapping = {
        "Sr No": "S.no",
        "Tag No": "Tag",
        "Category": "Category",
        "Product": "Product",
        "Model": "Model",
        "Width (mm)": "w(mm)",
        "Height (mm)": "H(mm)",
        "Airflow (L/s)": "Airflow(l/s)",
        "Safety Factor (%)": "SF(%)",
        "Total Area (m²)": "T_Area(m²)",
        "Velocity (m/s)": "Vel(m/s)",
        "Max Section Width (mm)": "MaxW(mm)",
        "Max Section Height (mm)": "MaxH(mm)",
        "Section Size": "SecSize",
        "Section Area (m²)": "SecArea(m²)",
        "No of Sections": "No_Sec",
        "Section Velocity (m/s)": "SecVel(m/s)",
        "Section Pressure Drop (Pa)": "SecPd",
        "Total Pressure Drop (Pa)": "T_Pd"
    }

    with col3:
        if selected_columns:
            export_data = st.session_state.damper_table[selected_columns]
            export_data_short = export_data.rename(columns=short_column_mapping)
            csv_data = export_data_short.to_csv(index=False)
            st.download_button(
                "💾 Save to CSV",
                csv_data,
                file_name=f"{customer}_{project}_results.csv",
                mime="text/csv",
                width='stretch',
                type="primary"
            )
        else:
            st.button("💾 Save to CSV", disabled=True, width='stretch')

    with col4:
        if selected_columns:
            try:
                export_data = st.session_state.damper_table[selected_columns]
                export_data_short = export_data.rename(columns=short_column_mapping)
                pdf_data = save_table_as_pdf(export_data_short, customer, project, report_date)
                st.download_button(
                    "📄 Save to PDF",
                    data=pdf_data,
                    file_name=f"{customer}_{project}_results.pdf",
                    mime="application/pdf",
                    width='stretch',
                    type="primary"
                )
            except Exception as e:
                st.error(f"Error generating PDF: {e}")
                st.info("Please try saving as CSV instead")
        else:
            st.button("📄 Save to PDF", disabled=True, width='stretch')

else:
    st.info("No data yet. Add manually or upload a CSV/Excel to calculate automatically.")

st.markdown(
    "<div class='footer'>🌀 Pressure Drop Calculation Tool — Central Ventilation Systems</div>",
    unsafe_allow_html=True,
)


# helpers.py
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


def damper_selection(airflow_lps, width_mm, height_mm, c_factor, max_width_mm, max_height_mm,
                     safety_factor_percentage=5.0):
    """Updated with safety factor as percentage input"""
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

        # NEW FORMULA: total_pressure_drop = section_pressure_drop + (total_sections * safety_factor_percentage% * section_pressure_drop)
        safety_factor_decimal = safety_factor_percentage / 100.0
        total_pressure_drop = section_pressure_drop + (total_sections * safety_factor_decimal * section_pressure_drop)

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
    """Generate PDF and return as bytes - FIXED VERSION"""
    try:
        pdf = FPDF(orientation="L", unit="mm", format="A4")
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "Pressure Drop Calculation Tool", ln=True, align="C")
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 8, f"Customer: {customer}", ln=True)
        pdf.cell(0, 8, f"Project: {project}", ln=True)
        pdf.cell(0, 8, f"Date: {report_date}", ln=True)
        pdf.ln(5)

        # Create a copy and reset index
        df_display = df.copy().reset_index(drop=True)

        # Set font for table
        pdf.set_font("Arial", 'B', 8)
        col_width = (pdf.w - 20) / len(df_display.columns)

        # Header row
        for col in df_display.columns:
            pdf.cell(col_width, 8, str(col), 1, 0, "C")
        pdf.ln()

        # Data rows
        pdf.set_font("Arial", '', 7)
        for _, row in df_display.iterrows():
            for col in df_display.columns:
                cell_value = str(row[col]) if pd.notna(row[col]) else ""
                # Truncate long values
                if len(cell_value) > 15:
                    cell_value = cell_value[:12] + "..."
                pdf.cell(col_width, 8, cell_value, 1, 0, "C")
            pdf.ln()

        # Return as bytes
        return pdf.output(dest='S').encode('latin-1')

    except Exception as e:
        st.error(f"PDF generation error: {e}")
        # Return empty bytes if PDF generation fails
        return b""