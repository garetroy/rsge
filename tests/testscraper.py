import sys
sys.path.append("../src/")

from scraper import Scraper

scraper = Scraper()
assert (scraper.getItem(2) != {}), "Got an item"
assert (scraper.getItem(k) == {}), "Caught wrongful item"
print("Base scraper is working")
