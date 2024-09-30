import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style="dark")



day_df = pd.read_csv("day_fix.csv", delimiter=",")
hour_df = pd.read_csv("hour_fix.csv", delimiter=",")

datetime_columns = ["date"]
day_df.sort_values(by="date", inplace=True)
day_df.reset_index(inplace=True)
datetime_columns = ["date"]
hour_df.sort_values(by="date", inplace=True)
hour_df.reset_index(inplace=True)
 
for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])
    hour_df[column] = pd.to_datetime(hour_df[column])

min_date_day = day_df["date"].min()
max_date_day = day_df["date"].max()

min_date_hour = hour_df["date"].min()
max_date_hour = hour_df["date"].max()
 
with st.sidebar:
    st.image("https://previews.123rf.com/images/stacyl17/stacyl171912/stacyl17191200104/135618701-vector-illustration-of-bike-rental-brush-lettering-for-banner-leaflet-poster-clothes-logo.jpg")
    
    start_date, end_date = st.date_input(
        label="Rentang Waktu",min_value=min_date_day,
        max_value=max_date_day,
        value=[min_date_day, max_date_day]
    )
filtered_day_df = day_df[(day_df["date"] >= pd.to_datetime(start_date)) & (day_df["date"] <= pd.to_datetime(end_date))]
filtered_hour_df = hour_df[(hour_df["date"] >= pd.to_datetime(start_date)) & (hour_df["date"] <= pd.to_datetime(end_date))]

st.title("Dashboard Penggunaan Sepeda🚲")


st.subheader("Rental Harian dan Pendaftaran")

col1, col2 = st.columns(2)

with col1:
    total_rentals = filtered_day_df["total_riders"].sum()
    st.metric("Total Rental", value=total_rentals)

with col2:
    total_registrations = filtered_day_df["registered"].sum()  
    st.metric("Total Pendaftaran", value=total_registrations)


st.subheader("Pola Penggunaan Sepeda Berdasarkan Waktu (Jam) dalam Satu Hari")
avgHourly = filtered_hour_df.groupby(filtered_hour_df["hour"])["total_riders"].mean()
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(avgHourly.index,avgHourly.values, marker="o", linestyle="-", color="b")
ax.set_title("Rata-Rata Penggunaan Sepeda Dalam Satu Hari")
ax.set_xlabel("Jam")
ax.set_ylabel("Rata-rata penggunaan sepeda")
st.pyplot(fig)

st.subheader("Penggunaan Sepeda Berdasarkan Musim")
avgSeason = filtered_day_df.groupby("season")["total_riders"].mean()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=avgSeason.index, y=avgSeason.values, ax=ax, palette="Set2")
ax.set_title("Rata-rata Penggunaan Sepeda Berdasarkan Musim")
ax.set_ylabel("Rata-rata penggunaan sepeda")
st.pyplot(fig)

st.subheader("Penggunaan Sepeda pada Hari Libur vs Hari Kerja")
avgHoliday = filtered_day_df.groupby("holiday")["total_riders"].mean()
fig, ax = plt.subplots(figsize=(8, 5))
if filtered_day_df["holiday"].nunique() > 1:  
    sns.barplot(x=["Hari Kerja", "Hari Libur"], y=avgHoliday.values, ax=ax, palette="Set1")
    ax.set_title("Rata-rata Penggunaan Sepeda pada Hari Libur vs Hari Kerja")
    ax.set_ylabel("Rata-rata penggunaan sepeda")
    st.pyplot(fig)
else:
    st.write("Hanya data hari libur yang tersedia dalam rentang waktu yang dipilih.")
    sns.barplot(x=["Hari Libur"], y=avgHoliday.values, ax=ax, palette="Set1")
    ax.set_title("Rata-rata Penggunaan Sepeda pada Hari Libur")
    ax.set_ylabel("Rata-rata penggunaan sepeda")
    st.pyplot(fig)

st.subheader("Distribusi Penggunaan Sepeda Sepanjang Minggu")
weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

avgWeekly = filtered_day_df.groupby("weekday")["total_riders"].mean()

weeklyUsage = {day: avgWeekly.get(day, 0) for day in range(7)}

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=weekdays, y=list(weeklyUsage.values()), ax=ax, palette="coolwarm")

ax.set_title("Rata-rata Penggunaan Sepeda per Hari dalam Seminggu")
ax.set_ylabel("Rata-rata penggunaan sepeda")
st.pyplot(fig)
