# pylint: disable=missing-module-docstring
# pylint: disable=exec-used

import os
import logging
import duckdb
import streamlit as st

if "data" not in os.listdir():
    logging.error(os.listdir())
    logging.error("Creating folder data")
    os.mkdir("data")

if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    with open("init_db.py", encoding="utf_8") as f:
        exec(f.read())

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)


def check_user_solution(user_query: str) -> None:
    """
    Checks that user SQL query is correct by:
    1: checking the columns
    2: checking the values
    :param user_query: a string containing the query interted by the user
    """
    result = con.execute(user_query).df()
    st.dataframe(result)
    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
    except KeyError:
        st.write("Some colums are missing!")
    n_lines_difference = result.shape[0] - solution_df.shape[0]
    if n_lines_difference != 0:
        st.write(
            f"Result has a {n_lines_difference} lines difference with the solution_df"
        )


available_themes = con.execute("SELECT DISTINCT theme FROM memory_state").df().values

with st.sidebar:
    theme = st.selectbox(
        "How would you like to review?",
        available_themes,
        index=None,
        placeholder="Select theme...",
    )

    if theme:
        st.write("You selected:", theme)
        SELECT_EXERCISE_QUERY = f"SELECT * FROM memory_state WHERE theme = '{theme}'"
    else:
        SELECT_EXERCISE_QUERY = "SELECT * FROM memory_state"

    exercise = (
        con.execute(SELECT_EXERCISE_QUERY)
        .df()
        .sort_values("last_reviewed")
        .reset_index(drop=True)
    )
    st.write(exercise)
    exercise_name = exercise.loc[0, "exercise_name"]
    with open(f"answers/{exercise_name}.sql", "r", encoding="utf_8") as f:
        ANSWER = f.read()
    solution_df = con.execute(ANSWER).df()


st.header("Enter your code:")
query = st.text_area(label="Your SQL code here", key="user_input")


if query:
    check_user_solution(query)

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
    if ANSWER:
        st.write(ANSWER)
    else:
        st.write("Please select a theme.")
