
# # _____________________________________________________________________________________________________________________
# #perfect working code
# # app.py
# import streamlit as st
# from datetime import date
# import pandas as pd
# import base64
# import math
#
# from config import DEFAULT_PRODUCTS, CATEGORIES
# from helpers import damper_selection, get_c_factor_from_backend, save_table_as_pdf
# import styles
#
# # Load CSS/styles
# styles.load_styles()
#
# # ------------------- Page Config -------------------
# st.set_page_config(
#     page_title="Pressure Drop Calculation Tool",
#     page_icon="🌀",
#     layout="wide"
# )
#
#
# # ------------------- Session State Initialization -------------------
# def initialize_session_state():
#     """Initialize all session state variables"""
#     if "PRODUCT_DATA" not in st.session_state:
#         st.session_state.PRODUCT_DATA = DEFAULT_PRODUCTS.copy()
#     if "damper_table" not in st.session_state:
#         st.session_state.damper_table = pd.DataFrame()
#     if "selected_rows" not in st.session_state:
#         st.session_state.selected_rows = set()
#     if "uploaded_filename" not in st.session_state:
#         st.session_state.uploaded_filename = None
#     if "export_columns" not in st.session_state:
#         st.session_state.export_columns = []
#     if "customer" not in st.session_state:
#         st.session_state.customer = ""
#     if "project" not in st.session_state:
#         st.session_state.project = ""
#     if "data_editor_key" not in st.session_state:
#         st.session_state.data_editor_key = 0
#
#
# initialize_session_state()
#
# # ------------------- Header -------------------
# st.markdown(
#     "<div class='top-bar'><h2>🌀 Pressure Drop Calculation Tool</h2></div>",
#     unsafe_allow_html=True
# )
#
# # ------------------- Customer Info -------------------
# col1, col2, col3 = st.columns([2, 2, 1])
# with col1:
#     customer = st.text_input(
#         "Customer Name",
#         value=st.session_state.get("customer", "")
#     )
# with col2:
#     project = st.text_input(
#         "Project Name",
#         value=st.session_state.get("project", "")
#     )
# with col3:
#     report_date = st.date_input("Date", value=date.today())
#
# st.session_state.customer = customer
# st.session_state.project = project
#
# st.markdown("---")
#
#
# # ------------------- Bulk Upload -------------------
# def process_uploaded_file(uploaded_file):
#     """Process uploaded CSV/Excel file and add to table"""
#     try:
#         if uploaded_file.name.lower().endswith(".csv"):
#             try:
#                 df = pd.read_csv(uploaded_file)
#             except Exception:
#                 df = pd.read_csv(uploaded_file, encoding="latin1", on_bad_lines="skip")
#         else:
#             df = pd.read_excel(uploaded_file)
#
#         st.success(f"✅ File '{uploaded_file.name}' uploaded ({len(df)} rows).")
#         st.dataframe(df.head())
#
#         required = [
#             "Width (mm)", "Height (mm)", "Airflow (L/s)",
#             "Product", "Model", "Max Width (mm)", "Max Height (mm)"
#         ]
#         missing = [c for c in required if c not in df.columns]
#
#         if missing:
#             st.warning(f"Missing columns: {', '.join(missing)}")
#             return
#
#         results = []
#         errors = []
#
#         for idx, row in df.iterrows():
#             try:
#                 airflow_val = row.get("Airflow (L/s)", 0)
#                 w_val = row.get("Width (mm)", 0)
#                 h_val = row.get("Height (mm)", 0)
#                 product_val = row.get("Product", "")
#                 model_val = row.get("Model", "")
#                 mw_val = row.get("Max Width (mm)", 0)
#                 mh_val = row.get("Max Height (mm)", 0)
#                 tag_no = row.get("Tag No", f"Tag_{idx + 1}")
#                 category_val = row.get("Category", "Life Safety Damper")
#                 safety_val = row.get("Safety Factor (%)", 5.0)
#
#                 c_val = get_c_factor_from_backend(product_val, model_val, mw_val, mh_val)
#
#                 if c_val is None:
#                     errors.append(
#                         f"Row {idx + 1}: No C-factor found for {product_val} - {model_val} with size {mw_val}×{mh_val}mm"
#                     )
#                     continue
#
#                 res = damper_selection(airflow_val, w_val, h_val, c_val, mw_val, mh_val, safety_val)
#                 if res:
#                     res["Category"] = category_val
#                     res["Product"] = product_val
#                     res["Model"] = model_val
#                     res["Tag No"] = tag_no
#                     res["Safety Factor (%)"] = float(safety_val)
#                     res["Max Size"] = f"{mw_val}×{mh_val}"
#                     results.append(res)
#
#             except Exception as e:
#                 errors.append(f"Row {idx + 1}: {str(e)}")
#
#         if errors:
#             st.warning(f"⚠️ {len(errors)} errors found during processing:")
#             for error in errors:
#                 st.write(f"• {error}")
#
#         if results:
#             bulk_df = pd.DataFrame(results)
#             st.session_state.damper_table = pd.concat(
#                 [st.session_state.damper_table, bulk_df],
#                 ignore_index=True
#             )
#             st.session_state.uploaded_filename = uploaded_file.name
#             st.session_state.data_editor_key += 1
#             st.success(f"✅ Calculated and added {len(results)} rows.")
#         else:
#             st.info("No valid calculation results produced from the file.")
#
#     except Exception as e:
#         st.error(f"Upload error: {e}")
#
#
# st.subheader("📂 Bulk Upload Data (CSV / Excel)")
# uploaded_file = st.file_uploader(
#     "Upload CSV/Excel with columns: Category, Width (mm), Height (mm), Airflow (L/s), Product, Model, Max Width (mm), Max Height (mm), Tag No, Safety Factor (%)",
#     type=["csv", "xlsx", "xls"]
# )
#
# if uploaded_file is not None:
#     if uploaded_file.name != st.session_state.uploaded_filename:
#         process_uploaded_file(uploaded_file)
#     else:
#         st.info(f"File '{uploaded_file.name}' already processed. Upload another file to add more rows.")
#
# st.markdown("---")
#
#
# # ------------------- Manual Calculation -------------------
# def handle_manual_calculation():
#     """Handle manual calculation and addition to table"""
#     st.subheader("Manual Calculation")
#
#     # First line: Category, Product, Model, Size
#     col1, col2, col3, col4 = st.columns(4)
#
#     with col1:
#         category = st.selectbox("Category", CATEGORIES, key="category_select")
#
#     with col2:
#         product = st.selectbox(
#             "Product",
#             ["Select Product"] + list(st.session_state.PRODUCT_DATA.keys()),
#             key="product_select"
#         )
#
#     model = "Select Model"
#     selected = "Select Size"
#     max_width = max_height = c_factor = 0
#     max_size_str = ""
#
#     if product != "Select Product":
#         with col3:
#             model = st.selectbox(
#                 "Model",
#                 ["Select Model"] + list(st.session_state.PRODUCT_DATA[product].keys()),
#                 key="model_select"
#             )
#
#     if model != "Select Model":
#         sizes = st.session_state.PRODUCT_DATA[product][model]
#         sorted_sizes = sorted(sizes, key=lambda x: x['width'] * x['height'], reverse=True)
#         size_options = [f"{s['width']}×{s['height']}" for s in sorted_sizes]
#
#         with col4:
#             selected = st.selectbox(
#                 "Max Size",
#                 options=["Select Size"] + size_options,
#                 key="size_select"
#             )
#
#         if selected != "Select Size":
#             try:
#                 max_width, max_height = map(int, selected.split("×"))
#                 for size_data in sorted_sizes:
#                     if size_data["width"] == max_width and size_data["height"] == max_height:
#                         c_factor = size_data["c_factor"]
#                         break
#                 max_size_str = selected
#             except ValueError:
#                 st.error("Invalid size format. Please select a valid size.")
#
#     # Second line: Tag, Airflow, Width, Height, Safety Factor
#     col1, col2, col3, col4, col5 = st.columns(5)
#
#     with col1:
#         tag_no = st.text_input("Tag No", value="", placeholder="Enter tag number", key="tag_input")
#
#     with col2:
#         airflow = st.number_input("Airflow (L/s)", min_value=0.0, value=0.0, step=1.0, key="airflow_input")
#
#     with col3:
#         width = st.number_input("Width (mm)", min_value=0.0, value=0.0, key="width_input")
#
#     with col4:
#         height = st.number_input("Height (mm)", min_value=0.0, value=0.0, key="height_input")
#
#     with col5:
#         safety_factor_local = st.number_input(
#             "Safety Factor (%)",
#             min_value=0.0,
#             value=5.0,
#             step=0.5,
#             key="safety_factor_local"
#         )
#
#     width_mm = width
#     height_mm = height
#
#     # Third line: Display calculated values
#     if width_mm > 0 and height_mm > 0 and airflow > 0 and c_factor > 0:
#         preview = damper_selection(airflow, width_mm, height_mm, c_factor, max_width, max_height, safety_factor_local)
#         if preview:
#             col1, col2 = st.columns(2)
#             with col1:
#                 st.text_input("Total Velocity (m/s)", value=preview["Velocity (m/s)"], disabled=True)
#             with col2:
#                 st.text_input("Total Pressure Drop (Pa)", value=preview["Total Pressure Drop (Pa)"], disabled=True)
#     else:
#         st.info("Enter Width, Height, Airflow and select a valid size to preview calculation.")
#
#     if st.button("➕ Add to Table", width='stretch'):
#         if product == "Select Product" or model == "Select Model" or selected == "Select Size":
#             st.warning("Select product, model and size first.")
#         elif not tag_no:
#             st.warning("Please enter a Tag No.")
#         else:
#             res = damper_selection(airflow, width_mm, height_mm, c_factor, max_width, max_height, safety_factor_local)
#             if res:
#                 res["Category"] = category
#                 res["Product"] = product
#                 res["Model"] = model
#                 res["Tag No"] = tag_no
#                 res["Safety Factor (%)"] = float(safety_factor_local)
#                 res["Max Size"] = max_size_str
#
#                 st.session_state.damper_table = pd.concat(
#                     [st.session_state.damper_table, pd.DataFrame([res])],
#                     ignore_index=True
#                 )
#                 st.session_state.data_editor_key += 1
#                 st.success("✅ Manual calculation added to table.")
#                 st.rerun()
#
#
# handle_manual_calculation()
# st.markdown("---")
#
#
# # ------------------- Project Summary -------------------
# def get_all_max_sizes():
#     """Get all possible max sizes from product data"""
#     all_max_sizes = set()
#     for product_name in st.session_state.PRODUCT_DATA.keys():
#         for model_name in st.session_state.PRODUCT_DATA[product_name].keys():
#             sizes = st.session_state.PRODUCT_DATA[product_name][model_name]
#             for size in sizes:
#                 all_max_sizes.add(f"{size['width']}×{size['height']}")
#
#     return sorted(list(all_max_sizes), key=lambda x: (int(x.split('×')[0]), int(x.split('×')[1])))
#
#
# def handle_table_edits(edited_df):
#     """Handle edits and recalculations in the table"""
#     for idx in range(len(edited_df)):
#         try:
#             row = edited_df.iloc[idx]
#             w_val = float(row.get("Width (mm)", 0) or 0)
#             h_val = float(row.get("Height (mm)", 0) or 0)
#             af_val = float(row.get("Airflow (L/s)", 0) or 0)
#             prod = row.get("Product", "")
#             mod = row.get("Model", "")
#             max_size_str = row.get("Max Size", "")
#             safety_val = float(row.get("Safety Factor (%)", 5.0) or 5.0)
#
#             # Parse Max Size and get c_factor
#             max_w = max_h = 0
#             c_val = None
#
#             if max_size_str and "×" in max_size_str:
#                 try:
#                     max_w, max_h = map(int, max_size_str.split("×"))
#                     c_val = get_c_factor_from_backend(prod, mod, max_w, max_h)
#                 except ValueError:
#                     st.error(f"Row {idx + 1}: Invalid Max Size format. Use 'width×height'")
#                     continue
#
#             # If c_factor not found, try to get default from product data
#             if not c_val and prod in st.session_state.PRODUCT_DATA and mod in st.session_state.PRODUCT_DATA[prod]:
#                 sizes = st.session_state.PRODUCT_DATA[prod][mod]
#                 if sizes:
#                     default_size = sizes[0]
#                     max_w = default_size["width"]
#                     max_h = default_size["height"]
#                     c_val = default_size["c_factor"]
#                     edited_df.at[idx, "Max Size"] = f"{max_w}×{max_h}"
#
#             if c_val:
#                 new_result = damper_selection(af_val, w_val, h_val, c_val, max_w, max_h, safety_val)
#                 if new_result:
#                     for calc_col in new_result:
#                         if calc_col in edited_df.columns:
#                             edited_df.at[idx, calc_col] = new_result[calc_col]
#             else:
#                 st.error(f"Row {idx + 1}: Could not find C-factor for {prod} - {mod} with size {max_size_str}")
#
#         except Exception as e:
#             st.error(f"Error recalculating row {idx + 1}: {str(e)}")
#
#     return edited_df
#
#
# def handle_row_movement(direction, selected_indices):
#     """Handle moving rows up or down"""
#     if not selected_indices:
#         st.warning("Please select rows to move first (use the checkboxes).")
#         return False
#
#     current_data = st.session_state.damper_table.reset_index(drop=True)
#
#     if direction == "up":
#         selected_indices = sorted(selected_indices)
#         for idx in selected_indices:
#             if idx > 0 and (idx - 1) not in selected_indices:
#                 current_data.iloc[idx - 1], current_data.iloc[idx] = (
#                     current_data.iloc[idx].copy(),
#                     current_data.iloc[idx - 1].copy()
#                 )
#     else:  # down
#         selected_indices = sorted(selected_indices, reverse=True)
#         for idx in selected_indices:
#             if idx < len(current_data) - 1 and (idx + 1) not in selected_indices:
#                 current_data.iloc[idx], current_data.iloc[idx + 1] = (
#                     current_data.iloc[idx + 1].copy(),
#                     current_data.iloc[idx].copy()
#                 )
#
#     st.session_state.damper_table = current_data.reset_index(drop=True)
#     st.session_state.data_editor_key += 1
#     return True
#
#
# def prepare_display_table():
#     """Prepare the display table with all necessary columns"""
#     display_table = st.session_state.damper_table.copy()
#
#     # Ensure required columns exist
#     if "Safety Factor (%)" not in display_table.columns:
#         display_table["Safety Factor (%)"] = 5.0
#     else:
#         display_table["Safety Factor (%)"] = display_table["Safety Factor (%)"].fillna(5.0)
#
#     if "Max Size" not in display_table.columns:
#         display_table["Max Size"] = ""
#     else:
#         display_table["Max Size"] = display_table["Max Size"].fillna("")
#
#     # Add helper columns
#     display_table.insert(0, "Sr No", [str(i) for i in range(1, len(display_table) + 1)])
#
#     # Initialize Select column based on session state
#     display_table.insert(1, "Select", False)
#     if st.session_state.selected_rows:
#         for idx in st.session_state.selected_rows:
#             if idx < len(display_table):
#                 display_table.at[idx, "Select"] = True
#
#     # Define column order
#     column_order = [
#         "Sr No", "Select", "Tag No", "Category", "Product", "Model", "Max Size",
#         "Width (mm)", "Height (mm)", "Airflow (L/s)", "Safety Factor (%)",
#         "Total Area (m²)", "Velocity (m/s)", "Section Size", "Section Area (m²)", "No of Sections",
#         "Section Velocity (m/s)", "Section Pressure Drop (Pa)", "Total Pressure Drop (Pa)"
#     ]
#
#     existing_columns = [col for col in column_order if col in display_table.columns]
#     return display_table[existing_columns]
#
#
# def setup_column_config():
#     """Setup column configuration for data editor"""
#     all_products = list(st.session_state.PRODUCT_DATA.keys())
#
#     all_models = []
#     for product_name in all_products:
#         for model_name in st.session_state.PRODUCT_DATA[product_name].keys():
#             all_models.append(model_name)
#     all_models = list(set(all_models))
#
#     all_max_sizes_list = get_all_max_sizes()
#
#     return {
#         "Sr No": st.column_config.TextColumn("Sr No", disabled=True),
#         "Select": st.column_config.CheckboxColumn("Select"),
#         "Tag No": st.column_config.TextColumn("Tag No"),
#         "Category": st.column_config.SelectboxColumn("Category", options=CATEGORIES),
#         "Product": st.column_config.SelectboxColumn("Product", options=all_products),
#         "Model": st.column_config.SelectboxColumn("Model", options=all_models),
#         "Max Size": st.column_config.SelectboxColumn("Max Size", options=all_max_sizes_list),
#         "Width (mm)": st.column_config.NumberColumn("Width (mm)", format="%d"),
#         "Height (mm)": st.column_config.NumberColumn("Height (mm)", format="%d"),
#         "Airflow (L/s)": st.column_config.NumberColumn("Airflow (L/s)", format="%.1f"),
#         "Safety Factor (%)": st.column_config.NumberColumn("Safety Factor (%)", format="%.2f"),
#         "Total Area (m²)": st.column_config.NumberColumn("Total Area (m²)", format="%.3f", disabled=True),
#         "Velocity (m/s)": st.column_config.NumberColumn("Velocity (m/s)", format="%.2f", disabled=True),
#         "Section Size": st.column_config.TextColumn("Section Size", disabled=True),
#         "Section Area (m²)": st.column_config.NumberColumn("Section Area (m²)", format="%.3f", disabled=True),
#         "No of Sections": st.column_config.NumberColumn("No of Sections", format="%d", disabled=True),
#         "Section Velocity (m/s)": st.column_config.NumberColumn("Section Velocity (m/s)", format="%.2f", disabled=True),
#         "Section Pressure Drop (Pa)": st.column_config.NumberColumn("Section Pressure Drop (Pa)", format="%.2f",
#                                                                     disabled=True),
#         "Total Pressure Drop (Pa)": st.column_config.NumberColumn("Total Pressure Drop (Pa)", format="%.2f",
#                                                                   disabled=True),
#     }
#
#
# def get_export_data_in_order(selected_columns):
#     """Prepare export data in the specific order required"""
#     # Define the desired column order for export
#     export_order = [
#         "Tag No", "Category", "Product", "Model", "Max Size", "Safety Factor (%)",
#         "Width (mm)", "Height (mm)", "Airflow (L/s)", "Total Area (m²)", "Velocity (m/s)",
#         "Section Size", "Section Area (m²)", "No of Sections", "Section Velocity (m/s)",
#         "Section Pressure Drop (Pa)", "Total Pressure Drop (Pa)"
#     ]
#
#     # Filter only selected and available columns in the desired order
#     ordered_columns = [col for col in export_order if
#                        col in selected_columns and col in st.session_state.damper_table.columns]
#
#     # Get the data with only selected columns in the desired order
#     export_data = st.session_state.damper_table[ordered_columns].copy()
#
#     # Add Sr No at the beginning
#     export_data.insert(0, "Sr No", [str(i) for i in range(1, len(export_data) + 1)])
#
#     return export_data
#
#
# def handle_table_actions(selected_indices):
#     """Handle all table actions (delete, clear, export)"""
#     st.subheader("📤 Table Actions")
#
#     # Action buttons in a single row - all 6 buttons together
#     col1, col2, col3, col4, col5, col6 = st.columns(6)
#
#     with col1:
#         move_up = st.button("⬆️ Move Up", width='stretch', type="secondary")
#
#     with col2:
#         move_down = st.button("⬇️ Move Down", width='stretch', type="secondary")
#
#     with col3:
#         delete = st.button("🗑️ Delete", width='stretch', type="primary")
#
#     with col4:
#         clear = st.button("🧹 Clear", width='stretch', type="primary")
#
#     # Short column mapping with exact names as requested
#     short_column_mapping = {
#         "Sr No": "S.no",
#         "Tag No": "Tag",
#         "Category": "Category",
#         "Product": "Product",
#         "Model": "Model",
#         "Max Size": "MaxSize",
#         "Safety Factor (%)": "SF(%)",
#         "Width (mm)": "w(mm)",
#         "Height (mm)": "H(mm)",
#         "Airflow (L/s)": "Airflow(l/s)",
#         "Total Area (m²)": "T_Area(m²)",
#         "Velocity (m/s)": "Vel(m/s)",
#         "Section Size": "SecSize",
#         "Section Area (m²)": "SecArea(m²)",
#         "No of Sections": "No_Sec",
#         "Section Velocity (m/s)": "SecVel(m/s)",
#         "Section Pressure Drop (Pa)": "SecPd",
#         "Total Pressure Drop (Pa)": "T_Pd"
#     }
#
#     # Get available columns for export (excluding helper columns)
#     available_columns = [col for col in st.session_state.damper_table.columns if col not in ['Select', 'Sr No']]
#
#     # Initialize export columns if not set or if table has changed
#     if not st.session_state.export_columns or len(st.session_state.export_columns) == 0:
#         st.session_state.export_columns = available_columns
#
#     # Always show CSV and PDF buttons when there's data, just disable if no columns selected
#     with col5:
#         if not st.session_state.damper_table.empty:
#             # Always show the CSV button, just disable if no columns selected
#             export_data = get_export_data_in_order(st.session_state.export_columns)
#             export_data_short = export_data.rename(columns=short_column_mapping)
#             csv_data = export_data_short.to_csv(index=False)
#
#             st.download_button(
#                 "💾 Save CSV",
#                 csv_data,
#                 file_name=f"{customer}_{project}_results.csv",
#                 mime="text/csv",
#                 width='stretch',
#                 type="primary",
#                 disabled=len(st.session_state.export_columns) == 0
#             )
#         else:
#             st.button("💾 Save CSV", disabled=True, width='stretch')
#
#     with col6:
#         if not st.session_state.damper_table.empty:
#             try:
#                 # Always show the PDF button, just disable if no columns selected
#                 export_data = get_export_data_in_order(st.session_state.export_columns)
#                 export_data_short = export_data.rename(columns=short_column_mapping)
#                 pdf_bytes = save_table_as_pdf(export_data_short, customer, project, report_date)
#
#                 if pdf_bytes and len(pdf_bytes) > 0:
#                     st.download_button(
#                         "📄 Save PDF",
#                         data=pdf_bytes,
#                         file_name=f"{customer}_{project}_results.pdf",
#                         mime="application/pdf",
#                         width='stretch',
#                         type="primary",
#                         key=f"pdf_download_{st.session_state.data_editor_key}",
#                         disabled=len(st.session_state.export_columns) == 0
#                     )
#                 else:
#                     st.error("PDF generation failed - no data received")
#             except Exception as e:
#                 st.error(f"Error generating PDF: {e}")
#         else:
#             st.button("📄 Save PDF", disabled=True, width='stretch')
#
#     # Handle button actions after defining all buttons
#     if move_up:
#         if handle_row_movement("up", selected_indices):
#             st.success("✅ Selected rows moved up!")
#             st.rerun()
#
#     if move_down:
#         if handle_row_movement("down", selected_indices):
#             st.success("✅ Selected rows moved down!")
#             st.rerun()
#
#     if delete:
#         if selected_indices:
#             new_table = st.session_state.damper_table.drop(selected_indices).reset_index(drop=True)
#             st.session_state.damper_table = new_table
#             st.session_state.selected_rows = set()
#             st.session_state.data_editor_key += 1
#             st.success("✅ Selected rows deleted successfully!")
#             st.rerun()
#         else:
#             st.warning("Please select rows to delete first.")
#
#     if clear:
#         if not st.session_state.damper_table.empty:
#             st.session_state.damper_table = pd.DataFrame()
#             st.session_state.selected_rows = set()
#             st.session_state.data_editor_key += 1
#             st.success("✅ Table cleared!")
#             st.rerun()
#         else:
#             st.info("No data to clear.")
#
#     # Column selection for export - placed below the table action buttons, spanning full width
#     if not st.session_state.damper_table.empty:
#         st.markdown("---")
#         st.subheader("📊 Export Settings")
#
#         # Column selection for export - full width
#         selected_columns = st.multiselect(
#             "Select columns to export:",
#             options=available_columns,
#             default=st.session_state.export_columns,
#             key="column_selector"
#         )
#
#         st.session_state.export_columns = selected_columns
#
#
# # Main Project Summary Section
# st.subheader("📊 Project Summary")
#
# if not st.session_state.damper_table.empty:
#     st.write(f"**Customer:** {customer} | **Project:** {project} | **Date:** {report_date}")
#
#     # Prepare and display the table
#     display_table = prepare_display_table()
#     column_config = setup_column_config()
#
#     # Render editable table with a unique key to force refresh
#     edited_df = st.data_editor(
#         display_table,
#         key=f"data_editor_{st.session_state.data_editor_key}",
#         num_rows="dynamic",
#         width='stretch',
#         hide_index=True,
#         column_config=column_config
#     )
#
#     # Update selected rows from the edited DataFrame
#     if "Select" in edited_df.columns:
#         new_selected_rows = set()
#         for idx, row in edited_df.iterrows():
#             if row.get("Select", False):
#                 new_selected_rows.add(idx)
#
#         # Only update if selection changed to avoid unnecessary reruns
#         if new_selected_rows != st.session_state.selected_rows:
#             st.session_state.selected_rows = new_selected_rows
#
#     # Handle edits and recalculations (only for non-select columns)
#     if not edited_df.equals(display_table):
#         # Check if changes are only in Select column
#         non_select_columns = [col for col in edited_df.columns if col != "Select"]
#         display_non_select = display_table[non_select_columns]
#         edited_non_select = edited_df[non_select_columns]
#
#         if not edited_non_select.equals(display_non_select):
#             edited_df = handle_table_edits(edited_df)
#             edited_data = edited_df.drop(columns=['Select', 'Sr No'], errors='ignore')
#             st.session_state.damper_table = edited_data.reset_index(drop=True)
#             st.session_state.data_editor_key += 1
#             st.rerun()
#
#     # Handle table actions
#     handle_table_actions(list(st.session_state.selected_rows))
#
# else:
#     st.info("No data yet. Add manually or upload a CSV/Excel to calculate automatically.")
#
# # ------------------- Footer -------------------
# st.markdown("---")
# st.markdown(
#     "<div class='footer'>🌀 Pressure Drop Calculation Tool — Central Ventilation Systems</div>",
#     unsafe_allow_html=True,
# )


# app.py
# app.py
import streamlit as st
from datetime import date
import pandas as pd
import base64
import math

from config import DEFAULT_PRODUCTS, CATEGORIES
from helpers import damper_selection, get_c_factor_from_backend, save_table_as_pdf
import styles

# Load CSS/styles
styles.load_styles()

# ------------------- Page Config -------------------
st.set_page_config(
    page_title="Pressure Drop Calculation Tool",
    page_icon="🌀",
    layout="wide"
)


# ------------------- Session State Initialization -------------------
def initialize_session_state():
    """Initialize all session state variables"""
    if "PRODUCT_DATA" not in st.session_state:
        st.session_state.PRODUCT_DATA = DEFAULT_PRODUCTS.copy()
    if "damper_table" not in st.session_state:
        st.session_state.damper_table = pd.DataFrame()
    if "selected_rows" not in st.session_state:
        st.session_state.selected_rows = set()
    if "uploaded_filename" not in st.session_state:
        st.session_state.uploaded_filename = None
    if "export_columns" not in st.session_state:
        st.session_state.export_columns = []
    if "customer" not in st.session_state:
        st.session_state.customer = ""
    if "project" not in st.session_state:
        st.session_state.project = ""
    if "data_editor_key" not in st.session_state:
        st.session_state.data_editor_key = 0


initialize_session_state()

# ------------------- Header -------------------
st.markdown(
    "<div class='top-bar'><h2>🌀 Pressure Drop Calculation Tool</h2></div>",
    unsafe_allow_html=True
)

# ------------------- Customer Info -------------------
col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    customer = st.text_input(
        "Customer Name",
        value=st.session_state.get("customer", "")
    )
with col2:
    project = st.text_input(
        "Project Name",
        value=st.session_state.get("project", "")
    )
with col3:
    report_date = st.date_input("Date", value=date.today())

st.session_state.customer = customer
st.session_state.project = project

st.markdown("---")


# ------------------- Bulk Upload -------------------
def process_uploaded_file(uploaded_file):
    """Process uploaded CSV/Excel file and add to table"""
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

        # Updated required columns with multiple alternative names
        required = [
            ["Tag", "tag"],  # Tag column alternatives
            ["Width (mm)", "W(mm)", "w_mm"],  # Width column alternatives
            ["Height (mm)", "H(mm)", "H_mm"],  # Height column alternatives
            ["Airflow (L/s)", "Airflow(l/s)"],  # Airflow column alternatives
            ["Product", "product_name"],  # Product column alternatives
            ["Model", "model"],  # Model column alternatives
            ["MaxSize", "maxsize"],  # MaxSize column alternatives
            ["Safety Factor", "SF(%)", "Safety Factor (%)"]  # Safety Factor alternatives
        ]

        # Check for missing columns and find which alternatives exist
        missing_columns = []
        column_mapping = {}

        for column_alternatives in required:
            found = False
            standard_name = column_alternatives[0]  # Use first name as standard

            # Check if any of the alternative names exists in the dataframe
            for alt_name in column_alternatives:
                if alt_name in df.columns:
                    column_mapping[standard_name] = alt_name
                    found = True
                    break

            if not found:
                missing_columns.append(standard_name)

        if missing_columns:
            st.warning(f"Missing required columns: {', '.join(missing_columns)}")
            st.info("Required columns (accepts any of these names):")
            for column_alternatives in required:
                st.write(f"• {column_alternatives[0]} (can be named as: {', '.join(column_alternatives)})")
            return

        # Create a standardized dataframe with consistent column names
        standardized_df = df.copy()

        # Rename columns to standard names if they use alternative names
        for standard_name, actual_name in column_mapping.items():
            if actual_name != standard_name and standard_name not in standardized_df.columns:
                standardized_df = standardized_df.rename(columns={actual_name: standard_name})

        results = []
        errors = []

        for idx, row in standardized_df.iterrows():
            try:
                # Extract values using standard column names
                tag_no = row.get("Tag", f"Tag_{idx + 1}")
                w_val = row.get("Width (mm)", 0)
                h_val = row.get("Height (mm)", 0)
                airflow_val = row.get("Airflow (L/s)", 0)
                product_val = row.get("Product", "")
                model_val = row.get("Model", "")
                max_size_str = row.get("MaxSize", "")
                safety_val = row.get("Safety Factor", 0)

                # Parse MaxSize string (format: "300×300")
                if max_size_str and "×" in max_size_str:
                    try:
                        mw_val, mh_val = map(int, max_size_str.split("×"))
                    except ValueError:
                        errors.append(f"Row {idx + 1}: Invalid MaxSize format. Use 'width×height' like '300×300'")
                        continue
                else:
                    errors.append(f"Row {idx + 1}: MaxSize is required and should be in format 'width×height'")
                    continue

                # Get category (optional, default to Life Safety Damper)
                category_val = row.get("Category", "Life Safety Damper")

                c_val = get_c_factor_from_backend(product_val, model_val, mw_val, mh_val)

                if c_val is None:
                    errors.append(
                        f"Row {idx + 1}: No C-factor found for {product_val} - {model_val} with size {mw_val}×{mh_val}mm"
                    )
                    continue

                res = damper_selection(airflow_val, w_val, h_val, c_val, mw_val, mh_val, safety_val)
                if res:
                    res["Category"] = category_val
                    res["Product"] = product_val
                    res["Model"] = model_val
                    res["Tag No"] = tag_no
                    res["Safety Factor (%)"] = float(safety_val)
                    res["Max Size"] = f"{mw_val}×{mh_val}"
                    results.append(res)

            except Exception as e:
                errors.append(f"Row {idx + 1}: {str(e)}")

        if errors:
            st.warning(f"⚠️ {len(errors)} errors found during processing:")
            for error in errors:
                st.write(f"• {error}")

        if results:
            bulk_df = pd.DataFrame(results)
            st.session_state.damper_table = pd.concat(
                [st.session_state.damper_table, bulk_df],
                ignore_index=True
            )
            st.session_state.uploaded_filename = uploaded_file.name
            st.session_state.data_editor_key += 1
            st.success(f"✅ Calculated and added {len(results)} rows.")

            # Show which column names were used
            st.info("📋 Column mapping used:")
            for standard_name, actual_name in column_mapping.items():
                st.write(f"• {actual_name} → {standard_name}")
        else:
            st.info("No valid calculation results produced from the file.")

    except Exception as e:
        st.error(f"Upload error: {e}")


st.subheader("📂 Bulk Upload Data (CSV / Excel)")
uploaded_file = st.file_uploader(
    "Upload CSV/Excel with required columns: Tag, Width (mm), Height (mm), Airflow (L/s), Product, Model, MaxSize, Safety Factor",
    type=["csv", "xlsx", "xls"],
    help="Accepted column names:\n"
         "• Tag: 'Tag' or 'tag'\n"
         "• Width: 'Width (mm)', 'W(mm)', or 'w_mm'\n"
         "• Height: 'Height (mm)', 'H(mm)', or 'H_mm'\n"
         "• Airflow: 'Airflow (L/s)' or 'Airflow(l/s)'\n"
         "• Product: 'Product' or 'product_name'\n"
         "• Model: 'Model' or 'model'\n"
         "• MaxSize: 'MaxSize' or 'maxsize'\n"
         "• Safety Factor: 'Safety Factor', 'SF(%)', or 'Safety Factor (%)'"
)

if uploaded_file is not None:
    if uploaded_file.name != st.session_state.uploaded_filename:
        process_uploaded_file(uploaded_file)
    else:
        st.info(f"File '{uploaded_file.name}' already processed. Upload another file to add more rows.")

st.markdown("---")


# ------------------- Manual Calculation -------------------
def handle_manual_calculation():
    """Handle manual calculation and addition to table"""
    st.subheader("Manual Calculation")

    # First line: Category, Product, Model, Size
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        category = st.selectbox("Category", CATEGORIES, key="category_select")

    with col2:
        product = st.selectbox(
            "Product",
            ["Select Product"] + list(st.session_state.PRODUCT_DATA.keys()),
            key="product_select"
        )

    model = "Select Model"
    selected = "Select Size"
    max_width = max_height = c_factor = 0
    max_size_str = ""

    if product != "Select Product":
        with col3:
            model = st.selectbox(
                "Model",
                ["Select Model"] + list(st.session_state.PRODUCT_DATA[product].keys()),
                key="model_select"
            )

    if model != "Select Model":
        sizes = st.session_state.PRODUCT_DATA[product][model]
        sorted_sizes = sorted(sizes, key=lambda x: x['width'] * x['height'], reverse=True)
        size_options = [f"{s['width']}×{s['height']}" for s in sorted_sizes]

        with col4:
            selected = st.selectbox(
                "Max Size",
                options=["Select Size"] + size_options,
                key="size_select"
            )

        if selected != "Select Size":
            try:
                max_width, max_height = map(int, selected.split("×"))
                for size_data in sorted_sizes:
                    if size_data["width"] == max_width and size_data["height"] == max_height:
                        c_factor = size_data["c_factor"]
                        break
                max_size_str = selected
            except ValueError:
                st.error("Invalid size format. Please select a valid size.")

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
        # Changed default from 5.0 to 0.0
        safety_factor_local = st.number_input(
            "Safety Factor (%)",
            min_value=0.0,
            value=0.0,  # Changed from 5.0 to 0.0
            step=0.5,
            key="safety_factor_local"
        )

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

    if st.button("➕ Add to Table", use_container_width=True):
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
                res["Max Size"] = max_size_str

                st.session_state.damper_table = pd.concat(
                    [st.session_state.damper_table, pd.DataFrame([res])],
                    ignore_index=True
                )
                st.session_state.data_editor_key += 1
                st.success("✅ Manual calculation added to table.")
                st.rerun()


handle_manual_calculation()
st.markdown("---")


# ------------------- Project Summary -------------------
def get_all_max_sizes():
    """Get all possible max sizes from product data"""
    all_max_sizes = set()
    for product_name in st.session_state.PRODUCT_DATA.keys():
        for model_name in st.session_state.PRODUCT_DATA[product_name].keys():
            sizes = st.session_state.PRODUCT_DATA[product_name][model_name]
            for size in sizes:
                all_max_sizes.add(f"{size['width']}×{size['height']}")

    return sorted(list(all_max_sizes), key=lambda x: (int(x.split('×')[0]), int(x.split('×')[1])))


def handle_table_edits(edited_df):
    """Handle edits and recalculations in the table"""
    for idx in range(len(edited_df)):
        try:
            row = edited_df.iloc[idx]
            w_val = float(row.get("Width (mm)", 0) or 0)
            h_val = float(row.get("Height (mm)", 0) or 0)
            af_val = float(row.get("Airflow (L/s)", 0) or 0)
            prod = row.get("Product", "")
            mod = row.get("Model", "")
            max_size_str = row.get("Max Size", "")
            # Changed default from 5.0 to 0.0
            safety_val = float(row.get("Safety Factor (%)", 0.0) or 0.0)

            # Parse Max Size and get c_factor
            max_w = max_h = 0
            c_val = None

            if max_size_str and "×" in max_size_str:
                try:
                    max_w, max_h = map(int, max_size_str.split("×"))
                    c_val = get_c_factor_from_backend(prod, mod, max_w, max_h)
                except ValueError:
                    st.error(f"Row {idx + 1}: Invalid Max Size format. Use 'width×height'")
                    continue

            # If c_factor not found, try to get default from product data
            if not c_val and prod in st.session_state.PRODUCT_DATA and mod in st.session_state.PRODUCT_DATA[prod]:
                sizes = st.session_state.PRODUCT_DATA[prod][mod]
                if sizes:
                    default_size = sizes[0]
                    max_w = default_size["width"]
                    max_h = default_size["height"]
                    c_val = default_size["c_factor"]
                    edited_df.at[idx, "Max Size"] = f"{max_w}×{max_h}"

            if c_val:
                new_result = damper_selection(af_val, w_val, h_val, c_val, max_w, max_h, safety_val)
                if new_result:
                    for calc_col in new_result:
                        if calc_col in edited_df.columns:
                            edited_df.at[idx, calc_col] = new_result[calc_col]
            else:
                st.error(f"Row {idx + 1}: Could not find C-factor for {prod} - {mod} with size {max_size_str}")

        except Exception as e:
            st.error(f"Error recalculating row {idx + 1}: {str(e)}")

    return edited_df


def handle_row_movement(direction, selected_indices):
    """Handle moving rows up or down"""
    if not selected_indices:
        st.warning("Please select rows to move first (use the checkboxes).")
        return False

    current_data = st.session_state.damper_table.reset_index(drop=True)

    if direction == "up":
        selected_indices = sorted(selected_indices)
        for idx in selected_indices:
            if idx > 0 and (idx - 1) not in selected_indices:
                current_data.iloc[idx - 1], current_data.iloc[idx] = (
                    current_data.iloc[idx].copy(),
                    current_data.iloc[idx - 1].copy()
                )
    else:  # down
        selected_indices = sorted(selected_indices, reverse=True)
        for idx in selected_indices:
            if idx < len(current_data) - 1 and (idx + 1) not in selected_indices:
                current_data.iloc[idx], current_data.iloc[idx + 1] = (
                    current_data.iloc[idx + 1].copy(),
                    current_data.iloc[idx].copy()
                )

    st.session_state.damper_table = current_data.reset_index(drop=True)
    st.session_state.data_editor_key += 1
    return True


def prepare_display_table():
    """Prepare the display table with all necessary columns"""
    display_table = st.session_state.damper_table.copy()

    # Ensure required columns exist
    if "Safety Factor (%)" not in display_table.columns:
        # Changed default from 5.0 to 0.0
        display_table["Safety Factor (%)"] = 0.0
    else:
        # Changed default from 5.0 to 0.0
        display_table["Safety Factor (%)"] = display_table["Safety Factor (%)"].fillna(0.0)

    if "Max Size" not in display_table.columns:
        display_table["Max Size"] = ""
    else:
        display_table["Max Size"] = display_table["Max Size"].fillna("")

    # Add helper columns
    display_table.insert(0, "Sr No", [str(i) for i in range(1, len(display_table) + 1)])

    # Initialize Select column based on session state
    display_table.insert(1, "Select", False)
    if st.session_state.selected_rows:
        for idx in st.session_state.selected_rows:
            if idx < len(display_table):
                display_table.at[idx, "Select"] = True

    # Define column order
    column_order = [
        "Sr No", "Select", "Tag No", "Category", "Product", "Model", "Max Size",
        "Width (mm)", "Height (mm)", "Airflow (L/s)", "Safety Factor (%)",
        "Total Area (m²)", "Velocity (m/s)", "Section Size", "Section Area (m²)", "No of Sections",
        "Section Velocity (m/s)", "Section Pressure Drop (Pa)", "Total Pressure Drop (Pa)"
    ]

    existing_columns = [col for col in column_order if col in display_table.columns]
    return display_table[existing_columns]


def setup_column_config():
    """Setup column configuration for data editor"""
    all_products = list(st.session_state.PRODUCT_DATA.keys())

    all_models = []
    for product_name in all_products:
        for model_name in st.session_state.PRODUCT_DATA[product_name].keys():
            all_models.append(model_name)
    all_models = list(set(all_models))

    all_max_sizes_list = get_all_max_sizes()

    return {
        "Sr No": st.column_config.TextColumn("Sr No", disabled=True),
        "Select": st.column_config.CheckboxColumn("Select"),
        "Tag No": st.column_config.TextColumn("Tag No"),
        "Category": st.column_config.SelectboxColumn("Category", options=CATEGORIES),
        "Product": st.column_config.SelectboxColumn("Product", options=all_products),
        "Model": st.column_config.SelectboxColumn("Model", options=all_models),
        "Max Size": st.column_config.SelectboxColumn("Max Size", options=all_max_sizes_list),
        "Width (mm)": st.column_config.NumberColumn("Width (mm)", format="%d"),
        "Height (mm)": st.column_config.NumberColumn("Height (mm)", format="%d"),
        "Airflow (L/s)": st.column_config.NumberColumn("Airflow (L/s)", format="%.1f"),
        "Safety Factor (%)": st.column_config.NumberColumn("Safety Factor (%)", format="%.2f"),
        "Total Area (m²)": st.column_config.NumberColumn("Total Area (m²)", format="%.3f", disabled=True),
        "Velocity (m/s)": st.column_config.NumberColumn("Velocity (m/s)", format="%.2f", disabled=True),
        "Section Size": st.column_config.TextColumn("Section Size", disabled=True),
        "Section Area (m²)": st.column_config.NumberColumn("Section Area (m²)", format="%.3f", disabled=True),
        "No of Sections": st.column_config.NumberColumn("No of Sections", format="%d", disabled=True),
        "Section Velocity (m/s)": st.column_config.NumberColumn("Section Velocity (m/s)", format="%.2f", disabled=True),
        "Section Pressure Drop (Pa)": st.column_config.NumberColumn("Section Pressure Drop (Pa)", format="%.2f",
                                                                    disabled=True),
        "Total Pressure Drop (Pa)": st.column_config.NumberColumn("Total Pressure Drop (Pa)", format="%.2f",
                                                                  disabled=True),
    }


def get_export_data_in_order(selected_columns):
    """Prepare export data in the specific order required"""
    # Define the desired column order for export
    export_order = [
        "Tag No", "Category", "Product", "Model", "Max Size", "Safety Factor (%)",
        "Width (mm)", "Height (mm)", "Airflow (L/s)", "Total Area (m²)", "Velocity (m/s)",
        "Section Size", "Section Area (m²)", "No of Sections", "Section Velocity (m/s)",
        "Section Pressure Drop (Pa)", "Total Pressure Drop (Pa)"
    ]

    # Filter only selected and available columns in the desired order
    ordered_columns = [col for col in export_order if
                       col in selected_columns and col in st.session_state.damper_table.columns]

    # Get the data with only selected columns in the desired order
    export_data = st.session_state.damper_table[ordered_columns].copy()

    # Add Sr No at the beginning
    export_data.insert(0, "Sr No", [str(i) for i in range(1, len(export_data) + 1)])

    return export_data


def handle_table_actions(selected_indices):
    """Handle all table actions (delete, clear, export)"""
    st.subheader("📤 Table Actions")

    # Action buttons in a single row - all 6 buttons together
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        move_up = st.button("⬆️ Move Up", use_container_width=True, type="secondary")

    with col2:
        move_down = st.button("⬇️ Move Down", use_container_width=True, type="secondary")

    with col3:
        delete = st.button("🗑️ Delete", use_container_width=True, type="primary")

    with col4:
        clear = st.button("🧹 Clear", use_container_width=True, type="primary")

    # Short column mapping with exact names as requested
    short_column_mapping = {
        "Sr No": "S.no",
        "Tag No": "Tag",
        "Category": "Category",
        "Product": "Product",
        "Model": "Model",
        "Max Size": "MaxSize",
        "Safety Factor (%)": "SF(%)",
        "Width (mm)": "w(mm)",
        "Height (mm)": "H(mm)",
        "Airflow (L/s)": "Airflow(l/s)",
        "Total Area (m²)": "T_Area(m²)",
        "Velocity (m/s)": "Vel(m/s)",
        "Section Size": "SecSize",
        "Section Area (m²)": "SecArea(m²)",
        "No of Sections": "No_Sec",
        "Section Velocity (m/s)": "SecVel(m/s)",
        "Section Pressure Drop (Pa)": "SecPd",
        "Total Pressure Drop (Pa)": "T_Pd"
    }

    # Get available columns for export (excluding helper columns)
    available_columns = [col for col in st.session_state.damper_table.columns if col not in ['Select', 'Sr No']]

    # Initialize export columns if not set or if table has changed
    if not st.session_state.export_columns or len(st.session_state.export_columns) == 0:
        st.session_state.export_columns = available_columns

    # Always show CSV and PDF buttons when there's data, just disable if no columns selected
    with col5:
        if not st.session_state.damper_table.empty:
            # Always show the CSV button, just disable if no columns selected
            export_data = get_export_data_in_order(st.session_state.export_columns)
            export_data_short = export_data.rename(columns=short_column_mapping)
            csv_data = export_data_short.to_csv(index=False)

            st.download_button(
                "💾 Save CSV",
                csv_data,
                file_name=f"{customer}_{project}_results.csv",
                mime="text/csv",
                use_container_width=True,
                type="primary",
                disabled=len(st.session_state.export_columns) == 0
            )
        else:
            st.button("💾 Save CSV", disabled=True, use_container_width=True)

    with col6:
        if not st.session_state.damper_table.empty:
            try:
                # Always show the PDF button, just disable if no columns selected
                export_data = get_export_data_in_order(st.session_state.export_columns)
                export_data_short = export_data.rename(columns=short_column_mapping)
                pdf_bytes = save_table_as_pdf(export_data_short, customer, project, report_date)

                if pdf_bytes and len(pdf_bytes) > 0:
                    st.download_button(
                        "📄 Save PDF",
                        data=pdf_bytes,
                        file_name=f"{customer}_{project}_results.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                        type="primary",
                        key=f"pdf_download_{st.session_state.data_editor_key}",
                        disabled=len(st.session_state.export_columns) == 0
                    )
                else:
                    st.error("PDF generation failed - no data received")
            except Exception as e:
                st.error(f"Error generating PDF: {e}")
        else:
            st.button("📄 Save PDF", disabled=True, use_container_width=True)

    # Handle button actions after defining all buttons
    if move_up:
        if handle_row_movement("up", selected_indices):
            st.success("✅ Selected rows moved up!")
            st.rerun()

    if move_down:
        if handle_row_movement("down", selected_indices):
            st.success("✅ Selected rows moved down!")
            st.rerun()

    if delete:
        if selected_indices:
            new_table = st.session_state.damper_table.drop(selected_indices).reset_index(drop=True)
            st.session_state.damper_table = new_table
            st.session_state.selected_rows = set()
            st.session_state.data_editor_key += 1
            st.success("✅ Selected rows deleted successfully!")
            st.rerun()
        else:
            st.warning("Please select rows to delete first.")

    if clear:
        if not st.session_state.damper_table.empty:
            st.session_state.damper_table = pd.DataFrame()
            st.session_state.selected_rows = set()
            st.session_state.data_editor_key += 1
            st.success("✅ Table cleared!")
            st.rerun()
        else:
            st.info("No data to clear.")

    # Column selection for export - placed below the table action buttons, spanning full width
    if not st.session_state.damper_table.empty:
        st.markdown("---")
        st.subheader("📊 Export Settings")

        # Column selection for export - full width
        selected_columns = st.multiselect(
            "Select columns to export:",
            options=available_columns,
            default=st.session_state.export_columns,
            key="column_selector"
        )

        st.session_state.export_columns = selected_columns


# Main Project Summary Section
st.subheader("📊 Project Summary")

if not st.session_state.damper_table.empty:
    st.write(f"**Customer:** {customer} | **Project:** {project} | **Date:** {report_date}")

    # Prepare and display the table
    display_table = prepare_display_table()
    column_config = setup_column_config()

    # Render editable table with a unique key to force refresh
    edited_df = st.data_editor(
        display_table,
        key=f"data_editor_{st.session_state.data_editor_key}",
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        column_config=column_config
    )

    # Update selected rows from the edited DataFrame
    if "Select" in edited_df.columns:
        new_selected_rows = set()
        for idx, row in edited_df.iterrows():
            if row.get("Select", False):
                new_selected_rows.add(idx)

        # Only update if selection changed to avoid unnecessary reruns
        if new_selected_rows != st.session_state.selected_rows:
            st.session_state.selected_rows = new_selected_rows

    # Handle edits and recalculations (only for non-select columns)
    if not edited_df.equals(display_table):
        # Check if changes are only in Select column
        non_select_columns = [col for col in edited_df.columns if col != "Select"]
        display_non_select = display_table[non_select_columns]
        edited_non_select = edited_df[non_select_columns]

        if not edited_non_select.equals(display_non_select):
            edited_df = handle_table_edits(edited_df)
            edited_data = edited_df.drop(columns=['Select', 'Sr No'], errors='ignore')
            st.session_state.damper_table = edited_data.reset_index(drop=True)
            st.session_state.data_editor_key += 1
            st.rerun()

    # Handle table actions
    handle_table_actions(list(st.session_state.selected_rows))

else:
    st.info("No data yet. Add manually or upload a CSV/Excel to calculate automatically.")

# ------------------- Footer -------------------
st.markdown("---")
st.markdown(
    "<div class='footer'>🌀 Pressure Drop Calculation Tool — Central Ventilation Systems</div>",
    unsafe_allow_html=True,
)