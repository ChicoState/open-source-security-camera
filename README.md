[![Python application](https://github.com/ChicoState/open-source-security-camera/actions/workflows/actions.yaml/badge.svg)](https://github.com/ChicoState/open-source-security-camera/actions/workflows/actions.yaml)
# open-source-security-camera
(raspberrypi OpenCV setup and partitioning)[https://qengineering.eu/install-opencv-4.5-on-raspberry-pi-4.html]
## Team Members

- [Meher Lippmann](https://www.github.com/melippmann)
- [Kevin Douglass](https://www.github.com/kevdouglass)
- [Cameron Watts](https://www.github.com/Zalymo)
- [Avery Pound](https://www.github.com/DJ-IRL)
- [Connor Ganaway](https://www.github.com/ConnorGanaway)

---

## Project description
This project is to develop an open source home security solution that puts user data rights and privacy at the core of the development processes.

---

## Docker
From Docker homepage:
> "Docker Engine is an open source containerization technology for building and containerizing your applications. <br>
> Consistent environments ( Solves "It works on my machine" problem) <br>
> Sandboxing (isolates the environment for each docker container) Makes deploying software across <br>
> multiple environments much easier. <br><br>
> Docker Image <br>
> "Includes everything needed to run an application <br>
> the code or binary, runtimes, dependencies, and any other filesystem objects required"<br>
> Docker images are created via a "Dockerfile", <br>
> which is a script file containing the steps to create that image's configuration.<br>
> A docker container is an instance of a docker image, which may be running (or not) <br>
> Docker image vs Docker Container === Class vs Objec <br>


### build command & naming convention

`docker build -t <your_name>/<your_machine>:osCam_latest .`

*note: everything after the `:` should be consistent across all our builds*
ex:

`docker build -t ave/local:osCam_latest .`

### running container

docker run -it -p 80:80 `<container_name>`

expected output:
```bash
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
March 16, 2022 - 18:15:46
Django version 4.0.3, using settings 'osCam.settings'
Starting development server at http://0.0.0.0:80/
Quit the server with CONTROL-C.
```

view running container via `127.0.0.1` in your browser <br>

### tips and tricks <br>
view all docker images <br>
`docker image ls` <br>

remove *a single* docker image <br>
`docker image rm <image_name>` <br>

remove *all* containers and images <br>
`docker system prune -a` <br>

### Running the Application <br>

To begin, OpenCV will need to be installed on the Raspberry Pi to make use of the motion detection feature. Run the following commands to enable and run this. *Note: This process will take around 2 hours to complete. *

```
chmod +x OpenCV-4-5-5.sh
./OpenCV-4-5-5.sh
```

Once OpenCV is installed, run the following commands to enable access to the startup script and run it.

```
chmod +x run.sh
./run.sh
```

The ```./run.sh``` will be used to start the application every time.

### Stopping the Application <br>

Hold Ctrl-C to stop the dashboard. Next type the following command to list the current running processes:

```
ps
```

From here type the following command followed by the process listed as "Python3". This will stop the motion detection script from running.

```
kill <PID Number>
```

### Sending Emails <br>

While running this script, it will prompt if you want to configure using your email to send notifications. To enable this feature, it will ask for a secrete key to have access to send from your email address. To generate the secret key follow these steps:

1. [Enable Less Secure Apps with your gmail account](https://myaccount.google.com/lesssecureapps)
2. Make sure two-factor authentication is enabled.
3. To get the secret key, you can do this by going to the [Security section](https://myaccount.google.com/security) of your google account, scrolling down to the Signing in to Google section, and clicking on App passwords
4. Click select app and choose a custom name for the app password such as "Security Camera Notifications". Then click generate.
5. A new window will show a 16 character password. Copy this and replace it where "secret_key" is.
6. Remove any spaces shown in the generate app password. (Instead of "abcd efgh ijkl mnop" use "abcdefghijklmnop")

---
### Database Design:
[ER Diagram.pdf](https://github.com/ChicoState/open-source-security-camera/files/8346569/ER.Diagram.pdf)
