# **WhatsApp Bot**

A WhatsApp bot designed to send newly assigned house chores, reminders, and more to your roommates, as defined in a `config.json` file.

## **Setup**

### **Contact Names & Chores**
- Store the names of contacts exactly as they appear in WhatsApp.
- Contacts and their corresponding chores are managed through the `config.json` file in servierer/.

### **Authentication**
- On first run, authenticate via a QR code.
- Subsequent logins use a locally stored Chrome profile, allowing for direct login unless manually logged out from the WhatsApp mobile app.

## **Simple Website**
- A beautiful, relaxing website is served at `/`.
- Accessible via a public domain (if purchased) or over `localhost`.
- Hosted as an independent Docker container and allows roommates to check in for their tasks.

## **Docker Compose**
- The bot communicates with other containers and feeds data to the database through Docker Compose.

## **Remarks**
- The WhatsApp bot is best run as a cron job in `/etc/cron.d/bot` under a normal user.
- Includes enhancements to minimize bot detection, along with some custom JavaScript.


#### Workflow Diagram
![image info](./cafanoble-duties.png)


## TODO

| task                                                                                                                                                                   | status |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|
| Scrape wiki-how and then send a random link based on the chore on sunday as help :)                                                                                    | done   |
| We still need the checkin logic, a small script that checks on monday evening if the link was clicked and therefore the chore is done                                  | done   |
| make it accessible from the internet. IP is already linked with no-ip, but since we have a static IP, we could also buy a domain. and configure router to port-forward | done   |
| make it headless if profile exists and otherwise with head so you can scan the QR code.                                                                                | done   |
| Pack up everything nicely as a docker image, so that we don't have this awful permission chaos etc.                                                                    | done   |
| Harden the nginx proxy server inside the container -> change config file                                                                                               | done   |
| add SSL certs with certtbot                                                                                                                                            | done   |           
## Disclaimer
This project is not affiliated, associated, authorized, endorsed by, or in any way officially connected with WhatsApp or any of its subsidiaries or its affiliates. The official WhatsApp website can be found at whatsapp.com. "WhatsApp" as well as related names, marks, emblems and images are registered trademarks of their respective owners. Also it is not guaranteed you will not be blocked by using this method. WhatsApp does not allow bots or unofficial clients on their platform, so this shouldn't be considered totally safe.
