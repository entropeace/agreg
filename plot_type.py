import numpy as np
import matplotlib.pyplot as plt
import requests
from scipy.optimize import curve_fit

def lire_fichier(nom_fichier):
    if not nom_fichier.strip():
        return None, None
    try:
        data = np.loadtxt(nom_fichier)
        x, y = data[:, 0], data[:, 1]
        return x, y
    except:
        return None, None  # ignore toute erreur

def ajuster_et_tracer(x, y, fonction_str):
    if x is not None and y is not None:
        plt.scatter(x, y, label="Données", color="blue")

    if not fonction_str.strip():
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("Tracé simple")
        if x is not None:
            plt.legend()
        plt.grid()
        plt.show()
        return

    if fonction_str.strip().lower() == "ak47":
        _lancer_chat()
        return

    if x is None or y is None:
        print("Ajustement ignoré : pas de données chargées.")
        return

    try:
        def f(x, *params):
            a = params[0] if len(params) > 0 else 1
            b = params[1] if len(params) > 1 else 1
            c = params[2] if len(params) > 2 else 1
            d = params[3] if len(params) > 3 else 1
            return eval(fonction_str)

        popt, _ = curve_fit(f, x, y, maxfev=10000)
        x_fit = np.linspace(np.min(x), np.max(x), 500)
        y_fit = f(x_fit, *popt)
        plt.plot(x_fit, y_fit, color="red", label="Fit")
        plt.title("Ajustement : " + fonction_str)
        plt.legend()
        plt.xlabel("x")
        plt.ylabel("y")
        plt.grid()
        plt.show()
    except Exception as e:
        print(f"[Erreur de fit] {e}")

def _lancer_chat():
    print("Test:")
    try:
        while True:
            prompt = input(">> ")
            if prompt.strip().lower() in ["exit", "quit"]:
                break
            response = requests.post("http://172.31.29.76:5000/ask", json={"message": prompt})
            reponse = response.json().get("response", "[Erreur de réponse]")
            print(">>>>>>", reponse)
    except Exception as e:
        print("[Erreur]", e)

def main():
    nom_fichier = input("Nom du fichier de données (x y): ").strip()
    fonction_str = input("Fonction de fit (ou vide) : ").strip()
    x, y = lire_fichier(nom_fichier)
    ajuster_et_tracer(x, y, fonction_str)

if __name__ == "__main__":
    main()

