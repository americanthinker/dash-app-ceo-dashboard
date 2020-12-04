## Data Analytics Dashboard for CEO of Veterans Service Organization
<p align="center">
  <img align="center" src="/assets/Dashboard-proto.png" width="800" title="Dashboard prototype">
</p>    

# Table of Contents
1. [Introduction](#introduction)
2. [Product Roadmap](#product-roadmap)
4. [Full Cycle Analytics Process Map](#full-cycle-analytics-process-map)
5. [Development Workflow](#development-workflow)
6. [Tech Stack](#tech-stack)
7. [Final Product](#final-product)
8. [Lessons Learned/Confirmed (along the way)](#lessons-learnedconfirmed-along-the-way)
9. [Shoutout Section!](#shout-out-section-wink)
# Introduction   

I embarked on an analytics platform journey by partnering with the CEO of [Elite Meet](www.elitemeet.us) - a non-profit Veterans Service Organization (VSO) 
that helps military veterans from Special Operations units transition into Corporate America after they leave service.  This was a [full-cycle data project](https://hdsr.mitpress.mit.edu/pub/577rq08d/release/3) beginning with delivering an initial value proposition to preparing the data all the way through deployment of an analytics platform in the cloud for use by the CEO.  Here is what I learned...  

# Product Roadmap   
- ## Status Quo  - The Challenge

    - Data resides in a Salesforce database.  Data is dirty and requires multiple transformation to derive insights. 
    - Current analytics/decision support is manual and time-consuming, i.e. not scalable or dynamic
    - CEO does not have time to conduct manual data pulls and sort through data for insight, i.e. needs answers at her fingertips

- ## Desired End State  

    - Data is automatically cleaned and tranformed for use. 
    - Data ingestion is automated and processed on a daily basis. 
    - CEO has access to self-serve analytics through a custom designed platform.
    - Solution is scable, production grade, and easy to maintain and update.  

- ## The Solution 
:white_check_mark: **Minimum Viable Product (MVP)**: A single-page, working dashboard connected to a local datasource.  Dashboard is visually appealing.  

:white_check_mark: **MVP+** : Multipage dashboard app deployed on a remote server.  Automated data pulls from original data source. Platforim is fully interactive.
- [ ] **MVP++** : Fully functioning app, modularized i.e. easy to maintain and update, and hardened for production.  User authentication required. 
<br></br>  

# Full Cycle Analytics Process Map
<p align="center">
  <img align="center" src="/assets/analyticspipeline3.png" width="1000" title="Analytics Pipeline">
</p>  

1. Data entry is performed at the user level when applicants enter their information into the application form on the [Elite Meet website](https://elitemeetus.org/).
2. The raw data is then stored in a cloud Salesforce instance.
3. Data is automatically pulled from Salesforce on a daily basis through their REST API. Schedule manager is [PM2](https://pm2.keymetrics.io/).
4. Data is cleaned and transformed on-site through an automated script and pushed to [Heroku](https://heroku.com) server on a daily basis.
5. Data is programatically further transformed through the [Dash](https://plotly.com/dash/) app on the Heroku server.  Git push to Heroku automatically generates the rebuild.
6. End user (CEO) can access the app website on [Heroku](https://heroku.com)at any time of day.   
<br></br>
# Development workflow
<p align="center">
  <img align="center" src="/assets/workflow2.png" width="1000" title="Development Workflow">
</p>  

1. All worked performed locally on iMac desktop.  
2. Saved work stored locally and in remote private Github repo. Repo is private to prevent public access to data. 
3. Created local feature branches to work on major feature changes.  Tested in local test environment and merged to master upon successful testing. 
4. Post-merge, app is tested in sandbox to check for deployability issues before pushing to production server.
5. Copy of work stored in public facing repo for educational purposes. 

## Tech Stack  

- App development: 
    - Python: 
        - Dash: design, configuration, and interaction
        - Plotly: data visualization
        - pandas: data crunching
    - CSS: styling
- Data pull automation/scheduling: 
    - Python: 
        - REST API interaction: simple_salesforce
    - Unix: 
        - PM2 and cron: job scheduler and automation
        - Bash scripting: autogenerate git push to Heroku through Heroku CLI
- Web server, app hosting:
    - Heroku  

***See requirements.txt file for full details on all associated libraries. 

# Final Product. 

<p float="left">
  <img align="center" src="/assets/homepage.png" width="500" />
  <img align="center" src="/assets/membership.png" width="500" /> 
</p> 


<p align='center'> 
  <img src="/assets/marketing.png" width="500" />
</p>

<br></br>
# Lessons Learned/Confirmed (Along the way...) 
- Commit early, commit often.  
- Just because it works in (local) testing does not guarantee that it will work in production.
- [Daft Punk](https://en.wikipedia.org/wiki/Daft_Punk) :sound: + Caffeine = ANYTHING is possible
- Read the docs, first, and then again after you have a better understanding. 
- Leverage the knowledge/skillsets of those in your network to blast through sticking points. 
- Sometimes, but certainly not always, the best answer is as simple as a REST API call, backed by a [cron](https://en.wikipedia.org/wiki/Cron) job, vs. newfangled, multifeatured software.  
- User feedback is critical throughout the Dev process, otherwise you're just a guy wearing [beer goggles](https://www.alcohol.org/effects/beer-goggles/) who's fallen in love with the product. 
- Persistence wins the day - always.  
<br></br>
# Shout-out section! :wink:
Special thanks to the following for helping me out along the way:
- [Ron Li](https://www.linkedin.com/in/ron-li-6531bb1b7/): for introducing me to [Dash](https://plotly.com/dash/) - a powerful Python framework for dashboard creation - and acting as a guide along the way
- [Ann Strange](https://www.linkedin.com/in/ann-strange/): for providing insight into the inner workings of the Salesforce platform
- Joe R.: for pointing out that my initial color scheme screamed "1995"
- Kayla Thomas and Sam G.: for insightful feedback along the way  
- My wife: for letting me escape into my dev cave :tent: for two weeks straight


