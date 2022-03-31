#!/usr/bin/python3
import os
import json
import csv
from socket import timeout
import pandas as pd
import requests
import logging
import http.client
import objectpath
from collections import Counter
import datetime
from datetime import date, timedelta
import itertools
import pyfiglet

ofile=open('output.csv', 'w')

def Average(ls):
    return sum(ls) / len(ls)

def max_val(url):
        r1 = requests.get(url, headers=headers)
        #print(r1.json(), url)
        with open(r"./temp/Metrics.json", "w") as g:
            json.dump(r1.json(), g, indent=4)

        file = open(r"./temp/Metrics.json", "r")
        data = file.read()
        occurrences = data.count("group")
        occurrences = occurrences - 1

        with open(r"./temp/Metrics.json") as file:
            data = json.load(file)

        for x in range(0, occurrences):
            with open(r"./temp/out"+str(x)+".json", "w") as f:
                json.dump(data['data'][x], f, indent=4)

        temp = list()
        tteam=[]
        max_team="None"
    
        for j in range(0, occurrences):
            with open(r"./temp/out" +str(j)+ ".json") as file:
                data = json.load(file)
                jsonnn_tree = objectpath.Tree(data)
                result_tuple1 = tuple(jsonnn_tree.execute('$..value'))
                result_tuple = tuple(jsonnn_tree.execute('$..owner_team_name'))

                lst = list(result_tuple1)
                for l in range(0, len(result_tuple1)):
                    if lst[l] == None:
                        lst[l] = 0
                        result_tuple1 = tuple(lst)
                temp.append(list(result_tuple1))
                tteam.append(list(result_tuple))
        if temp:
            max_value = max(temp)
            max_team=tteam[temp.index(max_value)][0]
            #print(url)
            #print(max_value, max_team)
            return max_value, max_team

def min_val(url):
        r1 = requests.get(url, headers=headers)
        with open(r"./temp/Metrics.json", "w") as g:
            json.dump(r1.json(), g, indent=4)

        file = open(r"./temp/Metrics.json", "r")
        data = file.read()
        occurrences = data.count("group")
        occurrences = occurrences - 1

        with open(r"./temp/Metrics.json") as file:
            data = json.load(file)

        for x in range(0, occurrences):
            with open(r"./temp/out"+str(x)+".json", "w") as f:
                json.dump(data['data'][x], f, indent=4)

        temp = list()
        tteam=[]
        min_team="None"
    
        for j in range(0, occurrences):
            with open(r"./temp/out" +str(j)+ ".json") as file:
                data = json.load(file)
                jsonnn_tree = objectpath.Tree(data)
                result_tuple1 = tuple(jsonnn_tree.execute('$..value'))
                result_tuple = tuple(jsonnn_tree.execute('$..owner_team_name'))

                lst = list(result_tuple1)
                for l in range(0, len(result_tuple1)):
                    if lst[l] == None:
                        lst[l] = 0
                        result_tuple1 = tuple(lst)
                temp.append(list(result_tuple1))
                tteam.append(list(result_tuple))
        if temp:
            min_value = min(temp)
            min_team=tteam[temp.index(min_value)][0]
            return min_value, min_team

col_list = ["AuthToken", "Start_date","End_date","Metrics","Benchmark","Cohort"]
df = pd.read_csv(r"C:/Rajani/Scripts and Tools/EBR Script/input2.csv", usecols=col_list,encoding='latin-1')

AuthToken=str(df["AuthToken"][0])
days_before=str(df["Start_date"][0])
curr=str(df["End_date"][0])

date_time_obj = datetime.datetime.fromisoformat(days_before)
date_time_obj2= datetime.datetime.fromisoformat(curr)

delta_range=(date_time_obj2-date_time_obj)
#current_date = date.today()
curr=datetime.datetime.strptime(curr,'%Y-%m-%d')
current_date=curr.date()
option = delta_range.days

#current_date="2021-11-17"

#print("Script end Date"+current_date.isoformat())

def trend(x,y):
    #print(x,y)
    return int((round(((y-x)/y),2))*100)

def per(x,y):
    #print(x,y)
    return int((round(((x-y)/y),2))*100)

if option > 0:
    days_before = (current_date-timedelta(days=option)).isoformat()
    
else:
    print("Incorrect option")
print("Script Start Date: "+ days_before)

days_before_delta=str(df["Start_date"][1])
current_date_delta=str(df["End_date"][1])

print("Script End Date: "+current_date.isoformat())
print("Trend Start Date: "+days_before_delta)
print("Trend End Date: "+current_date_delta)

#print(days_before_delta)
#print(current_date_delta)
#metrics = ["cycle_time","commits_per_day", "pushes_per_day", "innovation_rate", "rework_ratio", "maintenance_rate"]

metrics = ["cycle_time", "time_to_open", "time_to_review", "review_speed", "time_to_merge", "pull_request_throughput_per_contributor", "commits_per_day", "pushes_per_day", "innovation_rate", "size", "pull_request_success_ratio", "rework_ratio", "maintenance_rate", "defect_rate", "average_weekly_coding_days"]
#metrics=['maintenance_rate']

#metrics = ["cycle_time"]

print("{:<40} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format("METRICS_NAME", "ACROSS_TEAMS", "BEST_TEAM", "LAGGING_TEAM" ,"BENCH_MARK","COHORT","TREND","BEST TEAM", "LAG TEAM", "START DATE", "END DATE", "TREND START DATE", "TREND END DATE"))
strr='METRICS_NAME,ACROSS_TEAMS,BEST_TEAM,LAGGING_TEAM,BENCH_MARK,COHORT,TREND,BEST TEAM, LAG TEAM,START DATE,END DATE,TREND START DATE,TREND END DATE'
ofile.write(strr+'\n')

reduce=30
sample_list_trend = list()

for m in range(0, len(metrics)):
    bench_value=""+str(df["Benchmark"][m])
    #print(bench_value)
    cohort_value=str(df["Cohort"][m])
    url1 = "https://velocity.codeclimate.com/api/metric?name="+metrics[m]+"&start_date="+days_before+"&end_date="+current_date.isoformat()+"&interval=entire_range"
    url1_prev = "https://velocity.codeclimate.com/api/metric?name="+metrics[m]+"&start_date="+days_before_delta+"&end_date="+current_date_delta+"&interval=entire_range"
    headers = {"Authorization": "Bearer " + str(AuthToken), "Content-Type": "application/vnd.api+json"}
    
    #print(url1_prev)
    r2 = requests.get(url1, headers=headers,timeout=None)
    #print(r2.text)
    #print(url)


    with open(r"./temp/Metrics1.json", "w") as g:
        json.dump(r2.json(), g, indent=4)

    with open(r"./temp/Metrics1.json") as file:
        data = json.load(file)
        jsonnn_tree = objectpath.Tree(data)
        result_tuple1 = tuple(jsonnn_tree.execute('$..value'))
        lst_agg = list(result_tuple1)

    r3 = requests.get(url1_prev, headers=headers,timeout=None)    
    with open(r"./temp/Metrics11.json", "w") as g:
        json.dump(r3.json(), g, indent=4)

    with open(r"./temp/Metrics11.json") as file:
        data = json.load(file)
        jsonnn_tree = objectpath.Tree(data)
        result_tuple11 = tuple(jsonnn_tree.execute('$..value'))
        lst11_agg = list(result_tuple11)   

    z=trend(lst11_agg[0],lst_agg[0])
    sample_list_trend.append(z)

    #print("I m here........")
    #print(sample_list_trend)
    

    if (metrics[m] == "commits_per_day" or metrics[m] =="pushes_per_day" or metrics[m] =="innovation_rate" or metrics[m] =="rework_ratio" or metrics[m] =="maintenance_rate"):
        option=delta_range.days
        flag=0
        current_date=curr.date()
        #print(current_date)

        if option > 0:
            days_before = (current_date-timedelta(days=option)).isoformat()
    
        else:
            print("Incorrect option")
        #print(days_before)

        temp_avg=list()
        temp1_avg=list()
        best_team=""
        lag_team=""
        maxval=-9999
        minval=9999
        while True:
            #print(str(option)+" for metrics " + metrics[m])
            if option > reduce:
                days_before = (current_date-timedelta(days=reduce-1)).isoformat()
                #print(option)
                option=option-reduce
                #print("Printing the current_date: "+current_date.isoformat())
                #print("Printing the days_before: "+days_before)
                #print()
                url= "https://velocity.codeclimate.com/api/metric?name="+metrics[m]+"&start_date="+days_before+"&end_date="+current_date.isoformat()+"&interval=entire_range&group[]=owner_team"
                #print(url)
                maxx,maxt=max_val(url)
                minn,mint=min_val(url)
                temp_avg.append(maxx)
                temp1_avg.append(minn)
                if maxx[0]>maxval:
                    maxval=maxx[0]
                    best_team=maxt
                if minn[0]<minval:
                    minval=minn[0]
                    lag_team=mint
                #print(var)
                current_date=(current_date-timedelta(days=reduce))
            else:
                #print("Printing the current_date: "+current_date.isoformat())
                #print("printing option: "+str(option))
                days_before = (current_date-timedelta(days=option)).isoformat()
                print()
                #print("Printing the days_before: "+days_before)
                url = "https://velocity.codeclimate.com/api/metric?name="+metrics[m]+"&start_date="+days_before+"&end_date="+current_date.isoformat()+"&interval=entire_range&group[]=owner_team"
                #print(url)
                #var=best_worst(url)
                maxx,maxt=max_val(url)
                minn,mint=min_val(url)
                if maxx[0]>maxval:
                    maxval=maxx[0]
                    best_team=maxt
                if minn[0]<minval:
                    minval=minn[0]
                    lag_team=mint
                temp_avg.append(maxx)
                temp1_avg.append(minn)
                flag=1
            
            if flag==1:
                flat_list1 = [item for sublist in temp_avg for item in sublist]
                flat_list2 = [item for sublist in temp1_avg for item in sublist]
                #print(flat_list1)
                #print(flat_list2)
                average1=Average(flat_list1)
                average2=Average(flat_list2)

                final_max=str(round(average1,2))
                final_min=str(round(average2,2))
                #print("this should fix the code now.."+final_max+"..."+final_min)
                break   
            #average=Average(temp_avg)
            #print(average)
            
        lag_per=per(int(float(final_min)),int(lst_agg[0]))
        best_per=per(int(float(final_max)),int(lst_agg[0]))
        Cohert=per(int(float(cohort_value)),int(lst_agg[0]))        

        if (metrics[m] == "pull_request_throughput" or metrics[m] =="average_weekly_coding_days" or metrics[m] =="commits_per_day" or metrics[m] =="pushes_per_day" or metrics[m] =="innovation_rate" or metrics[m] =="pull_request_success_ratio"):


                print("{:<40} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format(metrics[m], str(lst_agg[0]), final_max+"["+str(best_per)+"]", final_min+"["+str(lag_per)+"]",(""+bench_value),cohort_value+"["+str(Cohert)+"]",z, best_team, lag_team, days_before, current_date.isoformat(), days_before_delta, current_date_delta))
                strr=f'{metrics[m]},{str(lst_agg[0])},{final_max+"["+str(best_per)+"]"},{final_min+"["+str(lag_per)+"]"},{(""+bench_value)},{cohort_value+"["+str(Cohert)+"]"},{z},{best_team.replace(",","_")},{lag_team.replace(",","_")},{days_before},{current_date.isoformat()},{days_before_delta},{current_date_delta}'
                ofile.write(strr+"\n")
        else:
                #print(lag_per)
                print("{:<40} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format(metrics[m], str(lst_agg[0]), final_min+"["+str(lag_per)+"]", final_max+"["+str(best_per)+"]",(""+bench_value),cohort_value+"["+str(Cohert)+"]",z, lag_team, best_team, days_before, current_date.isoformat(), days_before_delta, current_date_delta))

                strr=f'{metrics[m]},{str(lst_agg[0])},{final_min+"["+str(lag_per)+"]"},{final_max+"["+str(best_per)+"]"},{(""+bench_value)},{cohort_value+"["+str(Cohert)+"]"},{z},{lag_team.replace(",","_")},{best_team.replace(",","_")},{days_before},{current_date.isoformat()},{days_before_delta},{current_date_delta}'
                ofile.write(strr+"\n")
        #print("{:<40} {:<15} {:<15} {:<15} {:<15} {:<15}".format(metrics[m], str(lst_agg[0]),"","",(""+bench_value),cohort_value))







    else:    
        # bench_value=""+str(df["Benchmark"][m])
        # cohort_value=str(df["Cohort"][m])
        #url1 = "https://velocity.codeclimate.com/api/metric?name="+metrics[m]+"&start_date=2021-11-01&end_date=2022-01-04&interval=entire_range"
        #url = "https://velocity.codeclimate.com/api/metric?name=" + metrics[m] + "&start_date=2021-11-01&end_date=2022-01-04&interval=entire_range&group[]=owner_team"
    
        url1 = "https://velocity.codeclimate.com/api/metric?name="+metrics[m]+"&start_date="+days_before+"&end_date="+current_date.isoformat()+"&interval=entire_range"
        url = "https://velocity.codeclimate.com/api/metric?name="+metrics[m]+"&start_date="+days_before+"&end_date="+current_date.isoformat()+"&interval=entire_range&group[]=owner_team"
    
    
        headers = {"Authorization": "Bearer " + str(AuthToken), "Content-Type": "application/vnd.api+json"}
        # r2 = requests.get(url1, headers=headers,timeout=None)
        # #print(r2.text)
        # #print(url)

        # with open(r"Metrics1.json", "w") as g:
        #     json.dump(r2.json(), g, indent=4)

        # with open(r"Metrics1.json") as file:
        #     data = json.load(file)
        #     jsonnn_tree = objectpath.Tree(data)
        #     result_tuple1 = tuple(jsonnn_tree.execute('$..value'))
        #     lst_agg = list(result_tuple1)

        r1 = requests.get(url, headers=headers)
        with open(r"./temp/Metrics.json", "w") as g:
            json.dump(r1.json(), g, indent=4)

        file = open(r"./temp/Metrics.json", "r")
        data = file.read()
        occurrences = data.count("group")
        occurrences = occurrences - 1

        with open(r"./temp/Metrics.json") as file:
            data = json.load(file)

        for x in range(0, occurrences):
            with open(r"./temp/out"+str(x)+".json", "w") as f:
                json.dump(data['data'][x], f, indent=4)

        temp = list()
        tteam=[]
    
        for j in range(0, occurrences):
            with open(r"./temp/out" +str(j)+ ".json") as file:
                data = json.load(file)
                jsonnn_tree = objectpath.Tree(data)
                result_tuple1 = tuple(jsonnn_tree.execute('$..value'))
                result_tuple = tuple(jsonnn_tree.execute('$..owner_team_name'))

                lst = list(result_tuple1)
                for l in range(0, len(result_tuple1)):
                    if lst[l] == None:
                        lst[l] = 0
                        result_tuple1 = tuple(lst)
                temp.append(list(result_tuple1))
                tteam.append(list(result_tuple))
        #print(temp)
        #print(tteam)
        if temp:
            max_value = max(temp)
            max_team=tteam[temp.index(max_value)][0]
            min_value = min(temp)
            min_team=tteam[temp.index(min_value)][0]
            #print(max_team, min_team)
        #print("Best "+metrics[m]+" "+str(min_value[0]))
        #print("worst "+metrics[m]+" "+str(max_value[0]))
            print()
        #print("{:<40} {:<15} {:<15} {:<15}".format(metrics[m], str(lst_agg[0]), str(min_value[0]), str(max_value[0])))
            lag_per=per(int(min_value[0]),int(lst_agg[0]))
            best_per=per(int(max_value[0]),int(lst_agg[0]))
            Cohert=per(int(float(cohort_value)),int(lst_agg[0])) 
            if (metrics[m] == "pull_request_throughput" or metrics[m] =="average_weekly_coding_days" or metrics[m] =="commits_per_day" or metrics[m] =="pushes_per_day" or metrics[m] =="innovation_rate" or metrics[m] =="pull_request_success_ratio"):
                
                print("{:<40} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format(metrics[m], str(lst_agg[0]), str(max_value[0])+"["+str(best_per)+"]", str(min_value[0])+"["+str(lag_per)+"]",(""+bench_value),cohort_value+"["+str(Cohert)+"]",z,max_team, min_team, days_before, current_date.isoformat(), days_before_delta, current_date_delta))
                strr=f'{metrics[m]},{str(lst_agg[0])},{str(max_value[0])+"["+str(best_per)+"]"},{str(min_value[0])+"["+str(lag_per)+"]"},{(""+bench_value)},{cohort_value+"["+str(Cohert)+"]"},{z},{max_team.replace(",","_")},{min_team.replace(",","_")},{days_before},{current_date.isoformat()},{days_before_delta},{current_date_delta}'
                ofile.write(strr+"\n")
            
            else:
                
                print("{:<40} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format(metrics[m], str(lst_agg[0]), str(min_value[0])+"["+str(lag_per)+"]", str(max_value[0])+"["+str(best_per)+"]",(""+bench_value),cohort_value+"["+str(Cohert)+"]",z, min_team, max_team, days_before, current_date.isoformat(), days_before_delta, current_date_delta))
                strr=f'{metrics[m]},{str(lst_agg[0])},{str(min_value[0])+"["+str(lag_per)+"]"},{str(max_value[0])+"["+str(best_per)+"]"},{(""+bench_value)},{cohort_value+"["+str(Cohert)+"]"},{z},{min_team.replace(",","_")},{max_team.replace(",","_")},{days_before},{current_date.isoformat()},{days_before_delta},{current_date_delta}'
                ofile.write(strr+"\n")
        else:
            print()
            print("Unable to fetch data for given range for matrics: " + metrics[m])    
ofile.write("")
ofile.close()
#os.rmdir("C:/Rajani/Scripts and Tools/EBR Script/temp")

#filePath = 'C:/Rajani/Scripts and Tools/New/temp'
dir = 'C:/Rajani/Scripts and Tools/EBR Script/temp'

for f in os.listdir(dir):

    os.remove(os.path.join(dir, f))