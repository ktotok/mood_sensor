0. Assumptions

    Location coordinates are generated at client side as longitude and latitude.
    
    Authentification implemented as BasicAuthentication so username and password must be provided in every request to API.
    New user created by Admin
     
1. Endpoints
    - moods/ - retrieve list of available mood state 
    - mood_sense/ 
        - to upload mood state for specific location (Same location can be uploaded more than one time)
        - retrieve report how often user was 'happy', 'sad' or 'neutral'. (Would be good to implement some timeframe limit) 
                    
    - happy_location/ - retrieve list of nearest location where current user was happy 
    response items are sorted by 'distance' value in asc order
    
2. Use case

    Authentificated user upload mood sense state (based on available values) and provide geo location. 
    Also date timestamp automatically generated.   
    
    User can provide his/her current geo location and get list of nearest 'points oh happy' 
    and then decide what is the most appropriate for current moment 