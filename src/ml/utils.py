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


if __name__ == '__main__':
    # TODO(all): Cause it to just merge every folder in given root folder
    in_datasets = [
        "/home/misiu/src/self-driving/mini-self-driving-car/data/2017-08-13-11:05:19-ydykvo",
        "/home/misiu/src/self-driving/mini-self-driving-car/data/2017-08-13-11:02:23-s14csn"
    ]

    out_dir = "data/first_big_dataset"

    merge_datasets(in_datasets, out_dir)
