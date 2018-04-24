import glob
from matplotlib import pyplot


def get_data(line):
    '''
        [ 1s ] 28377.78 MiB/sec
        {
            bw: 28377.78,
        }
    '''
    split = line.replace('\n', '').split(' ')
    return {
        'time': split[1].replace('s', ''),
        'bw': split[3],
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
                    'bw': 0.00,
                }
            dataset[key]['bw'] += float(data['bw'])

    for key, value in dataset.items():
        dataset[key]['bw'] /= set_size
    return dataset


def plot_bw(dataset, loc):
    config = loc.split('/')[-2].split('_')
    time = [time for time in dataset.keys()]
    bw = [data['bw'] for key, data in dataset.items()]
    pyplot.figure(1)
    pyplot.title('sysbench Memory Benchmark')
    pyplot.axis([0, 60, 1000, 50000])
    pyplot.plot(
        time[:-1],
        bw[:-1],
        label='Stress[{}, {}]'.format(config[1], config[2])
    )
    pyplot.ylabel('MiB/sec')
    pyplot.xlabel('Time')
    pyplot.legend(loc=2, prop={'size': 6})
    pyplot.savefig('{}bw.png'.format(loc), bbox_inches='tight')


if __name__ == '__main__':
    # glob.glob('./data/memory/stress_[01]_?/*.log')
    # glob.glob(glob.glob('./data/memory/stress_?_[01]/*.log'))
    for path in sorted(glob.glob('./data/memory/*/*.log')):
        print('Generating ', path)
        loc = "/".join(path.split('/')[:-1]) + "/"
        dataset = transform_to_dataset(path)
        plot_bw(dataset, loc)
    print('Aggregate at ', path)
