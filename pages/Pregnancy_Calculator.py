import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta
st.set_page_config(
   page_title="Pregnancy Calculator",
   page_icon="🤰",
   layout="wide",
   initial_sidebar_state="expanded",
)
def make_donut(input_response, input_text, input_color):
  chart_color = ['#27AE60', '#781F16']
  source = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100-input_response, input_response]
  })
  source_bg = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100, 0]
  })
    
  plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          #domain=['A', 'B'],
                          domain=[input_text, ''],
                          # range=['#29b5e8', '#155F7A']),  # 31333F
                          range=chart_color),
                      legend=None),
  ).properties(width=130, height=160)
    
  text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=20, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{input_response} %'))
  plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          # domain=['A', 'B'],
                          domain=[input_text, ''],
                          range=chart_color),  # 31333F
                      legend=None),
  ).properties(width=130, height=160)
  return plot_bg + plot + text
def calculate_due_date_by_last_menstrual_period(date_of_last_menstrual_period, pregnancy_duration):
    due_date = date_of_last_menstrual_period + timedelta(days=pregnancy_duration)
    return due_date
def calculate_ivf_last_menstrual_period(date_of_ivf_transfer, pregnancy_duration, embryo_stage):
    if embryo_stage == "Day 3":
        extra_days = 3 + 14
    elif embryo_stage == "Day 5":
        extra_days = 5 + 14
    pregnancy_duration = pregnancy_duration - extra_days
    last_menstral_date = date_of_ivf_transfer - timedelta(days=extra_days)
    due_date = date_of_ivf_transfer + timedelta(days=pregnancy_duration)
    return due_date, last_menstral_date
def calculate_days_preganant(last_menstrual_period_date):
    # Get the current date
    current_date = datetime.now().date()
    # Calculate the difference in days
    difference_in_days = (current_date - last_menstrual_period_date).days 
    return difference_in_days
def calculate_weeks_pregnant(last_menstrual_period_date):  
    # Get the current date
    current_date = datetime.now().date()
    # Calculate the difference in days
    difference_in_days = (current_date - last_menstrual_period_date).days 
    # Convert days to weeks
    difference_in_weeks = difference_in_days / 7
    return round(difference_in_weeks,2)
def calculate_days_left(due_date):
    # Get the current date
    current_date = datetime.now().date()
    # Calculate the difference in days
    difference_in_days = (due_date - current_date).days 
    return difference_in_days
def calculate_weeks_left(due_date):
    # Get the current date
    current_date = datetime.now().date()
    # Calculate the difference in days
    difference_in_days = (due_date - current_date).days 
    # Convert days to weeks
    difference_in_weeks = difference_in_days / 7
    return round(difference_in_weeks,2)
def calculate_last_menstrual_period_by_due_date(due_date, pregnancy_duration):
    last_menstrual_period_date = due_date - timedelta(days=pregnancy_duration)
    return last_menstrual_period_date
def calculate_percentage_of_pregnancy_completed(last_menstrual_period_date, pregnancy_duration):
    days_preganant = calculate_days_preganant(last_menstrual_period_date)
    percentage_of_pregnancy = (days_preganant / pregnancy_duration) * 100
    return round(percentage_of_pregnancy,2)
def create_pregnancy_timeline(lmp_date_str, pregnancy_duration=280):
    due_date = calculate_due_date_by_last_menstrual_period(datetime.strptime(lmp_date_str, "%Y-%m-%d"), pregnancy_duration)
    # Create a list of weeks from the start of the pregnancy to the due date
    weeks = []
    current_date = datetime.strptime(lmp_date_str, "%Y-%m-%d")
    week_number = 1
    while current_date <= due_date:
        weeks.append({
            "Week Number": week_number,
            "Start Date": current_date.strftime("%Y-%m-%d"),
            "End Date": (current_date + timedelta(days=6)).strftime("%Y-%m-%d")
        })
        current_date += timedelta(days=7)
        week_number += 1
    # Create a DataFrame from the list of weeks
    df = pd.DataFrame(weeks)
    # Highlight the current week
    today = datetime.today().strftime("%Y-%m-%d")
    df["Current Week"] = df.apply(lambda row: "You are HERE!!!" if row["Start Date"] <= today <= row["End Date"] else ("✔️" if row["End Date"] < today else ""), axis=1)
    df.at[df.index[-1], "Current Week"] = "💖💖💖💖💖💖  👶  💖💖💖💖💖💖"
    return df
def highlight_row(row):
    if 'You are HERE!!!' in row.values:
        return ['background-color: green' for _ in row]
    elif '✔️' in row.values:
        return ['background-color: black' for _ in row]
    else:
        return ['' for _ in row]
def get_summary_details_dataframe(due_date, pregnancy_duration, last_menstrual_period_date):
    data = {"Description": ["Conception Date","Due Date:", "Pregnancy Duration (Days): ", "Days Pregnant: ", "Weeks Pregnant: ", "Weeks until Due Date: ", "Days until Due Date:", "Pregnancy Completed ( % ): "],
            "Values": [last_menstrual_period_date.strftime("%Y-%m-%d"),due_date.strftime("%Y-%m-%d"), str(pregnancy_duration), str(calculate_days_preganant(last_menstrual_period_date)), str(calculate_weeks_pregnant(last_menstrual_period_date)), str(calculate_weeks_left(due_date)),str(calculate_days_left(due_date)),str(calculate_percentage_of_pregnancy_completed(last_menstrual_period_date, pregnancy_duration))]}
    df = pd.DataFrame(data)
    return df
def summary_details_component(due_date, pregnancy_duration, last_menstrual_period_date):
    df = get_summary_details_dataframe(due_date, pregnancy_duration, last_menstrual_period_date)
    data_container = st.container()
    with data_container:
        table, plot = st.columns(2)
        with table:
            st.table(df)
        with plot:
            st.altair_chart(make_donut(calculate_percentage_of_pregnancy_completed(last_menstrual_period_date, pregnancy_duration), 'Pregnancy Precentage Completed', 'red'), use_container_width=True)
def app():
    st.title("Pregnancy Calculator")
    st.markdown("*I created this page to help you calculate the due date of your baby. It's a simple tool that you can use to calculate the due date based on the Last Menstrual Period, Conception Date, IVF Transfer Date, or Due Date.*") 
    st.markdown("*The aquiracy of the due date calculation is based on the average pregnancy duration of 280 days. The pregnancy duration can vary from 266 to 294 days.*")
    st.markdown("*Please validate the due date with your healthcare provider, as this tool is for informational purposes only.*")
    pregnancy_duration = 280
    radiobutton_calculate_by_options = ["Last Menstrual Period (Start Date)", "Conception Date", "IVF Transfer Date", "Due Date"]
    radiobutton_calculate_by = st.radio("Calculation Option:", radiobutton_calculate_by_options)
    if radiobutton_calculate_by == "Last Menstrual Period (Start Date)":    
        last_menstral_date = st.date_input("Date of Last Menstrual Period")
        due_date = calculate_due_date_by_last_menstrual_period(last_menstral_date, pregnancy_duration)
        if last_menstral_date > datetime.now().date():
            st.error("The date of the last menstrual period cannot be in the future.")
            return
        elif datetime.now().date() > due_date:
            st.error("The due date cannot be in the past.")
            return
        summary_details_component(due_date, pregnancy_duration, last_menstral_date)
        week_dates= create_pregnancy_timeline(last_menstral_date.strftime("%Y-%m-%d"))
        st.dataframe(week_dates.style.apply(highlight_row, axis=1), hide_index=True, height=1475, use_container_width=True)
    elif radiobutton_calculate_by == "Conception Date":
        date_of_conception = st.date_input("Date of Conception")
        due_date = date_of_conception + timedelta(days=266)
        last_menstral_date = date_of_conception - timedelta(days=14)
        if last_menstral_date > datetime.now().date():
            st.error("The date of the last menstrual period cannot be in the future.")
            return
        elif datetime.now().date() > due_date:
            st.error("The due date cannot be in the past.")
            return
        summary_details_component(due_date, pregnancy_duration, last_menstral_date)
        week_dates= create_pregnancy_timeline(last_menstral_date.strftime("%Y-%m-%d"))
        st.dataframe(week_dates.style.apply(highlight_row, axis=1), hide_index=True, height=1475, use_container_width=True)
    elif radiobutton_calculate_by == "IVF Transfer Date":
        date_of_ivf_transfer = st.date_input("Date of IVF Transfer")
        radiobutton_embryo_stage_options = ["Day 3", "Day 5"]
        radiobutton_embryo = st.radio("Embryo Stage days:", radiobutton_embryo_stage_options)
        due_date, last_menstral_date = calculate_ivf_last_menstrual_period(date_of_ivf_transfer, pregnancy_duration, radiobutton_embryo)
        if last_menstral_date > datetime.now().date():
            st.error("The date of the last menstrual period cannot be in the future.")
            return
        elif datetime.now().date() > due_date:
            st.error("The due date cannot be in the past.")
            return
        summary_details_component(due_date, pregnancy_duration, last_menstral_date)
        week_dates= create_pregnancy_timeline(last_menstral_date.strftime("%Y-%m-%d"))
        # st.dataframe(week_dates, hide_index=True, height=1475, use_container_width=True)
        st.dataframe(week_dates.style.apply(highlight_row, axis=1), hide_index=True, height=1475, use_container_width=True)
    elif radiobutton_calculate_by == "Due Date":
        date_of_due_date = st.date_input("Date of Due Date")
        due_date = date_of_due_date
        last_menstrual_period =calculate_last_menstrual_period_by_due_date(due_date, pregnancy_duration)
        summary_details_component(due_date, pregnancy_duration, last_menstrual_period)
        week_dates= create_pregnancy_timeline(last_menstrual_period.strftime("%Y-%m-%d"))
        st.dataframe(week_dates.style.apply(highlight_row, axis=1), hide_index=True, height=1475, use_container_width=True)
app()
