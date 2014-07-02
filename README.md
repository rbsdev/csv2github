csv2github - Conversion from Google Docs (CSV files) spreadsheet to Github issues
==========

This project is simple collection of scripts to convert a list of tasks 
(with hours assigned to persons) to Github issues. 

Running
==========
Just run informing your task list file:
```python docs2github.py tasks.csv```

Sample of task file
==========
You can create the list of taks using Google Docs and then export to
a CSV file. 
Sample:

Note that here we create user stories with subtasks, all of which will
be issues in your repository with different tags. 

If only one person is assigned to the task, the issue will be assigned
to the corresponding user.

config.py
==========
Is important that you configure your Github repo parameters in the configuration
file.

```
github_api_token = 'set_your_githup_api_token'

# CHANGE THIS AT EACH SPRINT
milestone = '1'

owner = 'gustavofuhr'
repo = 'beatles_software'

usernames_map = {
    'ringo': 'ringoisthebest',
    'john': 'johnnythezombie',
    'paul': 'mcpaul',
    'george': 'george',
}
```

- ```repo```: is the repo name in github
- ```usernames_map```: maps the names used in the task table with the usernames in github

========
That's all folks! Enjoy! 

