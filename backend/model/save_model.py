import pickle
from Final import voting_model

with open("autism_model.pkl", "wb") as f:
    pickle.dump(voting_model, f)

print("Model Saved Successfully!")