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
        mean = df_metrics.loc["Mean"]["Mensal"]
        median = df_metrics.loc["Median"]["Mensal"]
        top = df_metrics.loc["Max"]["Mensal"]
        bottom = df_metrics.loc["Min"]["Mensal"]
        mean_hour = df_metrics.loc["Mean"]["Per Hour"]
        median_hour = df_metrics.loc["Median"]["Per Hour"]
        top_hour = df_metrics.loc["Max"]["Per Hour"]
        bottom_hour = df_metrics.loc["Min"]["Per Hour"]
        print(df_metrics)
    return render(request, "pass.html", {"name":fullName.capitalize(), "mean":mean, "median":median, "top":top, "bottom":bottom, "mean_hour":mean_hour, "median_hour":median_hour, "top_hour":top_hour, "bottom_hour":bottom_hour})
