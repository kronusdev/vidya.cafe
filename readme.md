# Installation

Installing vidya.cafe locally is the fastest way to get the software up and running and start tinkering under the hood.

---

# Windows

1- Install Docker on your machine.

[Docker installation for Windows](https://docs.docker.com/docker-for-windows/install/)

2- Download vidya.cafe into your machine by running this command.

```
git clone https://github.com/kronusdev/vidya.cafe/
```

3- Press shift+right click inside the vidya.cafe code folder and run PowerShell. Then in PowerShell, run the following command:

```
docker-compose up
```

4- That's it! Visit `localhost` in your browser.

5- Optional: to configure the site settings and successsfully integrate it with the external services we use (hcaptcha, cloudflare, discord, tenor and mailgun), please edit the variables in the docker-compose.yml file.

---

# Linux

1- Download vidya.cafe into your machine by running this command.

```
git clone https://github.com/kronusdev/vidya.cafe/ /vidya.cafe
```

2- Navigate to `/vidya.cafe`

```
cd /vidya.cafe
```

3- run the following command:

```
source setup
```

4- That's it. Visit `localhost` in your browser.


5- Optional: to configure the site settings and successsfully integrate it with the external services we use (hcaptcha, cloudflare, discord, tenor and mailgun), please run this command and edit the variables:

```
nano /vidya.cafe/docker-compose.yml
```
