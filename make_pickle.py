import pickle

obj = {"user": "Kumar", "role": "tester", "n": 123}
with open("data.pkl", "wb") as f:
    pickle.dump(obj, f)
print("data.pkl created")