# Webos-renew-dev

-----------------
Turns out there is a way easier method than using the script in this repository. I'll leave the code but I don't recommend using it. The way, I recommend using to get renew is as following: 

## Getting your key: 
### Via SSH:
1. make sure the sdk is working, and your TV is added
2. run: `ssh prisoner@<tv IP> -p 9922 -i <key location> "/bin/sh -i"`
    -  the key is located in ~/ssh name is webos with your device name
    -  you can ignore the promting error message
    -  the password for the private key should be the passcode you used to register the tv in your sdk
3. run `cat /var/luna/preferences/devmode_enabled` and save the token


### Via webOS Dev Manager (https://github.com/webosbrew/dev-manager-desktop): 
1. select your TV and go into the Files menu
2. open `/var/luna/preferences/devmode_enabled`
3. copy the token

## Extending the devmode period
1. You can now extend the session time by sending a REST GET to: `https://developer.lge.com/secure/ResetDevModeSession.dev?sessionToken={token}>` simply create a cronjob and your session will never expire.
2. profit


## Checking devmode remaining period
With both methods, the TV seems to not update reliably. 
You can check it with a REST GET request to `https://developer.lge.com/secure/CheckDevModeSession.dev?sessionToken={token}`.

