from sklearn import datasets
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

from sklearn import metrics

from mlxtend.plotting import plot_decision_regions


wine = datasets.load_wine()


# Criando o DataFrame
df_wine = pd.DataFrame(data=wine.data,columns=wine.feature_names)


# Criando a coluna com os valores da variável target.
df_wine['class'] = wine.target

print(df_wine.head().T)


df_wine.info()


print(df_wine['class'].value_counts())


#########################################################


X_train, X_test, y_train, y_test = train_test_split(df_wine.drop('class',axis=1), df_wine['class'], test_size=0.3)




# Definindo o número de vizinhos.
knn = KNeighborsClassifier(n_neighbors=3)

knn.fit(X_train, y_train)

resultado = knn.predict(X_test)
print(resultado)


print (pd.crosstab(y_test,resultado, rownames=['Real'], colnames=['Predito'], margins=True))


# print('asiudiusdiuasgiau->>>> ', wine.target_names)

print(metrics.classification_report(y_test,resultado,target_names=wine.target_names))





############################################################# HORA DO PLOT 

print(X_train)

X = wine.data[:,[0,2]]
y = wine.target

print(wine.data)
print('X -->', X)


print( wine.target_names)
print(y)

knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X, y)
plt.figure(figsize=(8,5))
plot_decision_regions(X,y,clf=knn,legend=2)
plt.xlabel('alcohol')
plt.ylabel('malic_acid')
plt.title('Fronteiras de Complexidade - KNN')

plt.show()