import streamlit as st
from datetime import date
import pandas as pd

from config import DEFAULT_PRODUCTS
from helpers import damper_selection, get_c_factor_from_backend, save_table_as_pdf
import styles  # Loads CSS automatically

styles.load_styles()
# ------------------- Page Config -------------------
st.set_page_config(
    page_title="Pressure Drop Calculation Tool",
    page_icon="🌀",
    layout="wide"
)

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

st.subheader("📂 Bulk Upload Data (CSV / Excel)")
uploaded_file = st.file_uploader(
    "Upload CSV/Excel with columns: Width (mm), Height (mm), Airflow (L/s), Product, Model, Max Width (mm), Max Height (mm)",
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

                        c_val = get_c_factor_from_backend(product_val, model_val, mw_val, mh_val)

                        if c_val is None:
                            errors.append(
                                f"Row {idx + 1}: No C-factor found for {product_val} - {model_val} with size {mw_val}×{mh_val}mm")
                            continue

                        res = damper_selection(airflow_val, w_val, h_val, c_val, mw_val, mh_val)
                        if res:
                            res["Product"] = product_val
                            res["Model"] = model_val
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

# ------------------- Manual Calculation Section -------------------
st.subheader("Manual Calculation")
col1, col2, col3 = st.columns(3)
with col1:
    product = st.selectbox("Product", ["Select Product"] + list(st.session_state.PRODUCT_DATA.keys()))

model = "Select Model"
selected = "Select Size"
if product != "Select Product":
    with col2:
        model = st.selectbox("Model", ["Select Model"] + list(st.session_state.PRODUCT_DATA[product].keys()))
if model != "Select Model":
    sizes = st.session_state.PRODUCT_DATA[product][model]
    with col3:
        size_options = [f"{s['width']}×{s['height']} mm" for s in sizes]
        selected = st.selectbox("Select Size", ["Select Size"] + size_options)

if selected != "Select Size":
    idx = size_options.index(selected)
    max_width, max_height, c_factor = sizes[idx]["width"], sizes[idx]["height"], sizes[idx]["c_factor"]
else:
    max_width = max_height = c_factor = 0

airflow = st.number_input("Airflow (L/s)", min_value=0.0, value=0.0, step=1.0)
colw, colh = st.columns(2)
with colw:
    width = st.number_input("Width (mm)", min_value=0.0, value=0.0)
with colh:
    height = st.number_input("Height (mm)", min_value=0.0, value=0.0)

width_mm = width
height_mm = height

if width_mm > 0 and height_mm > 0 and airflow > 0 and c_factor > 0:
    preview = damper_selection(airflow, width_mm, height_mm, c_factor, max_width, max_height)
    if preview:
        st.text_input("Total Pressure Drop (Pa)", value=preview["Total Pressure Drop (Pa)"], disabled=True)
else:
    st.info("Enter Width, Height, Airflow and select a valid size to preview calculation.")

if st.button("➕ Add to Table"):
    if product == "Select Product" or model == "Select Model" or selected == "Select Size":
        st.warning("Select product, model and size first.")
    else:
        res = damper_selection(airflow, width_mm, height_mm, c_factor, max_width, max_height)
        if res:
            res["Product"] = product
            res["Model"] = model
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
    if "Select" not in display_table.columns:
        display_table.insert(0, "Select", False)

    # Add serial number
    display_table.insert(0, "Sr No", range(1, len(display_table) + 1))

    # Define column order (including new Max Section columns)
    column_order = [
        "Sr No", "Select", "Product", "Model", "Width (mm)", "Height (mm)",
        "Airflow (L/s)", "Total Area (m²)", "Velocity (m/s)",
        "Max Section Width (mm)", "Max Section Height (mm)", "Section Size",
        "Section Area (m²)", "No of Sections", "Section Velocity (m/s)",
        "Section Pressure Drop (Pa)", "Total Pressure Drop (Pa)"
    ]

    # Reorder columns
    existing_columns = [col for col in column_order if col in display_table.columns]
    display_table = display_table[existing_columns]

    edited_df = st.data_editor(
        display_table,
        key="data_editor",
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True
    )

    # ✅ CRITICAL: Update session state with edited data (excluding temporary columns)
    if not edited_df.empty:
        # Remove temporary columns before saving to session state
        edited_data = edited_df.drop(columns=['Select', 'Sr No'], errors='ignore')
        st.session_state.damper_table = edited_data.reset_index(drop=True)

    if "Select" in edited_df.columns:
        selected_rows = edited_df[edited_df["Select"] == True].index.tolist()
        st.session_state.rows_to_delete = selected_rows

    st.subheader("📤 Export Settings")
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
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    # ✅ DELETE CONFIRMATION DIALOG
    @st.dialog("⚠️ Confirm Deletion")
    def confirm_delete_dialog():
        st.write("Are you sure you want to delete the **selected rows**?")
        colA, colB = st.columns(2)
        with colA:
            if st.button("✅ Yes, Delete", use_container_width=True):
                # Use the current session state data for deletion
                st.session_state.damper_table = st.session_state.damper_table.drop(
                    st.session_state.rows_to_delete
                ).reset_index(drop=True)
                st.session_state.rows_to_delete = []
                st.success("✅ Selected rows deleted successfully!")
                st.rerun()
        with colB:
            if st.button("❌ Cancel", use_container_width=True):
                st.rerun()

    # ✅ CLEAR ALL CONFIRMATION DIALOG
    @st.dialog("⚠️ Confirm Clear All")
    def confirm_clear_dialog():
        st.write("Are you sure you want to **clear the entire table**?")
        st.warning("⚠️ This action cannot be undone.")
        colA, colB = st.columns(2)
        with colA:
            if st.button("✅ Yes, Clear All", use_container_width=True):
                st.session_state.damper_table = pd.DataFrame()
                st.success("✅ Table cleared!")
                st.rerun()
        with colB:
            if st.button("❌ Cancel", use_container_width=True):
                st.rerun()

    with col1:
        if st.button("🗑️ Delete Selected", use_container_width=True):
            if st.session_state.rows_to_delete:
                confirm_delete_dialog()
            else:
                st.warning("Please select rows to delete first.")

    with col2:
        if st.button("🧹 Clear All", use_container_width=True):
            if not st.session_state.damper_table.empty:
                confirm_clear_dialog()
            else:
                st.info("No data to clear.")

    # Define short column names mapping (updated with new columns)
    short_column_mapping = {
        "Sr No": "S.no",
        "Product": "Product",
        "Model": "Model",
        "Width (mm)": "w(mm)",
        "Height (mm)": "H(mm)",
        "Airflow (L/s)": "Airflow(l/s)",
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
            # Use the updated session state data for export
            export_data = st.session_state.damper_table[selected_columns]
            # Apply short column names
            export_data_short = export_data.rename(columns=short_column_mapping)
            csv_data = export_data_short.to_csv(index=False)
            st.download_button(
                "💾 Save to CSV",
                csv_data,
                file_name=f"{customer}_{project}_results.csv",
                mime="text/csv",
                use_container_width=True,
            )
        else:
            st.button("💾 Save to CSV", disabled=True, use_container_width=True)

    with col4:
        if selected_columns:
            # Use the updated session state data for export
            export_data = st.session_state.damper_table[selected_columns]
            # Apply short column names for PDF
            export_data_short = export_data.rename(columns=short_column_mapping)
            pdf_data = save_table_as_pdf(export_data_short, customer, project, report_date)
            st.download_button(
                "📄 Save to PDF",
                pdf_data,
                file_name=f"{customer}_{project}_results.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        else:
            st.button("📄 Save to PDF", disabled=True, use_container_width=True)

else:
    st.info("No data yet. Add manually or upload a CSV/Excel to calculate automatically.")

st.markdown(
    "<div class='footer'>🌀 Pressure Drop Calculation Tool — Central Ventilation Systems</div>",
    unsafe_allow_html=True,
)

