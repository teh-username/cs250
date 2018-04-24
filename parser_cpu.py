import glob
from matplotlib import pyplot


def get_data(line):
    '''
        [ 4s ] thds: 4 eps: 625.96 lat (ms,95%): 13.70
        {
            time: 4,
            thds: 4,
            eps: 625.96,
            lat: 13.70,
        }
    '''
    split = line.replace('\n', '').split(' ')
    return {
        'time': split[1].replace('s', ''),
        'thds': split[4],
        'eps': split[6],
        'lat': split[9],
    }


def transform_to_dataset(path):
    dataset = {}
    set_size = 3
    with open(path) as file:
        for line in file:
            if line[0] != '[':
                continue
            data = get_data(line)
            key = int(data['time'])
            if key not in dataset:
                dataset[key] = {
                    'eps': 0.00,
                    'lat': 0.00,
                }
            dataset[key]['eps'] += float(data['eps'])
            dataset[key]['lat'] += float(data['lat'])

    for key, value in dataset.items():
        dataset[key]['eps'] /= set_size
        dataset[key]['lat'] /= set_size
    return dataset


def plot_events(dataset, loc):
    config = loc.split('/')[-2].split('_')
    time = [time for time in dataset.keys()]
    eps = [data['eps'] for key, data in dataset.items()]
    pyplot.figure(1)
    pyplot.title('sysbench CPU Benchmark')
    pyplot.axis([0, 60, 100, 2500])
    pyplot.plot(
        time[:-1],
        eps[:-1],
        label='Stress[{}, {}]'.format(config[1], config[2])
    )
    pyplot.ylabel('Events per second')
    pyplot.xlabel('Time')
    pyplot.legend(loc=2, prop={'size': 6})
    pyplot.savefig('{}eps.png'.format(loc), bbox_inches='tight')


def plot_latency(dataset, loc):
    config = loc.split('/')[-2].split('_')
    time = [time for time in dataset.keys()]
    lat = [data['lat'] for key, data in dataset.items()]
    pyplot.figure(2)
    pyplot.title('sysbench CPU Benchmark')
    pyplot.axis([0, 60, 1, 50])
    pyplot.plot(
        time[:-1],
        lat[:-1],
        label='Stress[{}, {}]'.format(config[1], config[2])
    )
    pyplot.ylabel('Latency (ms)')
    pyplot.xlabel('Time')
    pyplot.legend(loc=2, prop={'size': 6})
    pyplot.savefig('{}lat.png'.format(loc), bbox_inches='tight')

if __name__ == '__main__':
    # glob.glob('./data/cpu/stress_[01]_?/*.log')
    # glob.glob('./data/cpu/stress_?_[01]/*.log')
    for path in sorted(glob.glob('./data/cpu/*/*.log')):
        print('Generating ', path)
        loc = "/".join(path.split('/')[:-1]) + "/"
        dataset = transform_to_dataset(path)
        plot_events(dataset, loc)
        plot_latency(dataset, loc)
    print('Aggregate at ', path)
