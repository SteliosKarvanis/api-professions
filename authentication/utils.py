import glob
import csv
from turtle import color
from bs4 import BeautifulSoup
from numpy import number
import pandas as pd
import requests
import matplotlib.pyplot as plt
import matplotlib
import os
matplotlib.use('Agg')

def get_dict() -> dict:
    files = glob.glob("authentication/data/*.csv")
    data = {}
    for file in files:
        with open(file, mode='r', encoding="latin-1") as f:
            reader = csv.reader(f, delimiter=";")
            next(reader)
            dic = {rows[1].strip().lower():rows[0] for rows in reader}
        data = {**dic, **data}
    return data


def map_ode_to_profission() -> dict:
    files = glob.glob("authentication/data/*.csv")
    data = {}
    for file in files:
        with open(file, mode='r', encoding="latin-1") as f:
            reader = csv.reader(f, delimiter=";")
            next(reader)
            dic = {rows[0]:rows[1].strip().lower() for rows in reader}
        data = {**dic, **data}
    return data


def get_cbo(data: dict, name: str) -> str:
    return data[name] 


def get_profission(name: str) -> str:
    data = map_ode_to_profission()
    return data[name] 


def format_name(name: str) -> str:
    name = name.replace("ç", "c")
    name = name.replace("ã", "a")
    name = name.replace("á", "a")
    name = name.replace("â", "a")
    name = name.replace("é", "e")
    name = name.replace("õ", "o")
    name = name.replace("ô", "o")
    name = name.replace(" ", "-")
    return name


def get_table_line(label: str, table, tag: str):
  result = []
  for mensal in table.findAll(tag, {"data-label":label}):
    text = mensal.text
    text = text.replace(".", "")
    text = text.replace(",", ".")
    try:
      result.append(float(text))
    except:
      pass

  return result


def get_url_given_profession(profession: str) -> str:
  dic = get_dict()
  return "https://www.salario.com.br/profissao/" + str(format_name(profession)) + "-cbo-" + str(get_cbo(dic, profession)) + "/"


def isCBO(name):
  try:
    int(name)
    return True
  except:
    return False


def get_metrics(profession: str, soup) -> pd.DataFrame:
  for table in soup.findAll("table"):
    if table.find("h2", attrs={"id":"calculo_salarial"}) is None:
        continue
    mensal = get_table_line(label="Salário Mensal", table=table, tag="td")
    mensal.pop(2)
    mensal.pop(3)
    per_hour = get_table_line(label="Salário Por Hora", table=table, tag="td")
    per_hour.pop(2)
    per_hour.pop(3)
    df = pd.DataFrame()
    df["Mensal"] = mensal
    df["Por Hora"] = per_hour
    rows = ["Piso Salarial", "Média Salarial", "Salário Mediana", "Teto Salarial"]
    df.rename({i:rows[i] for i in range(len(rows))}, inplace=True)
    break
  return df


def get_pay_per_hours(profession: str, soup):
  for table in soup.findAll("table"):
    if table.find("caption") is None or str(table.find("caption").text).strip() != "Cálculo de acordo com a carga horária mensal e salário":
      continue
    total = get_table_line(label="Total:", table=table, tag="td")
    hours = get_table_line(label="Jornada: ", table=table, tag="td")
    mensal = get_table_line(label="Salário Mensal:", table=table, tag="td")
    df = pd.DataFrame()
    df["total"] = total
    df["hours"] = hours
    df["mensal"] = mensal
    make_histogram(df)
    break
  return df


def connect_site(profession: str, functions: list):
  profession = profession.lower().strip()
  print("Requesting")
  r = requests.post(url=get_url_given_profession(profession))
  soup = BeautifulSoup(r.text, features="html.parser")
  results = []
  for function in functions:
    results.append(function(profession, soup))
  return results


def make_histogram(df):
  if os.path.exists("authentication/static/histogram.png"):
    os.remove("authentication/static/histogram.png")
  numbers = df["total"].to_numpy()
  hours = df["hours"].to_numpy()
  number_total = numbers.sum()
  plt.title("Distribuição dos funcionários por horas trabalhadas")
  plt.xlabel("Horas")
  plt.ylabel("Porcentagem de Funcionarios (%)")
  plt.bar(hours, numbers*100/number_total, color="blue")
  plt.savefig("authentication/static/histogram.png")
