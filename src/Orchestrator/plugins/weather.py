import requests
import threading

def LoadForecast(apiKey, lat, long, time=None, units="auto", lazy=False, callback=None):

    """
        This function builds the request url and loads some or all of the
        needed json depending on lazy is True
        inLat:  The latitude of the forecast
        inLong: The longitude of the forecast
        time:   A datetime.datetime object representing the desired time of
               the forecast. If no timezone is present, the API assumes local
               time at the provided latitude and longitude.
        units:  A string of the preferred units of measurement, "auto" id
                default. also us,ca,uk,si is available
        lazy:   Defaults to false.  The function will only request the json
                data as it is needed. Results in more requests, but
                probably a faster response time (I haven't checked)
    """

    if time is None:
        url = 'https://api.forecast.io/forecast/%s/%s,%s' \
              '?units=%s' % (apiKey, lat, long, units,)
    else:
        url_time = time.replace(microseconds=0).isoformat() #API will return 400 for microseconds
        url = 'https://api.forecast.io/forecast/%s/%s,%s,%s' \
              '?units=%s' % (apiKey, lat, long, url_time, units,)

    if lazy is True:
        baseUrl = "%s&exclude=%s" % (url,
                                     'minutely,currently,hourly,'
                                     'daily,alerts,flags')

    else:
        baseUrl = url

    return manual(baseUrl, callback=callback)

def manual(requestURL, callback=None):
    """
        This function is used by load_forecast OR by users to manually
        construct the URL for an API call.
    """

    if callback is None:
        return GetForecast(requestURL)
    else:
        thread = threading.Thread(target=load_async,
                                  args=(requestURL, callback))
        thread.start()

def GetForecast(requestURL):
        ForecastIO_Response = requests.get(requestURL)
        ForecastIO_Response.raise_for_status()  #Check there is no 4xx/5xx status code returned

        json = ForecastIO_Response.json()
        headers = ForecastIO_Response.headers

        return Forecast(json, ForecastIO_Response, headers)

def load_async(url, callback):
    callback(GetForecast(url))