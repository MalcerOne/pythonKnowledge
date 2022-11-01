#!/usr/bin/env python
"""
This program is a simple scraper of coursera course data.
"""

# Import necessary modules
import requests, re
from bs4 import BeautifulSoup
from progress.bar import IncrementalBar
import pandas as pd


# Infos about the program
__author__     = "Rafael Malcervelli"
__maintainer__ = "Rafael Malcervelli"
__email__      = "r.malcervelli@gmail.com"

# Class that will scrape the data from the website
class Scraper: 
    def __init__(self, url):
        self.url     = url
        self.soup    = self.get_soup()
        self.courses = self.get_courses()

    def get_soup(self):
        response = requests.get(self.url)
        soup     = BeautifulSoup(response.text, 'html.parser')
        return soup

    def get_courses(self):
        courses = self.soup.find_all('a', class_='CardText-link')
        return courses

def main(category_raw):
    list_courses = []
    dic_aux      = {}
    category = category_raw.lower().replace(" ", "-")
    print("\n[+] Scraping category: ", category)
    url = f'https://www.coursera.org/browse/{category}'

    # Initializing the scraper
    scraper = Scraper(url)
    courses = scraper.courses

    with IncrementalBar('Scraping', max=len(courses)) as bar:
        for course in courses:
            # This is to avoid scraping the projects, only the courses
            if "projects" in course.get('href'): 
                continue
            url_course = "https://www.coursera.org" + course.get('href')
            scraper_course = Scraper(url_course)

            try:
                # Getting the course data
                course_name            = scraper_course.soup.find('h1').text
                first_instructor_name  = scraper_course.soup.find('h3', class_="instructor-name headline-3-text bold").text
                course_description     = scraper_course.soup.find('div', class_="description").text.strip() 
                n_of_students_enrolled = re.sub('[^0-9,]', "", scraper_course.soup.find('div', class_="rc-ProductMetrics").text)
                n_of_ratings           = re.sub('[^0-9,]', "", scraper_course.soup.find('div', class_="_1srkxe1s XDPRating").text.split("stars")[1])
            
            except Exception as e:
                if e == AttributeError:
                    n_of_ratings = "None"
            # Creating a dictionary with the course data
            dic_aux['Category Name']          = category
            dic_aux['Course Name']            = course_name
            dic_aux['First Instructor Name']  = first_instructor_name
            dic_aux['Course Description']     = course_description
            dic_aux['# of Students']          = n_of_students_enrolled
            dic_aux['# of Ratings']           = n_of_ratings
            list_courses.append(dic_aux)
            dic_aux = {}
            bar.next()

    return list_courses

if __name__ == "__main__":
    # Create a category object
    CATEGORIES_CHOICES = {'data-science':'Data Science',
    'business': 'Business',
    'computer-science':'Computer Science',
    'personal-development':'Personal Development',
    'language-learning':'Language Learning',
    'information-technology':'Information Technology',
    'health':'Health',
    'math-and-logic':'Math and Logic',
    'physical-science-and-engineering':'Physical Science and Engineering',
    'social-sciences':'Social Sciences',
    'arts-and-humanities':'Arts and Humanities'}

    print("[?] Please, choose a valid category from the list below:\n")
    print(list(CATEGORIES_CHOICES.values()))

    category = input("[?] Category: ")
    while category.lower().replace(" ", "-") not in list(CATEGORIES_CHOICES.keys()):
        print("[!] Invalid category, please, try again.")
        category = input("\n[?] Category: ")
    
    courses = main(category)
    df = pd.DataFrame.from_dict(courses)
    df.to_csv(f'{category.lower().replace(" ", "_")}.csv', index=False)