# pylint: disable=missing-module-docstring
import duckdb
import streamlit as st

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

with st.sidebar:
    theme = st.selectbox(
        "How would you like to review?",
        ("cross_joins", "GroupBy", "window_functions"),
        index=None,
        placeholder="Select theme...",
    )

    st.write("You selected:", theme)

    exercise = con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}'").df().sort_values("last_reviewed").reset_index()
    st.write(exercise)

    try:
        exercise_name = exercise.loc[0, "exercise_name"]
        with open(f"answers/{exercise_name}.sql", "r", encoding="utf_8") as f:
            answer = f.read()
        solution_df = con.execute(answer).df()
    except KeyError:
        answer = None
    except FileNotFoundError:
        answer = "The answer is not available yet... But you won't really need it, right?"




st.header("Enter your code:")
query = st.text_area(label="Your SQL code here", key="user_input")

if query:
    result = con.execute(query).df()
    st.dataframe(result)

    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
    except KeyError as e:
        st.write("Some colums are missing!")

    n_lines_difference = result.shape[0] - solution_df.shape[0]
    if n_lines_difference != 0:
        st.write(
            f"Result has a {n_lines_difference} lines difference with the solution_df"
        )


tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    try:
        exercise_tables = exercise.loc[0, "tables"]
        for table in exercise_tables:
            st.write(f"table: {table}")
            df_table = con.execute(f"SELECT * FROM {table}").df()
            st.dataframe(df_table)
    except KeyError:
        st.write("Please select a theme.")

with tab3:
    if answer:
        st.write(answer)
    else:
        st.write("Please select a theme.")
