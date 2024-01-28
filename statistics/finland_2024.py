from pathlib import Path

import warnings

import numpy as np
import pandas as pd
warnings.filterwarnings('ignore')


def calculate_statistics():
    """ Train model and save it """
    df = pd.read_csv(Path('../data/finland_2024.csv'))
    for col in ['Date of application', 'Contact back',
                'First interview', 'Second interview', 'Third interview']:
        df[col] = pd.to_datetime(df[col], format='%d.%m.%Y')

    all_items_number = len(df)
    df_not_answered = df[df['Status'] == 'not answered']
    print(f'Number of non-answered: {len(df_not_answered)}, per cent: {(len(df_not_answered) / all_items_number) * 100:.0f}')

    df_rejected = df[df['Status'] == 'rejected']
    print(f'Number of rejected: {len(df_rejected)}, per cent: {(len(df_rejected) / all_items_number) * 100:.0f}')

    got_invitations_number = all_items_number - len(df_not_answered) - len(df_rejected)
    # df_interviewed = df[df['First interview'] != pd.Nan]
    print(f'Number of invitations to the first interview round: {got_invitations_number}, per cent: {(got_invitations_number / all_items_number) * 100:.0f}')

    df_rejected['Waiting time'] = df_rejected['Contact back'] - df_rejected['Date of application']
    print(f'Average waiting time to get rejection: {df_rejected["Waiting time"].mean().days}')


if __name__ == '__main__':
    calculate_statistics()
