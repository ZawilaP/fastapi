from fastapi import FastAPI, Query, Path
from typing import Annotated

app = FastAPI()

books_inventory={'title1': 7, 'title2': 3, 'title3': 1} # contains books that we have, might or might not be rented! 
rentals = {'title1': ['member1', 'member2'], 'title3': 'member7'}
# Create a REST API for the library!
# Required methods:
# - check if book exists in inventory
# - list current rentals
# - check if book can be rented
# Remember to validate your inputs - we know that titles are not >50 chars long