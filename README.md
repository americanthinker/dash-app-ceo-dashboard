## Data Analytics Dashboard for CEO of Veterans Service Organization
<p align="center">
  <img align="center" src="/assets/Dashboard-proto.png" width="1000" title="Dashboard prototype">
</p>    

# Introduction   

I embarked on an analytics platform journey by partnering with the CEO of [Elite Meet](www.elitemeet.us) - a non-profit Veterans Service Organization (VSO) 
that helps military veterans from Special Operations units transition into Corporate America after they leave service.  This was a full-cycle data project beginning with delivering an initial value proposition to preparing the data all the way through deployment of an analytics platform in the cloud for use by the CEO.  Here is what I learned...  
<br></br>  
# Product Roadmap   
## Status Quo  - The Challenge

- Data resides in a SalesForce database.  Data is dirty and requires multiple transformation to derive insights. 
- Current analytics/decision support is manual and time-consuming, i.e. not scalable or dynamic
- CEO does not have time to conduct manual data pulls and sort through data for insight, i.e. needs answers at her fingertips

## Desired End State  

- Data is automatically cleaned and tranformed for use. 
- Data ingestion is automated and processed on a daily basis. 
- CEO has access to self-serve analytics through a custom designed platform.
- Solution is scable, production grade, and easy to maintain and update.  

## The Solution 
- [x] **Minimum Viable Product (MVP)**: A single-page, working dashboard connected to a local datasource.  Dashboard is visually appealing. 
- [x] **MVP+** : Multipage dashboard app deployed on a remote server.  Automated data pulls from original data source. 
- [ ] **MVP++** : Fully functioning app, modularized i.e. easy to maintain and update, and hardened for production.  User authentication required. 
<br></br>  

# Full Cycle Analytics Process Map
<p align="center">
  <img align="center" src="/assets/analyticspipeline3.png" width="1000" title="Analytics Pipeline">
</p>  

1. Data entry is performed at the user level when applicants enter their information into the application form on the Elite Meet website.
2. The raw data is then stored in a cloud Salesforce instance.
3. Data is automatically pulled from Salesforce on a daily basis through their REST API. Schedule manager is PM2.
4. Data is cleaned and transformed on-site through an automated script and pushed to Heroku server on a daily basis.
5. Data is programatically further transformed through the Dash app on the Heroku server.  Git push to Heroku automatically generates the rebuild.
6. End user (CEO) can access the app website on Heroku at any time of day.   
<br></br>
# Development workflow
<p align="center">
  <img align="center" src="/assets/workflow2.png" width="1000" title="Development Workflow">
</p> 

<br></br>
# Lessons Learned/Confirmed (Along the way...) 
- Commit early, commit often.  
- Just because it works in (local) testing does not guarantee that it will work in production.
- Daft Punk + Caffeine = ANYTHING is possible
- Read the docs, first, and then again after you have a better understanding. 
- Leverage the knowledge/skillsets of those in your network to blast through sticking points. 
- Sometimes, but certainly not always, the answer is as simple as a REST API call backed by a cron job, vs. newfangled, multifeatured software.  
- User feedback is critical throughout the Dev process, otherwise your just a guy with beer goggles on who's fallen in love with the product. 
- Persistence wins the day - always.  
<br></br>
<br></br>

# Shout-out section!
Special thanks to the following for helping me out along the way:
- Ron Li: for introducing me to Dash - a powerful Python framework for dashboard creation - and acting as a guide along the way
- Ann Strange: for providing insight into the inner workings of the Salesforce platform
- Joe Raetano: for pointing out that my initial color scheme screamed "1995"
- Kayla Thomas and Sam Giampapa: for insightful feedback along the way  
- My wife: for letting me escape into my dev cave for two weeks straight


