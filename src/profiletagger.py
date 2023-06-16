import sys
import os
import argparse
import logging
import requests
import xml.etree.ElementTree as ET
import xml
from requests.auth import HTTPBasicAuth

# logging.basicConfig(level=logging.DEBUG,filename="profiletagger.log")
logging.basicConfig(level=logging.INFO,format='%(asctime)s %(message)s')

logger = logging.getLogger(__name__)

ET.register_namespace("snx", "http://www.ibm.com/xmlns/prod/sn")
ET.register_namespace("atom", "http://www.w3.org/2005/Atom")
ET.register_namespace("", "http://www.w3.org/2007/app")
ET.register_namespace("app","http://www.w3.org/2007/app")

def getOptions():
    parser = argparse.ArgumentParser(description="Add tags to a profile")
    parser.add_argument("-e", "--email", required=True,
                        help="List of email address to update",nargs='+',default=[],dest="email")
    parser.add_argument("-a", "--account", required=True,
                        dest="user", help="Admin Account User eg: connections@belsoft.ch")
    parser.add_argument("-p", "--password", required=True,
                        help="Admin Account Passwort")
    parser.add_argument("-c", "--connections", dest="apiurl",
                        required=True, help="Connections URL: https://conn.belsoft.ch")
    parser.add_argument("-t","--taglist",help="List of tags to add",dest="taglist",nargs='+',default=[],required=True)

    parser.add_argument("-d","--delete",help="Delete Tags from the profile",dest="remove",default=False)

    try:
        args = parser.parse_args()
        return args
    except:
        logger.error(" Error ")
        parser.print_help()
        sys.exit(1)
        return {}

def getTagUrl(options,email:str):
    logger.info(f"get Tag URL for {email}")    
    url = f"{options.apiurl}/profiles/atom/profileService.do?email={email}"    
    auth = HTTPBasicAuth(options.user, options.password)    
    response = requests.get(url, auth=auth)
    profile_content = response.content    
    tree = ET.fromstring(profile_content)
    taglinks=tree.findall(".//*[@rel='http://www.ibm.com/xmlns/prod/sn/tag-cloud']")
    tagcloud=taglinks[0]
    logger.info(f"tag url for {email} found :  {tagcloud.get('href')}")
    
    return tagcloud.get("href")
    

def getProfile(options,email:str):
    logger.info(f"update Tags for {email}")    
    tagCloud=getTagUrl(options,email)
    logger.debug(f"tag cloud url {tagCloud}" )
    auth = HTTPBasicAuth(options.user, options.password)    
    logger.info("get existing tags")
    response = requests.get(tagCloud, auth=auth)
    profile_content = response.content    
    logger.debug(profile_content)
    tree=ET.fromstring(profile_content)
    tagElements=tree.findall(".//{http://www.w3.org/2005/Atom}category")
    currentTags=[]
    logger.info("12")
    for tagElement in tagElements:
        currentTags.append(tagElement.get("term"))

    logger.info(f"Current tags for {email}: {currentTags}")
    if options.remove:
        logger.info(f"Remove tags {options.taglist}")
        for tag in options.taglist:
            tagElement=tree.find(f".//*[@term='{tag}']")
            
            if not tagElement is None:
                logger.debug(tagElement.get("term"))
                tree.remove(tagElement)
            else:
                logger.info(f"{email} has no tag {tag}")
            
    else:
        logger.info(f"Adding tags {options.taglist}")
        for tag in options.taglist:
            logger.debug(f"Add new tag: [{tag}]")
            tagElement=ET.Element("atom:category")
            tagElement.attrib["term"]=tag.lower()
            tree.append(tagElement)

    body='<?xml version="1.0" encoding="UTF-8"?>'    
    body=body+ET.tostring(tree,encoding="utf-8",method="xml").decode()
    logger.debug(f"Tags updated  {body}")
    puturl=f"{tagCloud}&sourceEmail={options.user}"
    logger.debug(puturl)
    response=requests.put(url=puturl,data=body,auth=auth)    
    
    if response.ok:
        logger.info("Tags successfully updated")
    else:        
        logger.error(f"{response.status_code},{response.reason}")
        logger.error(f"{response.content}")

    

def main():
    print("Profile Tagger 1.0")
    args = getOptions()
    if args.remove:
        logger.info("Tags will be removed")
    for mail in args.email:
        logger.info(f"Update Tags for {mail}")
        try:
            profile = getProfile(args,mail.lower())
        except:
            logger.error(f"ups da gabs einen fehler bei {mail}")
    print("done")


if __name__ == "__main__":
    main()
