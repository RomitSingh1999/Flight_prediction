from flask import Flask, render_template, url_for, redirect,request
import pickle
import numpy as np
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/predict',methods=['POST','GET'])
def predict():
    testdata=0
    data=[]
    if request.method =='POST':
        start_date = request.form['trip-start']
        flight_name = request.form['flight']
        Dep = request.form['Dep']
        Source = request.form['Source']
        Destination = request.form['Destination']
        Arrive = request.form['Arrive']
        Stops = request.form['Stops']
        data.append(Stops)
        print(Dep)
        if (start_date[-2:][0]=='0'):
            date=start_date[-1:]
        else:
            date=start_date[-2:]
        data.append(date)
        if (start_date[5:7][0]=='0'):
            month=start_date[6:7]
        else:
            month=start_date[5:7]
        data.append(month)
        if (Dep[:2][0]=='0'):
            Dep_hr=Dep[1:2]
        else:
            Dep_hr=Dep[:2]
        data.append(Dep_hr)
        if (Dep[-2:][0]=='0'):
            Dep_min=Dep[-1:]
        else:
            Dep_min=Dep[-2:]
        data.append(Dep_min)

        if (Arrive[:2][0]=='0'):
            Arrive_hr=Arrive[1:2]
        else:
            Arrive_hr=Arrive[:2]
        data.append(Arrive_hr)
        if (Arrive[-2:][0]=='0'):
            Arrive_min=Arrive[-1:]
        else:
            Arrive_min=Arrive[-2:]
        data.append(Arrive_min)

        if(Dep_hr>Arrive_hr):
            duration_hr=abs((24-int(Dep_hr))+int(Arrive_hr))
            duration_min=abs((60-int(Dep_min))+int(Arrive_min))
        else:
            duration_hr=abs(int(Arrive_hr)+int(Dep_hr))
            duration_min= abs(int (Arrive_min)-int(Dep_min))
        data.append(str(duration_hr))
        data.append(str(duration_min))
        flightlist=['Airline_Air India', 'Airline_GoAir', 'Airline_IndiGo',
       'Airline_Jet Airways', 'Airline_Jet Airways Business',
       'Airline_Multiple carriers',
       'Airline_Multiple carriers Premium economy', 'Airline_SpiceJet',
       'Airline_Trujet', 'Airline_Vistara', 'Airline_Vistara Premium economy']
        for i in flightlist:
            if(i==flight_name):
               i='1'
            else:
                i='0'
            data.append(i)
        Sourcelist=['Chennai', 'Delhi', 'Kolkata', 'Mumbai']
        for i in Sourcelist:
            if(i==Source):
                i='1'
            else:
                i='0'
            data.append(i)
        Destinationlist=['Cochin', 'Delhi', 'Hyderabad',
       'Kolkata', 'New Delhi']
        for i in Destinationlist:
            if(i==Destination):
                i='1'
            else:
                i='0'
            data.append(i)
        model = open('flight_rf.pkl', 'rb')
        forest= pickle.load(model)
        lst=data
        arr=[np.array(lst)]
        print(forest.predict(arr)[0])
        test_data=forest.predict(arr)[0]
        

        return render_template('index.html',testdata=test_data.round(2))
    else:
        return render_template("new.html")
if __name__ == "__main__":
    app.run(debug=True)