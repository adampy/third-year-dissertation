# Based on the library "mockseries" (https://mockseries.catheu.tech/)
from mockseries.trend import LinearTrend
from mockseries.seasonality import SinusoidalSeasonality
from mockseries.noise import GaussianNoise
from datetime import datetime, timedelta
from mockseries.utils import datetime_range
import csv

TIME_UNIT = timedelta(seconds=1)
LENGTH = 60 * 60 * 2 # 2 hours

TREND_BEGIN = 100
TREND_END = 100
TREND_COEFFICIENT = (TREND_END - TREND_BEGIN) / LENGTH

NOISE_MEAN = 0
NOISE_STD = 3

SEASONALITY_AMP = 70
SEASONALITY_PERIOD = timedelta(minutes=60)

def save_timeseries(timeseries):
    # Generate data points
    epoch = datetime.fromtimestamp(0)
    time_points = datetime_range(
        granularity=TIME_UNIT,
        start_time=epoch,
        end_time=epoch + timedelta(seconds=LENGTH),
    )
    ts_values = timeseries.generate(time_points=time_points)

    # Now write values
    output = "lp_b{}_e{}_s{}_r{}_sa{}_sp{}.csv".format(TREND_BEGIN, TREND_END, LENGTH, NOISE_STD, SEASONALITY_AMP, SEASONALITY_PERIOD.seconds)
    with open(output, "w") as f:
        writer = csv.writer(f)
        for i in range(len(ts_values)):
            vlaue = round(ts_values[i])
            writer.writerow([i, vlaue])

if __name__ == "__main__":

    trend = LinearTrend(coefficient=TREND_COEFFICIENT, time_unit=TIME_UNIT, flat_base=TREND_BEGIN)
    noise = GaussianNoise(mean=NOISE_MEAN, std=NOISE_STD)
    seasonality = SinusoidalSeasonality(amplitude=SEASONALITY_AMP, period=SEASONALITY_PERIOD, offset=SEASONALITY_PERIOD * (3/4))

    timeseries = trend + seasonality + noise

    #timeseries.preview_minute(LENGTH / 60)
    #timeseries.preview_hour(LENGTH / 60 / 60)
    
    save_timeseries(timeseries)