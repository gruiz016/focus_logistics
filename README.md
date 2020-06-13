# [Focus Logistics](https://focus-logistics.herokuapp.com/) - Logistics Management Platform

Created by: [Giovanni Ruiz](https://www.linkedin.com/in/giovanniruiz01/)

Technologies used: HTML, CSS, Python, Flask and PostgreSQL.

API used: [MapQuest API](https://developer.mapquest.com/)


# Short Description
 This capstone project is a management tool to help small or logistics managers track their fleets across the country. Focus Logistics is designed for teams that currently use excel spreadsheets or handle load tracking manually. By making a web platform users will have better visibility, automatic distance calculations and simple data analytics.  

# Design/Features
This platform was designed to be expanded on after building out V1 as a MVP. 

Meeting all capstone requirements, below is the schema design.

![Schema design for focus logistics ](https://raw.githubusercontent.com/gruiz016/focus_logistics/master/schema_design.png)

 1. Distribution Centers (Where users are receiving a load):

We call these locations, this is were users create a reusable D.C. that they can attach to a load they are tracking. By creating a D.C. when you update a loads location the distance is calculated by MapQuest API and appended to the page.

 2. Carriers (The people you hire to bring your load to your D.C.):

When you create a carrier profile you can select the carrier when creating a load. An expanded feature that will be released soon is carrier specific KPI's. This will allow users to see how carriers are stacking up against others.

3. Load Data (KPI's):

With the data collected from each load we look at several initial performance indicators. 

 - On time percentages
 - Breakdown percentages
 - Damages percentages
 - Average cost per load
 - Average cost per pallet
 - Average cost per pound 

 
