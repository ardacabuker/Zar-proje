import random
import itertools

import pandas as pd

zaryüzü = int(input("Zar yüzünü giriniz: "))
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
        results[(zarlar1, zarlar2)] = [0, 0]  # wins for die1 and die2
        for k in range(10000):
            roll1 = random.choice(zarlar1)
            roll2 = random.choice(zarlar2)
            if roll1 > roll2:
                results[(zarlar1, zarlar2)][0] += 1
            elif roll2 > roll1:
                results[(zarlar1, zarlar2)][1] += 1


def is_what_percent_of(num_a):
    return round((num_a / 10000) * 100, 2)


print("Results of 10000 races between each pair of dice:")
for pair, wins in results.items():
    print("{} vs {}: %{} win rate, %{} win rate".format(pair[0], pair[1], is_what_percent_of(wins[0]),
                                                        is_what_percent_of(wins[1])))

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

zarlar = [f" {i + 1}" for i in range(len(dice))]
fikstur_matrisi = pd.DataFrame(columns=zarlar, index=zarlar)

for i in range(len(dice)):
    for j in range(i, len(dice)):
        die1 = dice[i]
        die2 = dice[j]
        kazanma_oranlari = results[(die1, die2)]
        fikstur_matrisi.loc[zarlar[i], zarlar[j]] = kazanma_oranlari[0]
        fikstur_matrisi.loc[zarlar[j], zarlar[i]] = kazanma_oranlari[1]

print(fikstur_matrisi / 100)
