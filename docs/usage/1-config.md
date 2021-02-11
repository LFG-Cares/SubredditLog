# Initial Configuration

After logging in with your super user account, head over to the admin panel, which is available by navigating to 
`/admin`, for example https://subredditlog.example.com/admin. You should see a screen like this:

![Django Admin](django_admin.png "Django Admin screen")

## Site Configuration

Your SubredditLog installation can be configured by clicking on "Config" in the "Constance" section. Here, you can 
configure the name of your subreddit and whether you want the modlog to be publicly accessible.

![Site Configuration](config.png "/r/BaldursGate3's Config")

Add your subreddit's name, uncheck the box next to PUBLIC_MODLOG if you want it to be private, and click Save.

## Setting the Rules

Your subreddit has rules, so they need to be defined here, too.

In the admin panel, under Entries, click on Rules. Here, you can add, edit, and order rules to match your subreddit.

To add a rule, click the Add Rule button in the top right corner.

![Add Rule Form](add_rule_form.png "The 'Add Rule' form")

Enter the title and description of your rule, then click Save.

### Reordering Rules

You can reorder rules to match your subreddit's rule order by clicking on the arrows to the right of the rules.

### Editing and Deleting Rules

Rules can be edited by clicking on the Order Number of the rule.

Rules can be deleted by checking the box next to the rule, then selecting "Delete selected rules" from the action box
and clicking "Go".

![Rules List](rules_list.png "The rules list")

## Fellow Moderators

Your fellow moderators need accounts, so let's create them. Click on "Users" then click "Add User" in the top right.

!!! info Please note that only moderators should have accounts, as anyone with an account can submit new moderator actions.

![Add User](add_user.png "The 'Add User' screen")

Enter the moderator's Reddit username and give them a temporary password (you can use [NuPass](https://nupass.pw) to 
generate easy to read temporary passwords). You can then privately message these credentials to the mod.

### Making Other Super Users

By default, the new accounts created for your mods will not be able to access the admin panel, so cannot edit actions or
update the Site Configuration. If you'd like them to be able to do so, you'll need to be enable Staff and Superuser
status for the account.

The edit user screen is displayed after creating a user, but can also be reached by clicking on the user's name in the 
Users screen.

![Edit User](edit_user.png "The 'Edit User' screen")

Check both boxes, scroll down, and click Save.

