from django.shortcuts import render
from django.shortcuts import render
from .forms import LoginForm
from .utils import *
def input_profession(request):
    msg = None
    success = False
    form = LoginForm(request.GET)
    return render(request, "login.html", {"form": form, "msg": msg, "success": success})

def show_data(request):
    if request.method == "POST":
        fullName = str(request.POST["fullName"])
        if isCBO(fullName):
            fullName = get_profission(fullName)
            print("CBO")
            print(fullName)
        df_per_hours, df_metrics = connect_site(profession=fullName, functions=[get_pay_per_hours, get_metrics])
        mean = df_metrics.loc["Média Salarial"]["Mensal"]
        median = df_metrics.loc["Salário Mediana"]["Mensal"]
        top = df_metrics.loc["Teto Salarial"]["Mensal"]
        bottom = df_metrics.loc["Piso Salarial"]["Mensal"]
        mean_hour = df_metrics.loc["Média Salarial"]["Por Hora"]
        median_hour = df_metrics.loc["Salário Mediana"]["Por Hora"]
        top_hour = df_metrics.loc["Teto Salarial"]["Por Hora"]
        bottom_hour = df_metrics.loc["Piso Salarial"]["Por Hora"]
        print(df_metrics)
    return render(request, "pass.html", {"name":fullName.capitalize(), "mean":mean, "median":median, "top":top, "bottom":bottom, "mean_hour":mean_hour, "median_hour":median_hour, "top_hour":top_hour, "bottom_hour":bottom_hour})
