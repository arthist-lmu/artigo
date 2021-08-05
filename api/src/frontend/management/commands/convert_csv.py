import os
import sys
import uuid
import shutil
import argparse

import numpy as np
import pandas as pd

NS = uuid.UUID('9db60607-6b12-41eb-8848-eafd26681583')


def get_hex(x, prefix='artigo'):
    return uuid.uuid3(NS, f'{prefix}_{x}').hex


def get_path(x, folder):
    folder = os.path.join(folder, f'{x[0:2]}/{x[2:4]}')
    if not os.path.exists(folder): os.makedirs(folder)

    return os.path.join(folder, f'{x}.jpg')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, type=str, help='input folder')
    parser.add_argument('--output', required=True, type=str, help='output folder')
    parser.add_argument('--image_input', type=str, help='image input folder')
    parser.add_argument('--image_output', type=str, help='image output folder')
    parser.add_argument('--n_sessions', default=-1, type=int, help='number of sessions')

    return parser.parse_args()


def main():
    args = parse_args()
    csv_args = {'na_values': '\\N', 'low_memory': False}

    if os.path.isdir(args.input):
        gametype = pd.read_csv(os.path.join(args.input, 'gametype.csv'), **csv_args)
        gametype = gametype[gametype.name.isin(['imageLabeler'])]
        gametype = gametype[['id', 'name', 'rounds', 'roundduration']]
        gametype = gametype.rename(columns={'roundduration': 'round_duration'})

        gamesession = pd.read_csv(os.path.join(args.input, 'gamesession.csv'), **csv_args)
        gamesession = gamesession[gamesession.gametype_id.isin(gametype.id)]
        gamesession = gamesession[['id', 'gametype_id']]

        if args.n_sessions > 0:
            gamesession = gamesession.head(args.n_sessions)

        gameround = pd.read_csv(os.path.join(args.input, 'gameround.csv'), **csv_args)
        gameround = gameround[gameround.gamesession_id.isin(gamesession.id)]
        gameround = gameround[['id', 'person_id', 'gamesession_id', 'startdate', 'score']]
        gameround = gameround.rename(columns={'person_id': 'user_id', 'startdate': 'created'})

        gameround_fst = gameround.groupby(['gamesession_id'])
        gameround_fst = gameround_fst.agg({'created': np.min, 'user_id': np.min})
        gameround_fst = gameround_fst.reset_index(drop=False)
        gameround_fst = gameround_fst.rename(columns={'gamesession_id': 'id'})

        gamesession = pd.merge(gamesession, gameround_fst, on='id')
        
        tagging = pd.read_csv(os.path.join(args.input, 'tagging.csv'), **csv_args)
        tagging = tagging[tagging.gameround_id.isin(gameround.id)]
        tagging = tagging.rename(columns={'person_id': 'user_id'})

        tag = pd.read_csv(os.path.join(args.input, 'tag.csv'), **csv_args)
        tag = tag[tag.id.isin(tagging.tag_id)]
        tag = tag[['id', 'name', 'language']]
        
        resource = pd.read_csv(os.path.join(args.input, 'resource.csv'), **csv_args)
        resource = resource[resource.id.isin(tagging.resource_id)]
        resource = resource[['id', 'artist_id', 'source_id', 'datecreated', 'location', 'institution', 'origin', 'enabled', 'path']]
        resource = resource.rename(columns={'artist_id': 'creator_id', 'datecreated': 'created'})

        if os.path.isdir(args.image_input):
            images = pd.DataFrame({'path': os.listdir(args.image_input)})
            images['hash_id'] = np.vectorize(get_hex)(images['path'])
            resource = pd.merge(resource, images, on='path', how='left')

            if os.path.isdir(args.image_output):
                for _, row in resource.iterrows():
                    try:
                        path_from = os.path.join(args.image_input, row.path)
                        path_to = get_path(row.hash_id, args.image_output)

                        shutil.copy(path_from, path_to)
                    except Exception as e:
                        pass

        # TODO: add created_start, created_end (use unstruwwel)

        title = pd.read_csv(os.path.join(args.input, 'title.csv'), **csv_args)
        title = title[title.resource_id.isin(resource.id)]
        title = title.rename(columns={'title': 'name'})
        title = title[~title.name.isin(['Ohne Titel', 'Unknown'])]

        source = pd.read_csv(os.path.join(args.input, 'source.csv'), **csv_args)
        source = source[source.id.isin(resource.source_id)]
        source = source[['id', 'name', 'homepage']]
        source = source.rename(columns={'homepage': 'url'})

        person = pd.read_csv(os.path.join(args.input, 'person.csv'), **csv_args)

        user = person[person.id.isin(tagging.user_id)]
        user = user.dropna(axis=0, subset=['username', 'email'])
        user = user[['id', 'username', 'email', 'password', 'forename', 'surname', 'registration']]
        user = user.rename(columns={'forename': 'first_name', 'surname': 'last_name', 'registration': 'date_joined'})

        gamesession.loc[~gamesession.user_id.isin(user.id), 'user_id'] = np.nan
        gameround.loc[~gameround.user_id.isin(user.id), 'user_id'] = np.nan
        tagging.loc[~tagging.user_id.isin(user.id), 'user_id'] = np.nan

        creator = person[person.id.isin(resource.creator_id)]
        creator.fillna('', inplace=True)
        creator['name'] = creator.forename + ' ' + creator.surname
        creator.name = creator.name.str.strip()
        creator = creator.replace(r'^\s*$', np.nan, regex=True)
        creator = creator.dropna(axis=0, subset=['name'])
        creator = creator[['id', 'name']]
        creator = creator[~creator.name.isin(['Anonym', 'Unbekannt', 'Unknown'])]

        resource.loc[~resource.creator_id.isin(creator.id), 'creator_id'] = np.nan

        if not os.path.exists(args.output):
            os.makedirs(args.output)

        user.to_csv(os.path.join(args.output, 'user.csv'), index=False)
        source.to_csv(os.path.join(args.output, 'source.csv'), index=False)
        creator.to_csv(os.path.join(args.output, 'creator.csv'), index=False)
        resource.to_csv(os.path.join(args.output, 'resource.csv'), index=False)
        title.to_csv(os.path.join(args.output, 'title.csv'), index=False)
        gametype.to_csv(os.path.join(args.output, 'gametype.csv'), index=False)
        gamesession.to_csv(os.path.join(args.output, 'gamesession.csv'), index=False)
        gameround.to_csv(os.path.join(args.output, 'gameround.csv'), index=False)
        tag.to_csv(os.path.join(args.output, 'tag.csv'), index=False)
        tagging.to_csv(os.path.join(args.output, 'tagging.csv'), index=False)


if __name__ == '__main__':
    sys.exit(main())
