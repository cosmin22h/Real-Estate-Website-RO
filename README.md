# Real-Estate-Website-RO
Disclaimer: this is a real estate website dedicated to the Romanian real estate market. <br>
Backend technologies: Django, Python, PostgreSQL. <br>
Frontend technologies: Bootstrap, HTML, CSS. <br>
Objective: providing the service of real estate exposures and the service of communication between potential buyers and owners. <br>
Types of announces: apartament, house and land. <br>
Users: admin, customer, owner, real estate agency and website guest. <br>
Admin: 
  - website viewing;
  - database management (accounts and announces management);
  - send a monthly report to the real estate agencies which containts the number of contacts for each announces type.
 
Customer:
  - announces viewing;
  - add an announce to the list of favorites;
  - access and modify the list of favorites;
  - contact the owner;
  - contacts viewing;
  - account editing. 

Owner:
  - announces viewing;
  - add a request to post a new announce;
  - see the messages from potential buyers with additional details (the date and the time of a visit);
  - see the real estate agencies which are registered;
  - account editing.
  
Real estate agency:
  - see the requests from the owners;
  - announces viewing;
  - see the messages from potential buyers;
  - send the messages from potential buyers with additional details to owners;
  - see the profil;
  - see the monthly report;
  - account editing.
 
Guest:
  - announces viewing;
  - create a new account.

Create a new account - customer/owner:
  - customer type selection: customer/owner;
  - username - unique, without special characters, can’t be entirely numeric;
  - last name (nume);
  - first name (prenume);
  - phone number (telefon);
  - email - unique;
  - date of birth (data nasterii) - minimum age: 18;
  - password (parola, confirmare parola) - can’t be too similar to your other personal information, must contain at least 8 characters, can’t be a commonly used password, can’t be entirely numeric;
  - after the account is created the customer/owner can login with the username and the password.
  
 Create a new account - real estate agency: 
  - ID (CIF) - unique, must be entirely numeric;
  - name (nume);
  - logo - image file;
  - email - unique;
  - phone number (telefon);
  - address (adresă sediu);
  - establishment year (an infiintare);
  - password (parola, confirmare parola) - can’t be too similar to your other personal information, must contain at least 8 characters, can’t be a commonly used password, can’t be entirely numeric;
  - after the account is created the agency must wait until the admin approves the account, after that the agency can login with the ID and the password.
 
All types of announces have an owner, a responsible agency that handles the announce, a title, an address, a description, a price and their specific fields (see the database diagram). <br>

Project Resources (Bootstrap): https://drive.google.com/drive/folders/1Cf8zm6jNiqCbKXRv8tI2w8KEORIT6SB3
