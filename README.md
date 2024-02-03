# Hyperion Remote Control
A Telegram bot to control Hyperion ambilight 🎉

The Hyperion Remote Control script leverages the Hyperion project, enabling users to control and customize their ambient lighting experience. Integrated with a Telegram bot, the script allows users to command Hyperion functions.

## What is Hyperion
Hyperion is an open-source project designed to enhance the viewing experience by synchronizing ambient LED lighting with on-screen content. It utilizes a Raspberry Pi or similar hardware to control individual LEDs placed around a TV or monitor. Hyperion analyzes the screen content in real-time, creating dynamic lighting effects that extend beyond the display.

#### Key Features
1. **Real-time Synchronization:** Dynamically adjusts LED lighting based on on-screen content.
2. **Customization:** Offers extensive customization options for brightness, color, and effects.
3. **Open Source:** Being an open-source project, Hyperion encourages community contributions and modifications.

#### Ambilight by Philips
Ambilight, developed by Philips, is a proprietary ambient lighting technology integrated into certain Philips TVs. It works by extending the on-screen colors to LED lights on the TV's rear, providing an immersive and dynamic viewing experience. Ambilight is tightly integrated with Philips TVs, creating a cohesive visual ambiance.

#### Key Features
1. **Integrated System:** Ambilight is a built-in feature in select Philips TVs, creating a seamless integration with the viewing experience.
2. **Immersive Lighting:** Extends on-screen colors to the surroundings, offering an immersive and engaging atmosphere.
3. **Brand Specific:** Limited to Philips TVs and specific models.

#### Comparison

- **Open Source vs. Proprietary:** Hyperion is open-source, allowing for customization and adaptation to various hardware configurations. Ambilight is proprietary and exclusive to Philips TVs.

- **Hardware Requirements:** Hyperion is versatile and can be implemented on Raspberry Pi or similar hardware. Ambilight is specific to Philips TVs equipped with Ambilight technology.

- **Customization:** Hyperion offers extensive customization options, while Ambilight's features are tailored to work seamlessly with Philips TVs.

# Installation of Hyperion Remote Control
### Installation of Hyperion:
- GitHub repo of Hyperion: [Hyperion](https://github.com/hyperion-project/hyperion.ng)
- GitHub repo of HyperBian (for Rasbian OS): [HyperBian](https://github.com/hyperion-project/HyperBian/)
- Documentation of Hyperion: [Doc](https://docs.hyperion-project.org/)
- Forum of Hyperion: [Forum](https://hyperion-project.org/forum/)
- [Yes it's me](https://hyperion-project.org/forum/index.php?thread/13069-contr%C3%B4le-%C3%A0-distance-sans-me-lever-du-canap%C3%A9-ou-devoir-allumer-mon-ordi-ou-me-con/)

Video tutorial (in French but I'm sure you can find information on internet):
- https://www.youtube.com/watch?v=eIfdLJi3Gvs
- https://www.youtube.com/watch?v=F4XjuX7yn3g

### Installation of Hyperion Remote Control

There is a good chance that my script will not work depending on the hardware you used to build your Hyperion. Here are my characteristics:
- Raspberry Pi 3
- LED: [APA102](https://fr.aliexpress.com/item/4000340545026.html?spm=a2g0o.order_list.order_list_main.30.6aeb5e5bH8csxe&gatewayAdapt=glo2fra)
- Video acquisition: [LINK](https://fr.aliexpress.com/item/4000917130635.html?spm=a2g0o.order_list.order_list_main.35.6aeb5e5bH8csxe&gatewayAdapt=glo2fra)
  - Encoding format: YUYV

*Note* :You need to create an account on [Telegram](https://web.telegram.org/k/)

On the device where you install Hyperion:

1. Install [Telepot](https://github.com/nickoala/telepot):
    ```
    pip install telepot
    ```
    (For Raspberry only) Install [gpiozero](https://gpiozero.readthedocs.io/en/latest/):
    ```
    pip install gpiozero
    ```
2. Extract ```HRC.zip``` where you want → [Release](https://github.com/Jumitti/hyperion-remote-control/releases)
   - (For Raspberry) Don't forget to give all permissions at ```HRC``` folder:
     - In ```HRC``` folder, open a terminal:
     ```
     sudo 777 hyperion_remote_control.py
     sudo 777 SECRETS.py
     ```
3. Config ```SECRETS.json``` in ```HRC``` folder

   - How to get your **ID**:
     - send ```/getid``` to [myidbot](https://telegram.me/myidbot) on [Telegram](https://web.telegram.org/k/)
     - Copy/paste your ID in ```SECRETS.json``` without (') or (")
   
   - How to get your **TOKEN**:
     - Config a bot with [@BotFather](https://telegram.me/BotFather):
       - Create a bot with ```/newbot``` and follow instructions
       - Get API token with ```/mybots```, select your bot and get API token
       - Copy/paste your token in ```SECRETS.json``` between (') or (")
     - Don't forget to send ```/start``` at your Telegram bot
4. Run ```hyperion_remote_control.py```:
   - In ```HRC``` folder, open a terminal:
     ```
     python3 hyperion_remote_control.py
     ```
5. That all folks ! You just received a message on your Telegram bot ! 🎉

6. (Bonus Raspberry) For start ```hyperion_remote_control.py``` at boot:
    - In a terminal:
      ```
      sudo nano /etc/rc.local
      ```
    - You need to see that:
      ```
      #!/bin/sh -e
      #
      # rc.local
      #
      # This script is executed at the end of each multiuser runlevel.
      # Make sure that the script will "exit 0" on success or any other
      # value on error.
      #
      # In order to enable or disable this script just change the execution
      # bits.
      #
      # By default this script does nothing.
    
      # Print the IP address
      _IP=$(hostname -I) || true
      if [ "$_IP" ]; then
        printf "My IP address is %s\n" "$_IP"
      fi
    
      exit 0
      ```
    - Add ```sudo -u {user} python3 {YOUR_PATH}/HRC/hyperion_remote_control.py &``` before ```exit 0```:
      - In my case, user = pi and path = /home/pi/Desktop
        ```
        #!/bin/sh -e
        #
        # rc.local
        #
        # This script is executed at the end of each multiuser runlevel.
        # Make sure that the script will "exit 0" on success or any other
        # value on error.
        #
        # In order to enable or disable this script just change the execution
        # bits.
        #
        # By default this script does nothing.
    
        # Print the IP address
        _IP=$(hostname -I) || true
        if [ "$_IP" ]; then
          printf "My IP address is %s\n" "$_IP"
        fi
    
        sudo -u pi python3 /home/pi/Desktop/HRC/hyperion_remote_control.py &
    
        exit 0
        ```
    *Note*: You can use ```crontab``` way but I don't like it

# How to use Hyperion Remote Control

## NEWS from [HRC v1.0](https://github.com/Jumitti/hyperion-remote-control/releases/tag/v1.0)
A keyboard with all options is available. You can also change the brightness and apply colors or effects.

*Note*: The functions are also accessible as commands (see **List of commands** section below). A description is associated with it.
<div style="text-align:center">
    <p float="left">
      <img src="img/menu.jpg" width="100" />
      <img src="img/brightness.jpg" width="100" /> 
      <img src="img/effects.jpg" width="100" />
    </p>
</div>

## List of commands
Just send ```/help``` to your Telegram bot and see all command ! 😊

*Tips*: you can set command from ```/help``` with [@BotFather](https://telegram.me/BotFather) to have a quick access
- copy message from ```/help```
- send ```/mybots``` to [@BotFather](https://telegram.me/BotFather) and select your Telegram bot
- select ```Edit Bot```
- select ```Edit Commands```
- paste message from ```/help``` without /

| Command         | Description                                         | Raspberry | Windows |
|-----------------|-----------------------------------------------------|-----------|---------|
| `/temperature`  | Get CPU temperature                                 | ✅         | ❌       |
| `/quick_update` | To update and upgrade without autoremove and reboot | ✅         | ❌       |
| `/update`       | To update, upgrade, autoremove AND REBOOT           | ✅         | ❌       |
| `/reboot`       | Sometimes it's good                                 | ✅         | ❌       |
| `/shutdown`     | As expected                                         | ✅         | ❌       |
| `/hyperion_on`  | Turn on Hyperion                                    | ✅         | ✅       |
| `/hyperion_off` | Turn off Hyperion                                   | ✅         | ✅       |
| `/video_on`     | Hyperion based on video input                       | ✅         | ✅       |
| `/video_off`    | Hyperion background effect/color                    | ✅         | ✅       |
| `/brightness`   | Manage brightness                                   | ✅         | ✅       |
| `/effect`       | Select color/effect                                 | ✅         | ✅       |
| `/test`         | Is my Telegram bot still working?                   | ✅         | ✅       |
| `/help`         | A little reminder                                   | ✅         | ✅       |

Hyperion can make heat your Raspberry, so to prevent an overheat I had a command to know CPU temperature:
- In ```hyperion_remote_control.py```, you can set critical temperature, replace "85" and "90":
    ```
    if temperature >= 85:
        bot.sendMessage(chat_id_key, f'WARNING ! CPU temperature too hot{temperature}')
    if temperature >= 90:
        bot.sendMessage(chat_id_key,
            f'WARNING ! CPU temperature too hot{temperature}.\nShutdown in progress... See U soon')
        os.system('sudo shutdown now')
    ```

I add a function to auto-update your Raspberry every monday @ 02:30 and major update with reboot appends every 1st of each month @ 02:00, you can change that:
- Day: M=0; T=1; W=2...
    ```
    # Quick update every monday @ 2:30
    if day == 0 and hour == '02:30':
        bot.sendMessage(chat_id_key, 'Starting weekly update...')
        os.system('sudo apt-get update -y')
        bot.sendMessage(chat_id_key, 'Weekly update done.\nStarting weekly upgrade...')
        os.system('sudo apt-get upgrade -y')
        bot.sendMessage(chat_id_key, 'Weekly upgrade done')
    
    # Update every 1st of month @ 2:00
    if date == '1' and hour == '02:00':
        bot.sendMessage(chat_id_key, 'Starting monthly update...')
        os.system('sudo apt-get update -y')
        bot.sendMessage(chat_id_key, 'Monthly update done.\nStarting monthly upgrade...')
        os.system('sudo apt-get upgrade -y')
        bot.sendMessage(chat_id_key, 'Monthly upgrade done.\nStarting monthly autoremove...')
        os.system('sudo apt-get autoremove -y')
        bot.sendMessage(chat_id_key, 'Monthly autoremove done.\nStarting reboot...\nSee U soon')
    ```

# Can I use my own command ?

Yes of course, my script use JSON commands. Documentation [HERE](https://docs.hyperion-project.org/en/json/Control.html#sections)

Feel free to create your own Telegram bot with your own command 😊 My script is just a proof of concept 😊

# A Telegram Bot is secure ?

Yes it is if you don't create a public bot. When in doubt, you put your token and your ID in a SECRETS.json file. So your identifiers are not written in the script. In addition, I added a function that prevents commands from an unrecognized ID from being executed. A prevention message is sent to the unrecognized ID. And a message will be sent to you to warn you in this case with the ID trying to communicate with your Telegram Bot. 

# Disclaimer
This project is an independent initiative for enhancing the Hyperion experience and is not affiliated with the official Hyperion project or Philips Ambilight.
