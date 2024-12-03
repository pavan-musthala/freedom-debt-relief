# Freedom Debt Relief - Marketing Campaign Analysis

<img src="https://media.giphy.com/media/JrXas5ecb4FkwbFpIE/giphy.gif"  width="400" height="400"/>

### About Freedom Debt Relief

+ Freedom Debt Relief is a company that specializes in debt settlement services.
+ With a mission to assist individuals and families struggling with unmanageable debt, Freedom negotiates with creditors to reduce the total amount owed, providing a pathway towards financial freedom.

### Purpose of this Project

#### Overview

+ This project evaluates the effectiveness of a recent $5 million Marketing campaign conducted by Freedom Debt Relief. The analysis spans five months, with the campaign occurring in the third month.
+ The objective is to present insights to Marketing, Sales, and Operations regarding the success of the campaign.
+ Using the datasets given:

1. Provide a quantitative assessment of whether the marketing campaign was successful. What metrics were chosen and why?
2. Based on the provided data, what recommendation can be provided for the campaign strategy to be adjusted in the future to improve performance?
3. How would campaign performance have changed if it was rolled out in Month 6 instead of Month 3? Provide an incremental number versus your result in Question #1.


### Notebook Content

1. __Data exploration and Quantitative Assessment__:
  - Thorough exploration of client and deposit data to quantitatively assess campaign performance

2. __Metrics Selections__:
   - Explanation of chosen metrics and their relevance in evaluating campaign's impact

3. __Recommendations for Future Strategy__:
   - Strategic insights and recommendations to enhance future campaign performance
 
## Data Description

### Table 1: client_data.csv

__Data specific to fictional clients__

+ client_id: Randomly generated unique surrogate identifier for a client
+ client_geographical_region: Client geographical location in relation to U.S. Census definitions
+ client_residence_status: Client residence status in relation to whether they rent or own
+ client_age: Client age in relation to date of birth

### Table 2: deposit_data.csv 

__You will find data specific to the client deposit behavior__

+ client_id: Randomly generated unique surrogate identifier for a client
+ deposit_type: Delineates whether a client deposit is the scheduled record or actual record
+ deposit_amount: Client deposit amount to the dedicated bank account with Freedom
+ deposit_cadence: Timing and pattern of client deposit activity
+ deposit_date: Deposit date for deposit type

### Table 3: calendar_data.csv 

__This is a calendar reference table__

+ gregorian_date: This date aligns with the Gregorian calendar
+ month_name: These are the designated months in the case study
  - Month 1 and 2 are pre-campaign
  - Month 3 is the campaign
  - Month 4 and 5 are post-campaign

## Happy Analyzing! 📊
