import itertools
import pandas as pd
from sklearn.cluster import KMeans
import numpy as np

zaryüzü = 6
liste = [i + 1 for i in range(zaryüzü)]
dice = set()

for p in itertools.combinations_with_replacement(liste, zaryüzü):
    if sum(p) == sum(liste):
        dice.add(tuple(sorted(p)))

print(len(dice))
dice = list(dice)
print(dice)
results = {}
for i in range(len(dice)):
    for j in range(i, len(dice)):
        zarlar1 = dice[i]
        zarlar2 = dice[j]
        results[(zarlar1, zarlar2)] = [0, 0]
        total_outcomes = 0
        for roll1 in zarlar1:
            for roll2 in zarlar2:
                if roll1 > roll2:
                    results[(zarlar1, zarlar2)][0] += 1
                elif roll2 > roll1:
                    results[(zarlar1, zarlar2)][1] += 1
                total_outcomes += 1
        results[(zarlar1, zarlar2)] = [results[(zarlar1, zarlar2)][0] / total_outcomes, results[(zarlar1, zarlar2)][1] / total_outcomes]


zarlar = [f" {i + 1}" for i in range(len(dice))]
fikstur_matrisi = pd.DataFrame(columns=zarlar, index=zarlar)

for i in range(len(dice)):
    for j in range(i, len(dice)):
        die1 = dice[i]
        die2 = dice[j]
        win_rate = results[(die1, die2)][0]
        loss_rate = results[(die1, die2)][1]
        difference = (win_rate - loss_rate) * 100
        fikstur_matrisi.loc[zarlar[i], zarlar[j]] = difference
        fikstur_matrisi.loc[zarlar[j], zarlar[i]] = -difference


data = fikstur_matrisi.values.astype(float)

k = 4
kmeans = KMeans(n_clusters=k)
kmeans.fit(data)

print("Aitlik oranları:")
for i in range(len(dice)):
    zar = zarlar[i]
    cluster_label = kmeans.labels_[i]
    aitlik_oranlari = kmeans.transform([data[i]])[0]
    aitlik_oranlar_normalized = aitlik_oranlari / sum(aitlik_oranlari) * 100
    aitlik_oranlari_str = " ".join([f"{j + 1}: {aitlik:.2f}" for j, aitlik in enumerate(aitlik_oranlar_normalized)])
    print("{}: {}".format(zar, aitlik_oranlari_str))

fikstur_matrisi['Cluster'] = kmeans.labels_
print(fikstur_matrisi.to_string(index=True, justify='center'))

print("Önceki Merkezler:")
for center in kmeans.cluster_centers_:
    print(center)


new_centers = np.zeros((k + 1, data.shape[1]))
new_centers[:-1] = kmeans.cluster_centers_
cluster_counts = np.zeros(k + 1)

for i in range(len(dice)):
    cluster_label = kmeans.labels_[i]
    new_centers[cluster_label] += data[i]
    cluster_counts[cluster_label] += 1


for i in range(k):
    if cluster_counts[i] > 0:
        new_centers[i] /= cluster_counts[i]

kmeans.cluster_centers_ = new_centers

print("\nGüncellenen Merkezler:")
for center in kmeans.cluster_centers_:
    print(center)


print("\nAitlik oranları (Güncellenen Merkezler):")
for i in range(len(dice)):
    zar = zarlar[i]
    cluster_label = kmeans.labels_[i]
    aitlik_oranlari = kmeans.transform([data[i]])[0]
    aitlik_oranlar_normalized = aitlik_oranlari / sum(aitlik_oranlari) * 100
    aitlik_oranlari_str = " ".join([f"{j + 1}: {aitlik:.2f}" for j, aitlik in enumerate(aitlik_oranlar_normalized[:k])])
    print("{}: {}".format(zar, aitlik_oranlari_str))
