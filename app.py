import streamlit as st
from statsmodels.stats.power import FTestAnovaPower
import pandas as pd
import math

st.subheader("How many participants do I need?")
st.markdown("Add the details below to find the magic number!")

anova = FTestAnovaPower()

num_independent_variables = int(
    st.number_input("Number of independent variables", 1, 100, step=1, value=3)
)
all_independent_variables = {i: {} for i in range(num_independent_variables)}

with st.sidebar:

    for i in range(num_independent_variables):
        name_variable = st.text_input(
            "Name of independent variable", key=f"{i}_name", value=f"variable_{i}"
        )
        num_values = st.number_input(
            "Number of values", key=f"{i}_num", step=1, min_value=1
        )
        all_independent_variables[i]["name"] = name_variable
        all_independent_variables[i]["num_values"] = num_values
        st.markdown("---")


(
    col1,
    col2,
) = st.columns(2)

with col1:
    effect_size = st.number_input("Effect size")
    power = st.number_input("Power")

with col2:
    alpha = st.number_input("Alpha")
    prize_per_participant = st.number_input("Prize per participant (in £)", value=2.5)

k_groups = 1
num_values_variables = [i["num_values"] for idx, i in all_independent_variables.items()]
for i in num_values_variables:
    k_groups *= i


if effect_size and power and alpha:

    n_per_group = anova.solve_power(
        effect_size=effect_size, alpha=alpha, power=power, k_groups=k_groups
    )

    st.markdown("---")

    #     st.markdown(
    #         """
    # | Total number of participants     |  {n_per_group:.2f} |
    # | Number of participants per group |  {n_per_group//k_groups + int(bool(n_per_group%k_groups))} |
    # | Total amount needed (in £)       |  {n_per_group * prize_per_participant:.2f} |
    #                 """
    #     )

    #     st.markdown(f"**Total number of participants** : {n_per_group:.2f}")
    #     st.markdown(
    #         f"**Number of participants per group**: {n_per_group//k_groups + int(bool(n_per_group%k_groups))}"
    #     )
    #     st.markdown(
    #         f"**Total amount needed (in £)**: {n_per_group * prize_per_participant:.2f}"
    #     )

    data = {
        "Quantity": [
            "Number of groups",
            "Total number of participants",
            "Participants per group",
            "Total amount needed",
        ],
        "Value": [
            f"{k_groups}",
            f"{math.ceil(n_per_group)}",
            f"{math.ceil(n_per_group // k_groups)}",
            f"£ {math.ceil(n_per_group * prize_per_participant)}",
        ],
    }

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Display as a table
    st.dataframe(df, hide_index=True)

else:
    st.markdown("Please choose the values above to find the number of participants")
