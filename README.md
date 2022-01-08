# Webos-renew-dev
Renew dev mode

-----------------
Turns out there is a way easier method. I'll leave the code but but don't recommend using it.

To keep the TV in devmode, follow these steps:
1. make sure the sdk is working
2. run: `ssh prisoner@<tv IP> -p 9922 -i <key location> "/bin/sh -i"`
    -  the key is located in ~/ssh name is webos with your device name
    -  you can ignore the promting error message
3. run `cat /var/luna/preferences/devmode_enabled` and safe the prompting key
4. You can now extend the session time by sending a REST GET to: "https://developer.lge.com/secure/ResetDevModeSession.dev?sessionToken=<the key from step 3>" simply create a cronjob and your session will never expire.
5. profit
