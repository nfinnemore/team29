Feature: Login
Rule: User must already have an account
Example: Good Login with correct credentials
Given user already has an account
When the user enters their username and password
Then the login will be accepted
And they will be brought to the homepage
Example: Bad Login with bad credentials
Given user already has an account
If the username or password is incorrect
Then the login will be denied
And the user will be redirected to the login page


Feature: Registration
Rule: User must not have an account
Example: Good registration with new username not already existing
	Given user does not have an account
	When the user enters new account’s username
	And theUsername is accepted
	Then User is brought to the homepage.

Example: Bad registration with username already existing
	Given user does not have an account
	If the user enters a an existing username
	Then username will be denied
	And user will be asked to try another username

Example: Good registration with password having at least one uppercase letter, one lowercase letter and a number.
	Given user enters a password matching the criteria
	When user enters new account password
	And the Password matches criteria
	Then User account is made and 

Example: Bad registration with password not matching criteria
	Given user enters a password that does not match
	If the user enters new password
	And the password does not match criteria
	Then User account will not be made
	

Feature: View Projects
	Example: Given a user has logged in
		If the user has any projects or not
			When the user clicks on the view projects link
Then the user can see a list of projects

  
Feature: Edit project
Example: User selects project to edit
	Given user clicks an existing project
	And they have access to it
	Then user is able to upload changes
