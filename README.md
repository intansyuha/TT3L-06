Reveluxe - Outfit Building Website

Overview

Reveluxe is a modern web application designed to help users mix and match clothing items to 
build stylish outfits. The platform provides an intuitive interface that allows users to explore 
fashion trends, create their own outfits, and share their creations. Whether you're planning your 
wardrobe for the week or curating looks for a special event, Reveluxe offers an immersive 
experience for fashion enthusiasts.

Features

- Outfit Creator: Users can drag and drop clothing items to build and visualize outfits.

- Style Recommendations: Personalized suggestions based on the user’s outfit preferences.

- Clothing Library: A database of various clothing items, categorized by type (tops, bottoms, accessories, etc.).

- Responsive Design: Optimized for both desktop and mobile views.

- Social Sharing: Users can share their outfit ideas via social media.


Technologies Used

Frontend:

- HTML5: Structure and layout of the web pages.

- CSS3: Styling for the web pages, ensuring a modern and appealing design.

- JavaScript: For interactivity, including the drag-and-drop functionality of the outfit builder.


Backend:

- Python: Handles server-side logic, user authentication, and the processing of requests.

- SQLite: A lightweight database used to store user information, outfits, and clothing items.

- DB Browser for SQLite: Used for managing the SQLite database during development.


Installation Guide

To run the project locally, follow these steps:

1. Clone the repository:
   git clone https://github.com/intansyuha/TT3L-06.git
   cd TT3L-06

2. Set up a Python virtual environment (optional but recommended):
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate

3. Install the required Python packages:
   pip install -r requirements.txt

4. Set up the SQLite database:
   Make sure the database file (reveluxe.db or similar) is properly configured in your project.
   If it's not present, you can use DB Browser for SQLite to create it and set up the necessary
   tables for users, clothing items, and outfits.

5. Run the backend server:
   python app.py

This will start the backend server, typically accessible at http://localhost:5000.

6. Open the frontend:
   Open the index.html file in a browser to interact with the frontend.

Usage

Once the app is running, users can:

- Sign up or log in to their account.
  
- Browse through the clothing categories.

- Use the drag-and-drop interface to create and save custom outfits.

- Get personalized style recommendations based on the available clothing.
