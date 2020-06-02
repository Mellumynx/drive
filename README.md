Environment setup instructions: 
* Setup virtualbox:
    * Virtualbox setup: https://www.virtualbox.org/wiki/Mac%20OS%20X%20build%20instructions
    * Setup linux system - debian 9 (amd64): https://www.digitalocean.com/community/tutorials/how-to-install-the-latest-mysql-on-debian-9
    
* Install UI + software: 
    * settings - storage - cd(empty) - "a cd icon next to the /optical/ drive": import amd64
    * setup (first two, last two ) (clicking page) - SSH gnome
    * ...
    
* Install coding environment: 
    * python3: https://docs.python-guide.org/starting/install3/linux/
    * python flask: https://flask.palletsprojects.com/en/1.1.x/installation/
    * Visual studio code: https://linuxize.com/post/how-to-install-visual-studio-code-on-debian-9/
    * Mysql: https://www.digitalocean.com/community/tutorials/how-to-install-the-latest-mysql-on-debian-9  
        * Note: use mariadb if it showed "no installation canditate" https://unix.stackexchange.com/questions/270872/install-mysql-has-no-installation-candidate
    
    
    
Setup github repository: #description
    1. git install: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git  
    2. add projects: https://help.github.com/en/github/importing-your-projects-to-github/adding-an-existing-project-to-github-using-the-command-line 
    3. gitignore: https://git-scm.com/docs/gitignore 
    4. git clone: https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository



Database: 
    CREATE DATABASE *database-name*;

    USE *database-name*;

    CREATE TABEL *table-name*(
        *col-1* *datatype* 
        *col-2* *datatype*
        *col-3* *datatype*
    );









token 
https://pyjwt.readthedocs.io/en/latest/ 

postman
auth