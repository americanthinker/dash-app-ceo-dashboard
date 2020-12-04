## Data Analytics Dashboard for CEO of Veterans Service Organization (Elite Meet)

<p align="center">
  <img align="center" src="/assets/Dashboard-proto.png" width="1000" title="Dashboard prototype">
</p> 

I embarked on an analytics dashboard journey by partnering with the CEO of [Elite Meet](www.elitemeet.us) - a non-profit Veterans Service Organization (VSO) that help military veterans from Special Operations units transition into Corporate America after they leave service.  This was a full-cycle data project beginning with delivering an initial value proposition to preparing the data all the way through deployment of an analytics platform in the cloud for use by the CEO.  Here is what I learned...  

- [x] **Minimum Viable Product (MVP)**: A single-page, working dashboard connected to a local datasource.  Dashboard is visually appealing. 
- [x] **MVP+** : Multipage dashboard app deployed on a remote server.  Automated data pulls from original data source. 
- [ ] **MVP++** : Fully functioning app, modularized i.e. easy to maintain and update, and hardened for production.  User authentication required. 

<p align="center">
  <img align="center" src="/assets/analyticspipeline.png" width="1000" title="Analytics Pipeline">
</p> 

<br></br> 

<p align="center">
  <img align="center" src="/assets/workflow.png" width="1000" title="Development Workflow">
</p> 


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

\** *Special Thanks to the following for helping me out along the way: 
- Ron Li: for introducing me to Dash - a powerful Python framework for dashboard creation - and acting as a guide along the way
- Ann Strange: for providing insight into the inner workings of the Salesforce platform
- Joe Raetano: for pointing out that my initial color scheme screamed "1995"
- Kayla Thomas and Sam Giampapa: for insightful feedback along the way  
- My wife: for letting me escape into my dev cave for two weeks straight


