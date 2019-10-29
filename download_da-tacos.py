import argparse
import sys
import os.path
import wget
import json
from zipfile import ZipFile
import gdown

with open('./paths.json') as f:
    download_paths = json.load(f)

gdrive_prefix = 'https://drive.google.com/uc?id='


def download(dataset, data_type, source, output_dir, unpack_zips, remove_zips):
    if not os.path.exists(output_dir):
        sys.stderr.write('Output directory \'{}\' does not exist'.format(output_dir))
        return

    if dataset == 'da-tacos':
        download_sets = ['benchmark subset', 'cover analysis subset', 'metadata']
    else:
        if dataset != 'metadata':
            download_sets = [dataset, 'metadata']
        else:
            download_sets = [dataset]

    if type(data_type) is list:
        download_types = data_type
    else:
        download_types = [data_type]

    for subset in download_sets:
        if subset == 'metadata':
            output = os.path.join(output_dir, download_paths[subset]['filename'])
            print('Downloading the metadata')
            if source == 'gdrive':
                if source == 'gdrive':
                    gdown.download('{}{}'.format(gdrive_prefix, download_paths[subset]['gdrive']),
                                   output,
                                   quiet=False)
                else:
                    wget.download(download_paths[subset]['zenodo'], output)
            else:
                if source == 'gdrive':
                    gdown.download('{}{}'.format(gdrive_prefix, download_paths[subset][feature]['gdrive']),
                                   output,
                                   quiet=False)
                else:
                    wget.download(download_paths[subset][feature]['zenodo'], output)

            if unpack_zips:
                unpack_zip(output, output_dir)
            if remove_zips:
                remove_zip(output)
        else:
            for feature in download_types:
                print('Downloading {} folder for {}'.format(feature, subset))

                output = os.path.join(output_dir, download_paths[subset][feature]['filename'])

                if source == 'gdrive':
                    gdown.download('{}{}'.format(gdrive_prefix, download_paths[subset][feature]['gdrive']),
                                   output,
                                   quiet=False)
                else:
                    wget.download(download_paths[subset][feature]['zenodo'], output)

                if unpack_zips:
                    unpack_zip(output, output_dir)
                if remove_zips:
                    remove_zip(output)


def unpack_zip(output, output_dir):
    print('Unpacking the zip file {} into {}'.format(output, output_dir))
    with ZipFile(output, 'r') as z:
        z.extractall(output_dir)


def remove_zip(output):
    print('Removing the zip file {}'.format(output))
    os.remove(output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download script for Da-TACOS',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--dataset', 
                        default='metadata',
                        choices=['metadata', 'benchmark', 'coveranalysis', 'da-tacos'],
                        help='which subsets to download. \'da-tacos\' option downloads both subsets. the options other '
                             'than \'metadata\' will download the metadata as well.')
    parser.add_argument('--type',
                        default='single_files',
                        nargs='+',
                        choices=['single_files', 'cens', 'crema', 'hpcp', 'key', 'madmom', 'mfcc', 'tags'],
                        help='which folder to download. for downloading multiple folders, you can enter multiple '
                             'arguments (e.g. \'--type cens crema\'). for detailed explanation, please check '
                             'https://mtg.github.io/da-tacos/')
    parser.add_argument('--source',
                        default='gdrive',
                        choices=['gdrive', 'zenodo'],
                        help='from which source to download the files. you can either download from Google Drive '
                             '(gdrive) or from Zenodo (zenodo)')
    parser.add_argument('--outputdir',
                        default='./',
                        help='directory to store the dataset')
    parser.add_argument('--unpack', action='store_true', help='unpack the zip files')
    parser.add_argument('--remove', action='store_true', help='remove zip files after unpacking')

    args = parser.parse_args()

    if args.dataset == 'benchmark' and args.type == 'tags':
        raise Exception('Tags are only available in cover analysis subset. Please select either \'coveranalysis\' or '
                        '\'da-tacos\' to download the tags.')

    if args.source == 'zenodo':
        raise Exception('Currently, we only support downloads from Google Drive.')

    download(args.dataset, args.type, args.source, args.outputdir, args.unpack, args.remove)