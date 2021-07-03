# :test_tube: Flask app

This is in the context of [stacks](https://github.com/algorinfo/stacks)


## :monocle_face: FAQ

### How I use this ? 

You have at least two options:
1. Clone the repo with the new name that you want and run rename.sh script:

```
git clone https://github.com/algorinfo/flask_template/ <my_new_folder>

# Check before what is there:
cat rename.sh
./rename <my new name>
```

What is happening?
Well, this script change all the words `changeme` and `CHANGEME`. Also move some files and folder to the new name. 
Be aware that this script copies `.env.example` to `.envrc` so if you are using [direnv](https://direnv.net/) (I highly recommend that) then a warning message should be expected.

### What happens If I run more than one ?

A `.changeme` file exist in the root of the project, when the script runs the first time it checks for that file. If the file no longer exist, then the assumption is that the change was already made. 

:rotating_light: If you don't feel confortable with bash scripting, maybe it's better that you delete `rename.sh`

### Why you are not using cookie-cutter?

To be honest, I tried but it seems too complicate for this use case. Also I saw some repos before and it's difficult for me understand how the template code works. 

Instead, in this way you can see real code, no strange jinja placeholders, I the code can be tested in the github repo itself 

Also this is not a final version, some other features could be expected or some dependencies must be updated and I couldn't figure out how a cookie cutter template should grow. 

Maybe I lost some features like an option to template a blueprint or something like that, but if I really need that kind of stuff should be easy to implement using the already jinja2 installed.


## :fire: Features

- Prometheus exporter
- SQLAlchemy (NOT-Flask-Sqlalchemy) 
- Basic auth implemented
- Factory and Blueprint patterns
- docker-compose for a quick dev environment
- Dockerfile
- pytest setup


## :pushpin: References
metric endpoint
[Prometheus plugin](https://github.com/rycus86/prometheus_flask_exporter)
