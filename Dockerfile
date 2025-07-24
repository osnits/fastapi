#specify the base image 
FROM python:3.9.7

#technically optional -> from where run all commands 
WORKDIR /usr/src/app

#copy our requirements from local machine
#"./" is a shortcut for our WORKDIR above
COPY requirements.txt ./

#run command for installing dependencies 
RUN pip install --no-cache-dir -r requirements.txt

# copy everything from our app directory to current directory of container
COPY . . 

#run this command when we start this container, we break up each line word of the command wherever you have a space in command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]