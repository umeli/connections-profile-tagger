# connections-profile-tagger

Small script to tag profiles from commandline

## Usage

Add tags to a profile

```sh
python profiletagger.py

options:
  -h, --help            show this help message and exit
  -e EMAIL [EMAIL ...], --email EMAIL [EMAIL ...]

                        List of email address to update

  -a USER, --account USER

                        Admin Account User eg: admin@digitaloffice.collab.cloud

  -p PASSWORD, --password PASSWORD

                        Admin Account Passwort

  -c APIURL, --connections APIURL

                        Connections URL: https://digitaloffice.collab.cloud

  -t TAGLIST [TAGLIST ...], --taglist TAGLIST [TAGLIST ...]

                        List of tags to add

  -d REMOVE, --delete REMOVE

                        Delete Tags from the profile
```

Only Tags added by the provided user can be added or removed.
And it's probably a good idea to use an admin user to manage the tags...

## requirements

Python3

## example add tags

add the tags *collaboration* and *admin* to Salvos and Kefix profile.

```sh
python profiletagger.py  -a admin@digitaloffice.collab.cloud -p [SNIP] \
-c https://digitaloffice.collab.cloud \
-t collaboration admin \
-e salvos.aren@digitaloffice.collab.cloud \
kefix.londur@digitaloffice.collab.cloud
```

## example remove tags tags

Remove both tags

```sh
python profiletagger.py  -a connections@belsoft.ch -p [SNIP] \
-c https://digitaloffice.collab.cloud \
-d \
-t collaboration admin \
-e salvos.aren@digitaloffice.collab.cloud \
kefix.londur@digitaloffice.collab.cloud 
```
