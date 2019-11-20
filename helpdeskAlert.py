import requests
import lxml
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from pygame import mixer
import schedule
import os
# python -m pip install plyer
from plyer import notification


TICKET = ""



def notify(title, message):
  notification.notify(
      title=title,
      message=message,
      app_icon=None,  # e.g. 'C:\\icon_32x32.ico'
      timeout=10,  # seconds
  )


def crawlSite():
  url = "https://webservices.ulm.edu/computersos/helpdesk-dashboard"

  soup = urlopen(url)

  content = bs(soup, 'lxml')

  # ticked id's
  helpdesk_tickets_id_container = "views-field views-field-nid"

  # last activity
  last_activity = "views-field views-field-last-comment-timestamp"

  # specifier for helpdesk
  helpdesk = "block-views-helpdesk-tickets-block"

  # this will limit our search to helpdesk tickets only
  data = content.find("div", {"id": helpdesk})

  # get all ids for helpdesk
  ids = []

  gids = data.findAll("td", {"class": last_activity})

  for id in gids:
    ids.append(id.get_text().strip())
    
  return ids


# get current ticket 
def current_ticket(tickets):
  current = (tickets)[0]
  return current

def controller():
  ids = crawlSite()

  current = current_ticket(ids)
  global TICKET
  if current != TICKET:
    play_sound()
    notify("New Upate", "You have new update on a ticket")
      
  TICKET = current

  
  print(current)



# PLAY SOUND WHENVER THE NEW TICKET GETS IN
def play_sound():
    """Plays the sound when there is new ticket"""
    mixer.init()
    mixer.music.load('update.mp3')
    mixer.music.play()


# main method
def main():
  current = current_ticket(crawlSite())

  schedule.every(10).seconds.do(controller)
  while True:
      schedule.run_pending()
main()
