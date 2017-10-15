import itertools
import os
import pandas
import shutil
import tqdm

import lib.file as file_util


def merge_datasets(input_datasets, output_dir):
    """
    Merge list of datasets.
    """

    out_img_dir = os.path.join(output_dir, 'img')

    print("Creating directories...")
    # make sure the wanted directory exists
    file_util.mkdir_p(output_dir)
    file_util.mkdir_p(out_img_dir)

    print("Copying images...")
    # copy the images in
    for in_dir in tqdm.tqdm(input_datasets):
        in_img_dir = os.path.join(in_dir, 'img')

        for img in tqdm.tqdm(os.listdir(in_img_dir)):
            from_fname = os.path.join(in_img_dir, img)
            to_fname = os.path.join(out_img_dir, img)
            shutil.copy(from_fname, to_fname)

    print("Appending logs...")
    log_acc = []
    # merge the log files
    for in_dir in tqdm.tqdm(input_datasets):
        log_fname = os.path.join(in_dir, 'log.csv')

        local_log = pandas.read_csv(log_fname)
        log_acc.append(local_log)

    full_log = pandas.concat(log_acc)
    out_log_fname = os.path.join(output_dir, 'log.csv')

    full_log.to_csv(out_log_fname, index=False)


def merge_whole_dir(in_dir, out_dir):
    """
    Merge all datasets in target in_dir and write them to out_dir
    """

    in_datasets = [
        os.path.join(in_dir, dataset_path)
        for dataset_path in os.listdir(in_dir)
    ]

    merge_datasets(in_datasets, out_dir)


def group(lst, n):
    """group([0,3,4,10,2,3], 2) => iterator

     Group an iterable into an n-tuples iterable. Incomplete tuples
    are discarded e.g.

    e.g. list(group(range(10), 3))
    [(0, 1, 2), (3, 4, 5), (6, 7, 8)]
    """
    # TODO(mike): why is this here? looks like a bad refactor
    return zip(*[
        itertools.islice(lst, i, None, n)
        for i in range(n)
    ]
               )

if __name__ == '__main__':
    merge_whole_dir(
        in_dir='/home/misiu/src/self-driving/mini-self-driving-car/datasets/all',
        out_dir='datasets/all_to_date'
    )


