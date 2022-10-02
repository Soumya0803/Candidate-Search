# Candidate-Search

<img src="https://user-images.githubusercontent.com/23191602/158433487-9604fe94-796b-4523-ba5f-89c26267fcf8.png" width=70%>

## Description

The program converts the input string to different queries depending on the underlying database used.
Input strings can  be converted to sql, django_orm, mongodb queries.

The input to the program can be any combination of search terms combined with AND or OR logical operators. To identify logical operators in the input they must alway be capitalized. It also support multi-word search. Multi-words in the input must be enclosed in single or double quotes.

Below are some examples.
- Java 
- Java OR python 
- (Java AND Spring) OR (Python AND Django) OR (Ruby AND ("Ruby on Rails" OR ROR))


## Project Setup

- install pipenv https://pipenv.pypa.io/en/latest/install/#installing-pipenv
- `pipenv shell`
- `pipenv install`
- `python manage.py migrate`
- `python manage.py runserver`
