# Voice_Assistant

Command to run the code
'''
uvicorn main:app --reload
'''


--commands to run locally using docker
docker build -t interviewassist .
docker run -p 8080:8080 interviewassist
--open http://localhost:8080/ in the browser


--commands to push the image to ECR
---Authenticate Docker with your AWS credentials.
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 021891609648.dkr.ecr.us-east-1.amazonaws.com

--build docker image
docker build -t interviewassist .

--tag the image
docker tag interviewassist:latest 021891609648.dkr.ecr.us-east-1.amazonaws.com/interviewassist:latest

--push the image
docker push 021891609648.dkr.ecr.us-east-1.amazonaws.com/interviewassist:latest