import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
import plotly.express as px


def show_analysis_page():
    st.title('Analysis Page')

    hospital_details_df = pd.read_csv('Hospitalisation details.csv')
    medical_df = pd.read_csv('Medical Examinations.csv')
    Patient_names = pd.read_excel('Names.xlsx')

    ## Merging csv's into one
    first_merge = pd.merge(left = hospital_details_df, right = medical_df, on = 'Customer ID')
    data = pd.merge(left = Patient_names, right = first_merge, on = 'Customer ID')
    df = data.copy()
    df.head(2)

    ## I want to change columns name for better display
    df.columns = df.columns.str.lower()

    ## Data has ? in this data, we are going to remove it. 
    df.apply(lambda x : x == '?').sum()

    df = df.replace('?', np.nan)
    df.dropna(inplace = True)


    df['numberofmajorsurgeries'] = df['numberofmajorsurgeries'].replace('No major surgery', 0)
    df['numberofmajorsurgeries'] = df['numberofmajorsurgeries'].astype(int)

    df['year'] = df['year'].astype(int)
    today_date = datetime.date.today()
    current_year = today_date.year
    df['age'] = current_year - df['year']

    ## Assigning Gender according to their respective names
    def gender_assign(name):
        if 'Mr' in name:
            return 'Male'
        elif 'Miss' in name:
            return 'Female'
        elif 'Mrs' in name:
            return 'Female'
        elif 'Ms' in name:
            return 'Female'

    df['beneficiary_gender'] = df['name'].apply(gender_assign)
    
    st.write("Dataset after merging and cleaning:", df.head())
    
    ## Charts


    ## Average charges against hospital
    
    col1, col2 = st.columns(2)

    with col1:
        average_charges = df.groupby('hospital tier')['charges'].mean().reset_index()
        fig1 = px.bar(average_charges,
            x= 'hospital tier',
            y = 'charges',
            barmode='group',
            labels={'hospital tier': "Hospital Tier", 'charges': 'Average Charges'},
            title='Average Charges Across Hospital Tiers'
                )
        
        fig1.update_layout(width=1500, height=450)
        st.plotly_chart(fig1)

    with col2:
        fig2 = px.bar(df,
                      x='hospital tier', 
                      y= 'charges',
                      barmode='group',
                      color='beneficiary_gender',
                      labels={'hospital tier': "Hospital Tier", 'charges': 'Average Charges'},
                      title="Gender-wise Charges by Hospital Tiers")
        fig2.update_layout(width=1500, height=450)

        st.plotly_chart(fig2)
    st.write("Average hospital charges in hospital tier 1 are `highly outnumbered` by other hospitals. They may provide premium services (e.g., `private room`, `assistance`, etc.). As for we go further and see in `gender wise`, we can see `hospital tier 2` charges high, especially for females.")

## FIGURE 2 Avgera charges across city  
    col1, col2 = st.columns(2)

    with col1:
        average_charges = df.groupby('city tier')['charges'].mean().reset_index()
        fig1 = px.bar(average_charges,
            x= 'city tier',
            y = 'charges',
            barmode='group',
            labels={'city tier': "City Tier", 'charges': 'Average Charges'},
            title='Average Charges Across city Tiers'
                )
        
        fig1.update_layout(width=1500, height=450)
        st.plotly_chart(fig1)

    with col2:
        fig2 = px.bar(df,
                      x='city tier', 
                      y= 'charges',
                      barmode='group',
                      color='beneficiary_gender',
                      labels={'city tier': 'City Tier', 'charges': 'Average Charges'},
                      title="Gender-wise Charges by city Tiers")
        fig2.update_layout(width=1500, height=450)

        st.plotly_chart(fig2)
    st.write("The average city charges in city tier 3 are slightly higher compared to other cities. They may have developed cities (e.g., `Mumbai`, `Bengaluru`, etc.). If we go further and look at `gender-wise`, we can see that in all city tiers, male average charges are higher, but in tier 3, they are the highest.")

## Figure 3
    ## Checking for which city has which type of hospitals is there and how many
    counts = df.groupby(['city tier', 'hospital tier']).size().unstack()
    counts.plot(kind = 'bar')
    plt.title('Which city has which type of hospital')
    plt.ylabel('Counts of hospital')
    plt.legend(loc = 'center left')
    plt.xticks(rotation=0)
    plt.show()
    st.pyplot(plt)

    st.write("`City tier 3` hospital has a slightly higher number of hospitals tier 1.")
    st.write("`City tier 2`, hospital tier 2 has the maximum number of hospitals")
    st.write("`City tier 1` hospital tier 3 has the highest number.")


## Figure 4
    grouped_counts = df.groupby(['smoker', 'heart issues']).size().unstack()
    grouped_counts.plot(kind='bar', figsize=(10, 6))
    plt.title('Count of People by smoker and Heart Issues', fontsize=16)
    plt.xlabel('smoker', fontsize=14)
    plt.ylabel('Count', fontsize=14)
    plt.xticks(rotation=0)
    plt.legend(title='Heart Issues')
    plt.show()
    st.pyplot(plt)

    st.write("The count of people who are not a smoker and does not have heart issues is high count and who smokes and have a heart issue their count is still pretty high so we can say the maximum patient are not a smokers or may have a heart issue.")

#3 Figure 4
    ## Average charges of whether patient smokes or not
    average_charges_smoker = df.groupby('smoker')['charges'].mean()
    average_charges_smoker.plot(kind = 'bar', figsize=(10,6))
    plt.title('Average Charges for Smokers and Non-Smokers', fontsize=16)
    plt.xlabel('Smoker', fontsize=14)
    plt.ylabel('Average Charges', fontsize=14)
    plt.xticks(rotation=0)
    plt.show()
    st.pyplot(plt)
    st.write("Patients who smoke have to pay more charges.")


## Figure 5
    ## Average charges of whether patient has heart issues or not
    average_charges_smoker = df.groupby('heart issues')['charges'].mean()
    average_charges_smoker.plot(kind = 'bar', figsize=(10,6))
    plt.title('Average Charges for heart issues', fontsize=16)
    plt.xlabel('heart issues', fontsize=14)
    plt.ylabel('Average Charges', fontsize=14)
    plt.xticks(rotation=0)
    plt.xticks(ticks=[0, 1], labels=['Yes', 'No'])
    plt.show()
    st.pyplot(plt)

    st.write("Patient has not heart issues have to pay because of may other include like sugar level, smoking etc..")

## Figure 6
    df.groupby(['smoker', 'heart issues'])['charges'].sum().unstack().plot(kind = 'bar')

    # Adding labels and title
    plt.title('', fontsize=16)
    plt.xlabel('smoker', fontsize=14)
    plt.ylabel('Average charges', fontsize=14)
    plt.xticks(rotation=0)
    plt.legend(title='Heart Issues')
    plt.show()
    st.pyplot(plt)

    st.write("""Patients who smoke and do not have any heart issues are likely to pay more charges compared to others,
            and the second thing is there are some patients who do not smoke,
             but still their charges are so high, maybe because of other illnesses.""")

