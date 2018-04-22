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
    dataset = []
    with open(path) as file:
        for line in file:
            if line[0] != '[':
                continue
            dataset.append(get_data(line))
    return dataset


def plot_dataset(dataset):
    pyplot.plot([1, 2, 3, 4], [1, 4, 9, 16])
    pyplot.ylabel('some numbers')
    pyplot.show()


if __name__ == '__main__':
    path = 'parse.log'
    dataset = transform_to_dataset(path)
    plot_dataset(dataset)
    print(dataset)
