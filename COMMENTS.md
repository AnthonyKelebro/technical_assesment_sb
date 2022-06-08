# Comments to tasks
## python_cli_tool
The script is not big but I think it would be even smaller if I wrote it in bash. By the way in bash I would use tools such as __sed__, __find__, __lsstat__ and array with the cycle inside the script.

But for example if we need to extend the script with new functions in the future then bash will definitely lose out. So because of that I use python. I should also note that it uses a very simple directory handling mechanics, which we pass as an argument and the script looks only inside this directory BUT without considering sub-directories. To support such functionality I would use recursion algorithm to cover all sub-directories and files with additional granularity option.

The cli-tool works in two modes, as a normal rename tool and in debug mode, where all files are created by the tool itself in a temporary folder that is deleted after input from the user.

P.S. You could add */usr/bin/env python* to the script to remove the first part of the launch, but it usually gets blamed by linter, so I left it with the standard use as much as possible.

P.S.S. You may also be stung by the fact that all code uses f-string's, but the logger uses %s format. This is due to the fact that there is a wish from the creators of the library logging to use their module this way, because f-string when scaling can lead to loss of performance (And as I remember linter in default configuration give error).

## docker
No special comments here, everything is done by tech assessment. The only thing is that ElastickSearch and Kibana version is the previous one, because in new version 8 there are problems with user data transfer for ElastickSearch and Kibana bundle when running this pipeline in docker-compose. You need to use a token there and essentially need to play around with a little crutch to do it. And one more thing after all operation with docker-compose need wait some time for filebeat initialization.

## ansible
There are no specific comments here either. 
The only thing is that the repository was created simply, but with the ability to expand immediately into a larger repository with support for various mechanisms, including [tags] to manually call specific playbook steps. I did not use the default vault to protect credentials, as this is a test repository. 

The playbook was tested on Ubuntu versions 18.04, 20.04 and 22.04.
