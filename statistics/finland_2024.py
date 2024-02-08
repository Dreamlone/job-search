from pathlib import Path

import warnings

import numpy as np
import pandas as pd
warnings.filterwarnings('ignore')


def calculate_statistics():
    df = pd.read_csv(Path('../data/finland_2024.csv'))
    for col in ['Date of application', 'Contact back',
                'First interview', 'Second interview', 'Third interview']:
        df[col] = pd.to_datetime(df[col], format='%d.%m.%Y')

    all_items_number = len(df)
    df_not_answered = df[df['Status'] == 'not answered']
    print(f'Number of non-answered: {len(df_not_answered)}, per cent: {(len(df_not_answered) / all_items_number) * 100:.0f}')

    df_rejected = df[df['Status'] == 'rejected']
    print(f'Number of rejected: {len(df_rejected)}, per cent: {(len(df_rejected) / all_items_number) * 100:.0f}')

    df_interviewed = df.query(f'Status != ["not answered", "rejected"]')
    df_interviewed['Waiting time'] = df_interviewed['Contact back'] - df_interviewed['Date of application']
    print(f'Number of invitations to the first interview round: {len(df_interviewed)}, '
          f'per cent: {(len(df_interviewed) / all_items_number) * 100:.0f}')
    print(f'Average waiting time for feedback after application (invitation for the interview): {df_interviewed["Waiting time"].mean().days}')

    df_rejected['Waiting time'] = df_rejected['Contact back'] - df_rejected['Date of application']
    print(f'Average waiting time for feedback after application (rejection): {df_rejected["Waiting time"].mean().days}')


if __name__ == '__main__':
    calculate_statistics()
