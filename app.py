import streamlit as st
from statsmodels.stats.power import FTestAnovaPower
import pandas as pd
import math

st.subheader("How many participants do I need?")
st.markdown(
    "Add the details below and on the sidebar on the left to find the magic number!"
)

st.info(
    """ Choose the values below and press "Enter" for the results to update!  
Step 1: Choose the number of independent variables below.  
Step 2: Choose the number of values the independent variables can take on the left sidebar.  
Step 3: Add information about Effect Size, Power, and Alpha and press enter!
        """
)

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
    effect_size = st.number_input("Effect size", value=0.2)
    power = st.number_input("Power", value=0.8)

with col2:
    alpha = st.number_input("Alpha", value=0.05)
    prize_per_participant = st.number_input("Prize per participant (in £)", value=2.5)


k_groups = 1
num_values_variables = [i["num_values"] for idx, i in all_independent_variables.items()]
for i in num_values_variables:
    k_groups *= i

if effect_size and power and alpha and k_groups > 1:

    n_per_group = anova.solve_power(
        effect_size=effect_size, alpha=alpha, power=power, k_groups=k_groups
    )

    st.markdown("---")

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
    st.markdown(
        "Please choose the values above and on the left to find the number of participants"
    )
