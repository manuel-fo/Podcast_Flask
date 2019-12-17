# Podcast_Flask

Project Type: Plan A

Group Members Name: Manuel Fernandez Oromendia

Link to live application: https://flask-podcast.herokuapp.com/home

Link to Repository: https://github.com/manuel-fo/Podcast_Flask

List of technology/API used:
    - Flask
    - flask-login
    - wtforms
    - flask_sqlalchemy
    - podcastparser (to parse XML files into python)
    - RSS feeds (these were the APIs i used to get all my data)
        - a list of the rss feeds i used is found in rss_links.py
    - bootstrap
    - templates
    
Detailed Description:
      This website is used to easily browse different podcast and look at their episodes and add the ones that you like into
      your list of favorites. In the home page you can view many different podcast and then click the 'View Episodes' button 
      to view a list of the 20 most recent episodes for that podcast. You can then click the name of an episode to start listening
      to that episode. If you have created an account and are logged in you will see a button next to each episode that 
      allows you to add that episode to your list of favorites. Once an episode is in your list of favorites you can navigate to 
      the favorites tab of the page where all your favorites are listed and if you click on one it will start playing. To create an 
      account you can either click the 'login' button on the top right of the page and then click 'dont have an account?' or you 
      can navigate to '/register'. The password that you create is never stored and only a hash is stored in the database to keep
      the website secure. In the future I wish to add the ability to create many custom playlists instead of just a favorites list
       and to also have the buttons next to each episode change to 'remove' if the episode has already been added to favorites. I 
       planned on doing this for this turn-in but it ended up being much more complex than it seemed at first glance. 
       If you have any questions please dont hesitate to reach out to me at: ferna285@umn.edu
       
Controllers and Descriptions:
     - '/home'
           - this is the home page of the website. Here we have a card-view of all the podcasts that are currently in the databse.
     - '/login'
           - this is where the user logs in using their email and password
     - '/register'
           - this is where the user can register an account with a username, email, password
     - '/<id>' + '/episodes/<id>'
           - this is the detailed view of the podcast stored in the database under <id>. shows a description and list of episodes
     - '/playlist'
           - this is where the list of the users favorites episodes is. named playlist because it will house a list of playlists in the future
     - '/logout'
            - logs the user out if they are logged in. redirects back to home after log out
     - '/reloadDB'
            - tells the server to go through the RSS feeds and add any new episodes that have been released. redirects back to home when finished.
     - '/favorite/<id>/<podcast>
            - adds the episode under id to the users favorite list. then redirects back to the podcast episodes page.
  
Views and Descriptions:
     - layout.html
            - this holds the nav-bar and bootstrap links, is the parent of all other views
     - home.html
            - displays a card view of all the podcasts in the database
     - login.html
            - uses wtforms to log the user in
     - register.html
            - uses wtforms to register the user and check that both passwords match-up
     - episodes.html
            - displays a detailed view of one podcast as well as the list of episodes for that podcast.
     - playlists.html
            - displays the users favorite episodes as well as a link to listen to them. 
            
 Tables and Descriptions:
      - User
          - table that holds the users. contains unique id, unique email, unique username, and a hashed password
      - Podcast
          - each entry represents a podcast. contains unique id, title, description, image, web-link, and a relationship to the episodes table
          - has a one-to-many relatioinship with episodes
      - Episodes
          - each entry is a unique episode. has unique id, title, link, audio_url, time_published, length, and the id of the podcast it belongs to (for the relationship)
      - Playlist_Episode
          - used to store which episodes has been favorited by which user.
          - has a unique id, user_id (id of the user that favorited it), episode_id (id of the episode that was favorited)
          
 References/Resrouces:
      - I did not use online templates but did use Bootstrap to style my website.
      - I used Miguel Grinberg's tutorial to learn how to implement flask-login
      - I used https://www.youtube.com/watch?v=FKy21FnjKS0&t=926s to learn how to deploy to Heroku
      
      
      
THANK YOU FOR GRADING MY PROJECT AND FOR A GREAT SEMESTER. I HOPE YOU ENJOY MY WEBSITE AND THAT YOU HAVE A GREAT WINTER BREAK!
  
