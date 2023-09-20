import pandas as pd
import numpy as np

def fill_flightcodes(series):
    flight_code = series.iloc[0]
    code_incr = 10
    for i in range(1, len(series)):
        flight_code += code_incr
        if pd.isna(series.iloc[i]):
            series.iloc[i] = flight_code
        
    return series

def clean_airline_data(data):
    newline = '\n'
    delimiter = ';'

    rows = data.strip().split(newline)

    data_rows = [row.split(delimiter) for row in rows]

    df = pd.DataFrame(data_rows[1:], columns=data_rows[0])
    print(df)

    df[['FROM', 'TO']] = df['To_From'].str.split('_', expand=True)

    # capatilize from and to locations to ensure data quality
    df['FROM'] = df['FROM'].str.upper()
    df['TO'] = df['TO'].str.upper()
    del df["To_From"]

    # fill null values, convert column to integer type, fill missing flight codes
    df['FlightCodes'] = df['FlightCodes'].replace('', np.nan)
    df['FlightCodes'] = df['FlightCodes'].astype(float).astype(pd.Int64Dtype())
    df['FlightCodes'] = fill_flightcodes(df['FlightCodes'])

    # clean airline codes
    df['Airline Code'] = df['Airline Code'].str.replace('[^a-zA-Z\s]', '', regex=True).str.strip()

    return df


data = 'Airline Code;DelayTimes;FlightCodes;To_From\nAir Canada (!);[21, 40];20015.0;WAterLoo_NEWYork\n<Air France> (12);[];;Montreal_TORONTO\n(Porter Airways. );[60, 22, 87];20035.0;CALgary_Ottawa\n12. Air France;[78, 66];;Ottawa_VANcouvER\n""".\\.Lufthansa.\\.""";[12, 33];20055.0;london_MONTreal\n'
cleansed_data = clean_airline_data(data)

print(cleansed_data)


