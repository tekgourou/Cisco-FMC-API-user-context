
                  fire-context                          
     For LAB only, for production use at your own risk      
       aargeris@cisco.com, alexandre@argeris.net        
  
  DESCRIPTION
  
  This python script will give you the ability to manually add or delete a user to IP passive mapping in Cisco FMC. All now mapping will    be safe in a DB call db_users_fmc.'YOUR-DOMAIN-NAME'.json. This script leverage the user agent API use by the Cisco Terminal Services (TS) Agent. 
  
  VARIABLES TO MODIFY BEFORE RUNNING THE SCRIPT
  
![image](https://github.com/tekgourou/Cisco-FMC-API-user-context/blob/master/screenshot-variables-to-change.png)  

  EXAMPLES
  
  ADDING a user/ip mapping:
![image](https://github.com/tekgourou/Cisco-FMC-API-user-context/blob/master/screenshot-fire-context-add-user-mapping.png)

  DELETING a user/ip mapping:
![image](https://github.com/tekgourou/Cisco-FMC-API-user-context/blob/master/screenshot-fire-context-delete-user-mapping.png)
  
  In your FMC you should see the following result :
![image](https://github.com/tekgourou/Cisco-FMC-API-user-context/blob/master/screenshot-FMC.png)
