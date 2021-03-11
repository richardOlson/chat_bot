# This is pulled from the git repo of https://github.com/dimitrismistriotis/profanity-check

import pkg_resources
import numpy as np
import joblib

vectorizer = joblib.load(pkg_resources.resource_filename('profanity_check', 'data/vectorizer.joblib'))
model = joblib.load(pkg_resources.resource_filename('profanity_check', 'data/model.joblib'))

def _get_profane_prob(prob):
  return prob[1]

def predict(texts):
  return model.predict(vectorizer.transform(texts))

def predict_prob(texts):
  return np.apply_along_axis(_get_profane_prob, 1, model.predict_proba(vectorizer.transform(texts)))




if __name__ == "__main__":
  s = "Blacks don't look good in blue clothes, just kidding they look great."
  t = "I love dogs."

  print(f"Trying the functions to see how well this is working")
  print("Predicting for s  " , predict([s]))
  print("Predicting for t  ", predict([t]))
  print("Predict proba for s  ", predict_prob([s]))
  print("Predict proba for t   ", predict_prob([t]))
  