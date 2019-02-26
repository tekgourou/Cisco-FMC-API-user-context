  [![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/tekgourou/Cisco-FMC-API-user-context)
  
alexandre@argeris.net        
  
  DESCRIPTION
  
  This python script will give you the ability to manually add or delete a user to IP passive mapping in Cisco FMC. All new mapping will    be save in a DB call db_users_fmc.'YOUR-DOMAIN-NAME'.json. This script leverage the user agent REST API used by the Cisco Terminal Services (TS) Agent. Description of this API can be found here : https://www.cisco.com/c/en/us/td/docs/security/ise/2-2/pic_admin_guide/PIC_admin/PIC_admin_chapter_011.html#id_38498
  
  VARIABLES TO MODIFY BEFORE RUNNING THE SCRIPT
  
![image](https://github.com/tekgourou/Cisco-FMC-API-user-context/blob/master/screenshot-variables-to-change.png)  

  EXAMPLES
  
  ADDING a user/ip mapping:
![image](https://github.com/tekgourou/Cisco-FMC-API-user-context/blob/master/screenshot-fire-context-add-user-mapping.png)

  DELETING a user/ip mapping:
![image](https://github.com/tekgourou/Cisco-FMC-API-user-context/blob/master/screenshot-fire-context-delete-user-mapping.png)
  
  In your FMC you should see the following result :
![image](https://github.com/tekgourou/Cisco-FMC-API-user-context/blob/master/screenshot-FMC.png)
