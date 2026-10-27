# this section filters the emails
import json 

def load_preferences(path="preferences.json"):  #load_preferences opens the preferences.json file
    with open(path, encoding="utf-8") as file:   #gives the file the name file, closes automatically with with
        return json.load(file)
    #load_preferences opens the preferences.json file and converts the preferences inside into a dictionary

def contains_any(text, words):
    return any(word in text for word in words)
#If AT LEAST ONE of the words in the list appears in the text, T

def check_email(email, prefs):
    text = (email["subject"] + " " + email["snippet"]).lower()
    #Combines the subject and the preview. converts to lowercase
    #no problem when searching- part time=Part time

    if not contains_any(text, prefs["topic_words"]):      # job_words -> topic_words
        return False, "not a relevant topic"

    if contains_any(text, prefs["blocked_words"]):         # bad_words -> blocked_words
        return False, "contains an unwanted word"

    if contains_any(text, prefs["wanted_words"]):          # good_words -> wanted_words
        return True, "match found"
    
    return False, "no match found"

# Only when this file is run: try the filter with sample emails
if __name__ == "__main__":
    prefs = load_preferences()  # Read the settings from the file
    #test section
    test_emails = [
        {"subject": "Part-Time Junior Web Developer", "snippet": "Enfield, student friendly"},
        {"subject": "Senior Full-Time Engineer", "snippet": "5 years experience"},
        {"subject": "Sude Mete tarafından para alındı", "snippet": "Wise payment"},
        {"subject": "Light AI Engineering Intern", "snippet": "London office"},
    ]

    for email in test_emails:
        decision, reason = check_email(email, prefs)  # Take the two values separately: decision and reason
        print(decision, "|", reason, "|", email["subject"])