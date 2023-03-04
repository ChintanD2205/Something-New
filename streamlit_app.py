import streamlit as st
import pandas as pd
import numpy as np

# Read the dataset
profiles = pd.read_csv("users.csv")

# Define the scoring function
def score_profile(profile):
    score = 0
    if profile['verified']:
        score += 10
    if profile['completion'] == 100:
        score += 10
    score += profile['num_likes_received']
    score += profile['num_matches_received'] * 5
    if profile['paid_subscription']:
        score += 20
    if profile['verified_user']:
        score += 5
    score += profile['num_likes_given'] - profile['num_likes_received']
    score -= profile['num_dislikes_given'] / profile['num_likes_received']
    score -= profile['num_dislikes_received'] / profile['num_likes_given']
    return score

# Compute the profile scores
profiles['score'] = profiles.apply(score_profile, axis=1)

# Define the function to fetch random profiles
def fetch_random_profiles(profile, num_profiles=10):
    # Filter by score range
    score_range = np.arange(profile['score'] - 10, profile['score'] + 10)
    filtered_profiles = profiles[profiles['score'].isin(score_range)]
    
    # Filter by latest accounts
    latest_profiles = filtered_profiles.sort_values(by='created_at', ascending=False).head(100)
    
    # Give bias to free accounts for first 24 hours
    if profile['paid_subscription'] == 'free':
        latest_profiles = latest_profiles.sample(frac=2)
    
    # Show more profiles to users with low matches
    if profile['num_matches_received'] < 3:
        latest_profiles = latest_profiles.sample(frac=2)
    
    # Fetch random profiles
    random_profiles = latest_profiles.sample(num_profiles)
    return random_profiles

# Define the Streamlit app
st.title("Profile Scoring and Fetching Random Profiles")

# Get the user input
verified = st.checkbox("Verified User")
completion = st.slider("Profile Completion", 0, 100, 0)
num_likes_given = st.slider("Number of Likes Given", 0, 100, 0)
num_likes_received = st.slider("Number of Likes Received", 0, 100, 0)
num_matches_received = st.slider("Number of Matches Received", 0, 100, 0)
paid_subscription = st.radio("Paid Subscription", ['Free', 'Paid'])
verified_user = st.checkbox("Verified User")
num_dislikes_given = st.slider("Number of Dislikes Given", 0, 100, 0)
num_dislikes_received = st.slider("Number of Dislikes Received", 0, 100, 0)

# Create the user profile
user_profile = {'verified': verified,
                'completion': completion,
                'num_likes_given': num_likes_given,
                'num_likes_received': num_likes_received,
                'num_matches_received': num_matches_received,
                'paid_subscription': paid_subscription.lower(),
                'verified_user': verified_user,
                'num_dislikes_given': num_dislikes_given,
                'num_dislikes_received': num_dislikes_received}

# Compute the user profile score
user_profile_score = score_profile(user_profile)

# Fetch random profiles based on the user profile score
random_profiles = fetch_random_profiles(user_profile, num_profiles=10)

# Show the user profile score
st.write("Your profile score is:", user_profile_score)

# Show the random profiles
st.write("Here are 10 random profiles for you:")
st.table(random_profiles)

