import urllib.request, json, os, sys
import statistics as stats

from optparse import OptionParser
from datetime import datetime, timedelta
from collections import Counter

def plot_histogram(start, end):

    if os.path.exists(opt.datadir + "/" + start + "-" + end + ".json"):
        data = json.load(open(opt.datadir + "/" + start + "-" + end + ".json", "r"))
    else:
        #httpresponse = urllib.request.urlopen("https://www.dcc.ufrrj.br/ocupationdb/api.php?period_from=2019-12-06%2008:00:00&period_to=2019-12-06%2018:00:00&type=data&mac_id=813")
        httpresponse = urllib.request.urlopen("https://www.dcc.ufrrj.br/ocupationdb/api.php?period_from=" + urllib.parse.quote(start) + "&period_to=" + urllib.parse.quote(end) + "&type=data")
        # Was hoping text would contain the actual json crap from the URL, but seems not...
        data = json.loads(httpresponse.read().decode())
        json.dump(data, open(opt.datadir + "/" + start + "-" + end + ".json", "w"))

    # get mac id's
    macs = []
    for pkt in data:
        macs.append(pkt['mac'])

    # remove dupplicates
    macs = list(dict.fromkeys(macs))

    # Read samples
    samples = {}
    for pkt in data:
        mac = pkt['mac']
        sensor = pkt['device_id']
        if mac not in samples:
            samples[mac] = {}
        if sensor not in samples[mac]:
            samples[mac][sensor] = []
        samples[mac][sensor].append(int(pkt['s']))

    for mac in samples:
        for sensor in samples[mac]:
            samples[mac][sensor].sort(reverse=True)

            # calc mean
            mean = sum(samples[mac][sensor]) / len(samples[mac][sensor])

            # calc xue17
            #print(samples[mac][sensor][:maxM])
            xue17 = sum(samples[mac][sensor][:maxM]) / len(samples[mac][sensor][:maxM])

            # write to file
            #f = open(data_dir + "/" + str(mac) + "." + sensor, "a")
            #f.write("{}\t{:.3f}\t{:.3f}\n".format(start, mean, xue17))
            #f.close()

            if mac not in rssi:
                rssi[mac] = {}
            if sensor not in rssi[mac]:
                rssi[mac][sensor] = {}
                rssi[mac][sensor]["time"] = []
                rssi[mac][sensor]["mean"] = []
                rssi[mac][sensor]["xue17"] = []

            rssi[mac][sensor]["time"].append(datetime.strptime(start, "%Y-%m-%d %H:%M:%S"))
            rssi[mac][sensor]["mean"].append(mean)
            rssi[mac][sensor]["xue17"].append(xue17)

            # print histogram
    #        histogram = Counter(samples[mac])
    #        print("mac: " + str(mac))
    #        for i in sorted (histogram.keys()) :  
    #            print(str(i) + " " + str(histogram[i]), end = "\n") 


# Read args from command line
parser = OptionParser()
parser.add_option("-o", "--out-dir", type="string", dest="outdir", default="output", help="output directory DIR", metavar="DIR")
parser.add_option("-d", "--data-dir", type="string", dest="datadir", default="data", help="json data directory DIR", metavar="DIR")
parser.add_option("-M", "--max", type="int", dest="maxM", default=10, help="NUM amount of RSSI maximum samples used in [Xue17]", metavar="NUM")
parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="don't print debug messages to stdout")

(opt, args) = parser.parse_args()

# create directories
try:
    os.mkdir(opt.datadir)
    print("Directory", opt.datadir, "created.") 
except FileExistsError:
    print("Directory", opt.datadir, "already exists.")

try:
    os.mkdir(opt.outdir)
    print("Directory", opt.outdir, "created.") 
except FileExistsError:
    print("Directory", opt.outdir, "already exists.")

maxM = opt.maxM
start_date = datetime(2019, 12, 6, 8, 0, 0)
end_date = datetime(2019, 12, 6, 11, 59, 59)
delta = timedelta(minutes=5)

rssi = {}
while start_date <= end_date:
    start = start_date.strftime("%Y-%m-%d %H:%M:%S")
    end = (start_date+delta).strftime("%Y-%m-%d %H:%M:%S")
    if opt.verbose: print("Getting data from " + start + " to " + end)
    plot_histogram(start, end)
    start_date += delta

count_std_mean = 0
count_std_xue17 = 0
count_s_mean = 0
count_s_xue17 = 0
for mac in rssi:
    for sensor in rssi[mac]:
        avg_mean = stats.mean(rssi[mac][sensor]["mean"])
        avg_xue17 = stats.mean(rssi[mac][sensor]["xue17"])
        std_mean = stats.stdev(rssi[mac][sensor]["mean"]) if len(rssi[mac][sensor]["mean"]) > 1 else 0
        std_xue17 = stats.stdev(rssi[mac][sensor]["xue17"]) if len(rssi[mac][sensor]["xue17"]) > 1 else 0
        if std_mean < std_xue17:
            count_std_mean += 1
        if std_mean > std_xue17:
            count_std_xue17 += 1
        if opt.verbose: print("{:8s} {:15s} {:.3f} {:.3f} - {:.3f} {:.3f}".format(mac, sensor, avg_mean, std_mean, avg_xue17, std_xue17))

        ltime = rssi[mac][sensor]["time"]
        lmean = rssi[mac][sensor]["mean"]
        lxue17 = rssi[mac][sensor]["xue17"]
        smean = 0
        sxue17 = 0
        for i in range(len(ltime)):
            if i == 0 or i == len(ltime)-1: continue
            smean += (lmean[i] - (lmean[i-1] + lmean[i] + lmean[i+1])/3)**2
            sxue17 += (lxue17[i] - (lxue17[i-1] + lxue17[i] + lxue17[i+1])/3)**2
        if smean < sxue17:
            count_s_mean += 1
        if smean > sxue17:
            count_s_xue17 += 1
        if opt.verbose: print("smean: {:.3f} sxue17: {:.3f}".format(smean, sxue17))

        plt.plot(ltime, lmean, label="Mean", lw=1)
        plt.plot(ltime, lxue17, label="Xue17", lw=1)
        plt.legend()
        plt.gcf().autofmt_xdate()
        plt.savefig(opt.outdir + "/" + mac + sensor + ".pdf")
        plt.clf()

print ("STDEV:  Simple mean had {} times lower std. dev., and Xue17 had {} times lower std. dev.".format(count_std_mean, count_std_xue17))
print ("SMOOTH: Simple mean had {} times lower smoothness idx, and Xue17 had {} times lower smoothness idx.".format(count_s_mean, count_s_xue17))

