from pathlib import Path

import warnings

import matplotlib.pyplot as plt

import pandas as pd
warnings.filterwarnings('ignore')

STATUSES_ORDER = ["not answered", "rejected", "ghosted", "withdrawn",
                  "rejected after 1st interview",
                  "rejected after 2nd interview",
                  "rejected after 3rd interview",
                  "offer"]


def calculate_statistics():
    df = pd.read_csv(Path('../data/finland_2024_spring.csv'))
    df['Status'] = pd.Categorical(df['Status'], STATUSES_ORDER)

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
    df_interviewed = df_interviewed.sort_values(by='Status')

    print(f'Number of invitations to the first interview round: {len(df_interviewed)}, '
          f'per cent: {(len(df_interviewed) / all_items_number) * 100:.0f}')
    print(f'Average waiting time for feedback after application (invitation for the interview): {df_interviewed["Waiting time"].mean().days}')

    df_rejected['Waiting time'] = df_rejected['Contact back'] - df_rejected['Date of application']
    print(f'Average waiting time for feedback after application (rejection): {df_rejected["Waiting time"].mean().days}')

    df_offer = df[df['Status'] == 'offer']
    if len(df_offer) > 0:
        print(f'\nOffers numbers: {len(df_offer)}, per cent: {(len(df_offer) / all_items_number) * 100:.0f}')

    # Prepare visualization
    labels = ['not\n answered', 'rejected before\n interview', 'got interview']
    sizes = [24, 53, 23]
    explode = (0, 0.0, 0.2)

    fig_size = (14.0, 4.0)
    fig, axs = plt.subplots(1, 2, figsize=fig_size,
                            gridspec_kw={'width_ratios': [1, 2], 'wspace': 1.0})

    axs[0].pie(sizes, explode=explode, labels=labels, autopct='%1.0f%%',
               shadow=False, startangle=90, colors=['gold', 'tomato', 'cornflowerblue'],
               textprops={'fontsize': 13}, radius=0.5)
    axs[0].axis('equal')
    axs[1].scatter(df_not_answered['Date of application'], df_not_answered['Status'], s=50, c='gold', edgecolors={'black'})
    axs[1].scatter(df_rejected['Date of application'], df_rejected['Status'], s=50, c='tomato', edgecolors={'black'})
    axs[1].scatter(df_interviewed['Date of application'], df_interviewed['Status'], s=50, c='cornflowerblue', edgecolors={'black'})
    plt.xticks(rotation=45)
    axs[1].set_xlabel('Datetime of the application', fontsize=15)
    axs[1].set_ylabel('Status', fontsize=15)
    axs[1].grid()

    plt.suptitle(f'Number of processed applications: {len(df)}')
    fig.savefig(Path('.', 'finland_2024_spring_eng.png'), dpi=300, bbox_inches='tight')
    plt.close()


if __name__ == '__main__':
    calculate_statistics()
