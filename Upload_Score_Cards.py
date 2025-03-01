import itertools

import pandas as pd
import streamlit as st

st.title("Upload inidivual Excels and merge")

uploaded_files = st.file_uploader("Upload Excel files", type="xlsx", accept_multiple_files=True)

SHEET_NAME = "Knock Out Rounds"

if uploaded_files:
    first = True
    for uploaded_file in uploaded_files:
        # Read each Excel file
        filename = uploaded_file.name
        euro_data = pd.read_excel(uploaded_file, sheet_name=SHEET_NAME)

        # Display the Input Excel as DataFrame
        # st.write(f"DataFrame from the uploaded file: {uploaded_file.name}")
        # st.dataframe(euro_data)

        match_row_indices = list(range(5, 21)) + list(range(23, 39)) + list(range(41, 49)) + list(range(51, 55)) + [57]
        match_col_indices = [3, 6]
        score_col_indices = [4, 5]
        penalty_col_indices = [7, 8]

        matches = [
            euro_data.iloc[row_index, match_col_index]
            for row_index in match_row_indices
            for match_col_index in match_col_indices
        ]
        # st.write(matches)
        scores = [
            int(euro_data.iloc[row_index, score_col_index])
            for row_index in match_row_indices
            for score_col_index in score_col_indices
        ]
        # st.write(scores)
        penalty_scores = [
            int(euro_data.iloc[row_index, penalty_col_index])
            if pd.notna(euro_data.iloc[row_index, penalty_col_index])
            else euro_data.iloc[row_index, penalty_col_index]
            for row_index in match_row_indices
            for penalty_col_index in penalty_col_indices
        ]
        # st.write(penalty_scores)

        # Create column names
        match_column_names = [f"{matches[i]}-{matches[i + 1]}" for i in range(0, len(matches), 2)]
        penalty_columns = [f"(P) {matches[i]}-{matches[i + 1]}" for i in range(0, len(matches), 2)]
        column_names = list(itertools.chain(*zip(match_column_names, penalty_columns)))
        # Create row values
        row_values_matches = [f"{scores[i]}-{scores[i + 1]}" for i in range(0, len(scores), 2)]
        row_values_penalties = [f"{penalty_scores[i]}-{penalty_scores[i + 1]}"
                     if pd.notna(penalty_scores[i]) else penalty_scores[i]
                     for i in range(0, len(penalty_scores), 2)
                     ]
        row_values = list(itertools.chain(*zip(row_values_matches, row_values_penalties)))
        # Prepend the row values with the filename
        column_names = ["filename"] + column_names
        row_values = [filename] + row_values

        # st.write(column_names)
        # st.write(row_values)

        if first:
            # Create the Match Scores DataFrame
            result_df = pd.DataFrame([row_values], columns=column_names)
            # Keep track of having processed the first file
            first = False
        else:
            # Append the Match Scores DataFrame
            result_df = pd.concat([result_df, pd.DataFrame([row_values], columns=column_names)], ignore_index=True)


    # Display the Match Scores DataFrame
    st.write("Hover over the table below and, in the top-right, click 'Download as CSV':")
    # st.dataframe(result_df)

    # Drop the unnecessary columns (those that are all NaN)
    result_df = result_df.dropna(axis=1, how='all')
    st.dataframe(result_df)

    # Doesn't work in the deployed app:
    # st.button(
    #     "Save to Excel",
    #     on_click=lambda: result_df.to_excel("combined_sheet.xlsx", index=False)
    # )
