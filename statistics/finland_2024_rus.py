from pathlib import Path

import warnings

import matplotlib.pyplot as plt

import pandas as pd
warnings.filterwarnings('ignore')


def calculate_statistics():
    df = pd.read_csv(Path('../data/finland_2024.csv'))
    for col in ['Date of application', 'Contact back',
                'First interview', 'Second interview', 'Third interview']:
        df[col] = pd.to_datetime(df[col], format='%d.%m.%Y')

    all_items_number = len(df)
    df_not_answered = df[df['Status'] == 'not answered']
    print(f'Количество заявок на которые не было получено ответа: {len(df_not_answered)}, проценты: {(len(df_not_answered) / all_items_number) * 100:.0f}')

    df_rejected = df[df['Status'] == 'rejected']
    print(f'Количество отказов без приглашения на интервью: {len(df_rejected)}, проценты: {(len(df_rejected) / all_items_number) * 100:.0f}')

    df_interviewed = df.query(f'Status != ["not answered", "rejected"]')
    df_interviewed['Waiting time'] = df_interviewed['Contact back'] - df_interviewed['Date of application']
    print(f'Количество приглашений на первое собеседование: {len(df_interviewed)}, '
          f'проценты: {(len(df_interviewed) / all_items_number) * 100:.0f}')
    print(f'Среднее время ожидания обратной связи (в случае приглашения на интервью): {df_interviewed["Waiting time"].mean().days}')

    df_rejected['Waiting time'] = df_rejected['Contact back'] - df_rejected['Date of application']
    print(f'Среднее время ожидания обратной связи (в случае отказа): {df_rejected["Waiting time"].mean().days}')

    # Prepare visualization
    labels = ['не ответили', 'отказали без приглашения\n на собеседование', 'пригласили на\n собеседование']
    sizes = [34, 61, 5]
    explode = (0, 0.0, 0.2)

    fig_size = (14.0, 4.0)
    fig, axs = plt.subplots(1, 2, figsize=fig_size,
                            gridspec_kw={'width_ratios': [1, 2], 'wspace': 1.0})

    axs[0].pie(sizes, explode=explode, labels=labels, autopct='%1.0f%%',
               shadow=False, startangle=90, colors=['gold', 'tomato', 'cornflowerblue'],
               textprops={'fontsize': 13}, radius=0.5)
    axs[0].axis('equal')
    axs[1].scatter(df_rejected['Date of application'], df_rejected['Status'], s=50, c='tomato', edgecolors={'black'})
    axs[1].scatter(df_not_answered['Date of application'], df_not_answered['Status'], s=50, c='gold', edgecolors={'black'})
    axs[1].scatter(df_interviewed['Date of application'], df_interviewed['Status'], s=50, c='cornflowerblue', edgecolors={'black'})
    axs[1].set_xlabel('Дата подачи заявления', fontsize=15)
    axs[1].set_ylabel('Статус', fontsize=15)
    axs[1].grid()

    plt.suptitle(f'Количество поданных заявки: {len(df)}')
    fig.savefig(Path('.', 'finland_2024_rus.png'), dpi=300, bbox_inches='tight')
    plt.close()


if __name__ == '__main__':
    calculate_statistics()
